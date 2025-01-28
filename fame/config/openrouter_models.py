# Default OpenRouter model configurations
DEFAULT_MODELS = {
    "text_generation": {
        "id": "deepseek/deepseek-chat",  # Primary model
        "backup_models": [
            "google/gemini-2.0-flash-exp:free",
            "microsoft/phi-4",
            "openai/gpt-4o-mini",
            "anthropic/claude-3.5-sonnet:beta",
        ],
        "default_params": {
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
        },
    },
    "chat": {
        "id": "deepseek/deepseek-chat",  # Primary model
        "backup_models": [
            "google/gemini-2.0-flash-exp:free",
            "microsoft/phi-4",
            "openai/gpt-4o-mini",
            "anthropic/claude-3.5-sonnet:beta",
        ],
        "default_params": {
            "temperature": 0.8,
            "max_tokens": 500,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
        },
    },
}
