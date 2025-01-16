from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from ..config.openrouter_models import DEFAULT_MODELS


class OpenRouterIntegration:
    def __init__(self, api_key: str, custom_models: dict = None):
        """
        Initialize OpenRouter integration with optional custom model configurations.

        Args:
            api_key: OpenRouter API key
            custom_models: Optional dict to override default model configurations
        """
        self.api_key = api_key
        self.models = DEFAULT_MODELS.copy()
        self.base_url = "https://openrouter.ai/api/v1"

        # Override with custom models if provided
        if custom_models:
            for model_type, config in custom_models.items():
                if model_type in self.models:
                    self.models[model_type].update(config)

        # Initialize LLM client
        self.llm = ChatOpenAI(
            model=self.models["text_generation"]["id"],
            temperature=self.models["text_generation"]["default_params"]["temperature"],
            max_tokens=self.models["text_generation"]["default_params"]["max_tokens"],
            api_key=api_key,
            base_url=self.base_url,
            max_retries=3,
            timeout=30,
        )

    def set_model(self, model_type: str, model_id: str, default_params: dict = None):
        """Set or update a model configuration."""
        if model_type not in self.models:
            self.models[model_type] = {"id": model_id, "default_params": {}}
        else:
            self.models[model_type]["id"] = model_id

        if default_params:
            self.models[model_type]["default_params"].update(default_params)

        # Update LLM client if text generation model changed
        if model_type == "text_generation":
            self.llm = ChatOpenAI(
                model=model_id,
                api_key=self.api_key,
                base_url=self.base_url,
                max_retries=3,
                timeout=30,
                **self.models[model_type]["default_params"],
            )

    def generate_text(self, prompt: str) -> Optional[str]:
        """Generate text using the configured model."""
        try:
            print("\nPreparing to generate text...")
            print(f"Using model: {self.models['text_generation']['id']}")

            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ]

            print("\nSending request to OpenRouter...")
            response = self.chat_completion(messages)

            if not response or "choices" not in response:
                print("No valid response from OpenRouter")
                return None

            generated_text = response["choices"][0]["message"]["content"]
            print(f"\nGenerated text: {generated_text}")

            return generated_text.strip()

        except Exception as e:
            print(f"Text generation failed: {str(e)}")
            return None

    def chat_completion(
        self, messages: List[Dict[str, str]], model_type: str = "chat", **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Get chat completion using the specified model type."""
        try:
            # Convert dict messages to langchain message objects
            langchain_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    langchain_messages.append(SystemMessage(content=msg["content"]))
                else:
                    langchain_messages.append(HumanMessage(content=msg["content"]))

            response = self.llm.invoke(langchain_messages)
            return {
                "choices": [
                    {"message": {"content": response.content, "role": "assistant"}}
                ]
            }

        except Exception as e:
            print(f"Chat completion failed: {str(e)}")
            return None
