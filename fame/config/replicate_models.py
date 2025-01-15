# Default Replicate model configurations
DEFAULT_MODELS = {
    "image_generation": {
        "id": "black-forest-labs/flux-1.1-pro",
        "default_params": {
            "prompt_upsampling": True,
            "width": 1024,
            "height": 1024,
        },
    },
    "face_swap": {
        "id": "cdingram/face-swap:d1d6ea8c8be89d664a07a457526f7128109dee7030fdac424788d762c71ed111",
        "default_params": {},
    },
}
