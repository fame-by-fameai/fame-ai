import os
import time
import replicate
import requests
from pathlib import Path
from typing import Optional
import base64


class ReplicateIntegration:
    """Integration with Replicate API for image generation and face swapping."""

    def __init__(self, api_key: str):
        """Initialize Replicate integration."""
        os.environ["REPLICATE_API_TOKEN"] = api_key
        self.client = replicate.Client(api_token=api_key)
        print("Successfully initialized Replicate client")

    def generate_image(self, prompt: str, negative_prompt: str = None) -> Optional[str]:
        """Generate an image using Replicate's image generation model."""
        try:
            print("\nStarting image generation...")
            print(f"Prompt: {prompt}")

            # Configure model and input
            model = "xlabs-ai/flux-dev-realism:39b3434f194f87a900d1bc2b6d4b983e90f0dde1d5022c27b52c143d670758fa"
            input_data = {
                "prompt": prompt,
                "guidance": 3.5,
                "num_outputs": 1,
                "aspect_ratio": "4:5",
                "lora_strength": 0.8,
                "output_format": "webp",
                "output_quality": 100,
                "num_inference_steps": 30,
            }

            # Run prediction
            output = self.client.run(model, input=input_data)
            if not output:
                print("No output received from model")
                return None

            # Get output URL
            output_url = output[0] if isinstance(output, list) else output

            # Create temp directory
            temp_dir = Path("temp")
            temp_dir.mkdir(exist_ok=True)

            # Save the generated image
            output_path = temp_dir / f"generated_image_{int(time.time())}.png"

            print(f"Downloading image from: {output_url}")
            response = requests.get(output_url)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"\nSuccessfully saved image to: {output_path}")
            return str(output_path)

        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return None

    def face_swap(self, base_image_path: str, face_image_path: str) -> Optional[str]:
        """Swap faces in images using Replicate's face swap model."""
        try:
            print("\nStarting face swap...")
            print(f"Base image: {base_image_path}")
            print(f"Face image: {face_image_path}")

            # Function to convert image to data URI
            def get_data_uri(file_path: str) -> str:
                with open(file_path, "rb") as file:
                    data = base64.b64encode(file.read()).decode("utf-8")
                    return f"data:image/jpeg;base64,{data}"

            # Convert both images to data URIs
            base_image_uri = get_data_uri(base_image_path)
            face_image_uri = get_data_uri(face_image_path)

            print("Successfully converted images to data URIs")

            # Configure model
            model = "cdingram/face-swap:d1d6ea8c8be89d664a07a457526f7128109dee7030fdac424788d762c71ed111"

            # Prepare input with data URIs
            input_data = {"input_image": base_image_uri, "swap_image": face_image_uri}

            # Run face swap
            output = self.client.run(model, input=input_data)
            if not output:
                print("No output received from face swap model")
                return None

            # Get output URL
            output_url = output[0] if isinstance(output, list) else output

            # Create temp directory
            temp_dir = Path("temp")
            temp_dir.mkdir(exist_ok=True)

            # Save the swapped image
            output_path = temp_dir / f"swapped_image_{int(time.time())}.png"

            print(f"Downloading swapped image from: {output_url}")
            response = requests.get(output_url)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"Face swap successful, saved to: {output_path}")
            return str(output_path)

        except Exception as e:
            print(f"Face swap failed: {str(e)}")
            return None
