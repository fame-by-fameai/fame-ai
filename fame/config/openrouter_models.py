# Default OpenRouter model configurations
DEFAULT_MODELS = {
    "text_generation": {
        "id": "deepseek/deepseek-chat",  # Primary model
        "backup_models": [
            "anthropic/claude-2",
            "google/palm-2-chat-bison",
            "meta-llama/llama-2-70b-chat",
            "anthropic/claude-instant-v1",  # Fastest fallback
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
            "anthropic/claude-instant-v1",  # Faster, cheaper backup
            "google/palm-2-chat-bison",
            "meta-llama/llama-2-70b-chat",
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
