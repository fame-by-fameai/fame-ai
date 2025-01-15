import replicate
import os
import requests
from typing import Optional, Dict, Any, Tuple
import tempfile
import time
import base64
from ..config.replicate_models import DEFAULT_MODELS


class ReplicateIntegration:
    def __init__(self, api_key: str, custom_models: dict = None):
        """
        Initialize Replicate integration with optional custom model configurations.

        Args:
            api_key: Replicate API key
            custom_models: Optional dict to override default model configurations
        """
        self.api_key = api_key
        self.models = DEFAULT_MODELS.copy()

        # Override with custom models if provided
        if custom_models:
            for model_type, config in custom_models.items():
                if model_type in self.models:
                    self.models[model_type].update(config)

    def set_model(self, model_type: str, model_id: str, default_params: dict = None):
        """
        Set or update a model configuration.

        Args:
            model_type: Type of model (e.g., "image_generation", "face_swap")
            model_id: Replicate model ID
            default_params: Optional default parameters for the model
        """
        if model_type not in self.models:
            self.models[model_type] = {"id": model_id, "default_params": {}}
        else:
            self.models[model_type]["id"] = model_id

        if default_params:
            self.models[model_type]["default_params"].update(default_params)

    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = None,
        width: int = None,
        height: int = None,
    ) -> Optional[str]:
        """Generate an image using Flux 1.1 Pro model."""
        try:
            client = replicate.Client(api_token=self.api_key)

            # Get model config
            model_config = self.models["image_generation"]
            default_params = model_config["default_params"]

            # Prepare input
            input_payload = {
                "prompt": prompt,
                "prompt_upsampling": default_params.get("prompt_upsampling", True),
                "width": width or default_params.get("width", 1024),
                "height": height or default_params.get("height", 1024),
            }

            # Run image generation
            output = client.run(
                model_config["id"],
                input=input_payload,
            )

            if output:
                output_dir = tempfile.gettempdir()
                output_path = os.path.join(output_dir, "generated_image.png")

                # Handle different types of output from Flux model
                if isinstance(output, (list, tuple)):
                    output_item = output[0] if output else None
                else:
                    output_item = output

                if not output_item:
                    print(f"No valid output received: {output}")
                    return None

                try:
                    # Handle URL output
                    if isinstance(output_item, str) and output_item.startswith("http"):
                        response = requests.get(output_item, timeout=10)
                        response.raise_for_status()  # Raise exception for bad status codes
                        with open(output_path, "wb") as f:
                            f.write(response.content)
                        return output_path

                    # Handle file-like object
                    if hasattr(output_item, "read"):
                        content = output_item.read()
                        if content:
                            with open(output_path, "wb") as f:
                                f.write(content)
                            return output_path

                    # Handle PIL Image object
                    if hasattr(output_item, "save"):
                        output_item.save(output_path, format="PNG")
                        return output_path

                    print(f"Unhandled output type: {type(output_item)}")
                    return None

                except requests.RequestException as e:
                    print(f"Error downloading image: {str(e)}")
                    return None
                except IOError as e:
                    print(f"Error saving image: {str(e)}")
                    return None

            print("No output received from model")
            return None

        except Exception as e:
            print(f"Image generation failed: {str(e)}")
            return None

    def _image_to_base64(self, image_path: str) -> Optional[str]:
        """Convert image file to base64 data URI."""
        try:
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()
            return f"data:image/jpeg;base64,{image_data}"
        except Exception as e:
            print(f"Failed to convert image to base64: {str(e)}")
            return None

    def face_swap(
        self, base_image_path: str, face_image_path: str, output_dir: str = None
    ) -> Optional[str]:
        """
        Perform face swap using Replicate's model.

        Args:
            base_image_path: Path to the base image to swap onto
            face_image_path: Path to the face image to use
            output_dir: Optional directory for output

        Returns:
            Path to the face-swapped image or None if failed
        """
        try:
            # Convert both images to base64
            base_image_data = self._image_to_base64(base_image_path)
            face_image_data = self._image_to_base64(face_image_path)

            if not base_image_data or not face_image_data:
                print("Failed to prepare images")
                return None

            # Initialize Replicate client
            client = replicate.Client(api_token=self.api_key)

            # Prepare input
            input_data = {
                "input_image": base_image_data,  # Base image to swap onto
                "swap_image": face_image_data,  # Face to use
            }

            # Run face swap model
            output = client.run(
                self.models["face_swap"]["id"],
                input=input_data,
            )

            # Handle the output
            if output:
                output_dir = output_dir or tempfile.gettempdir()
                output_path = os.path.join(output_dir, "face_swapped.jpg")

                # If output is a URL
                if isinstance(output, str) and output.startswith("http"):
                    response = requests.get(output)
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    return output_path
                # If output has a URL attribute (FileOutput object)
                elif hasattr(output, "url"):
                    response = requests.get(output.url)
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    return output_path

            print(f"Unexpected output format: {type(output)}")
            return None

        except Exception as e:
            print(f"Face swap failed: {str(e)}")
            return None

    def generate_and_swap(
        self,
        prompt: str,
        face_image_path: str,
        negative_prompt: str = None,
        retries: int = 3,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate an image with a random face and then swap it with the provided face.
        """
        try:
            # Enhance the prompt for better face generation
            enhanced_prompt = (
                f"{prompt}, close up portrait, clear face, front facing, "
                "professional lighting, high detail facial features, "
                "professional photography, 8k uhd, high quality"
            )

            # First, generate the base image
            base_image_path = self.generate_image(
                prompt=enhanced_prompt,
                negative_prompt=negative_prompt,
            )

            if not base_image_path:
                return None, None

            # Try face swapping with retries
            for attempt in range(retries):
                swapped_image_path = self.face_swap(
                    base_image_path=base_image_path,
                    face_image_path=face_image_path,
                )

                if swapped_image_path:
                    return base_image_path, swapped_image_path

                # If face swap failed, try generating a new base image
                if attempt < retries - 1:
                    print(
                        f"Face swap attempt {attempt + 1} failed, generating new base image..."
                    )
                    os.remove(base_image_path)
                    base_image_path = self.generate_image(
                        prompt=enhanced_prompt,
                        negative_prompt=negative_prompt,
                    )
                    time.sleep(1)  # Small delay between attempts

            # If all retries failed
            if os.path.exists(base_image_path):
                os.remove(base_image_path)
            return None, None

        except Exception as e:
            print(f"Generate and swap failed: {str(e)}")
            # Cleanup
            if base_image_path and os.path.exists(base_image_path):
                os.remove(base_image_path)
            return None, None
