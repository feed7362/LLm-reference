from pydantic_settings import BaseSettings

class ModelSettings(BaseSettings):
    model_path: str = "models/nlp/gemma-3-4b-it-q4_0.gguf"
    chat_format: str = "chatml-function-calling"
    n_gpu_layers: int = 20
    n_threads: int = 8
    n_batch: int = 256 
    use_mlock: bool = False
    use_mmap: bool = True
    n_ctx: int = 4096
    verbose: bool = True    

class DefaultInputParams(BaseSettings):
    stop: list[str] = ["<|im_end|>"]
    stream: bool = True
    repeat_penalty: float = 1.1

    class Config:
        env_prefix = "default_"

class BaseInputParams(DefaultInputParams):
    max_tokens: int = 512
    temperature: float = 0.6
    top_p: float = 0.95
    top_k: int = 40

    class Config:
        env_prefix = "base_"

class PremiumParams(DefaultInputParams):
    max_tokens: int = 1024
    temperature: float = 0.8
    top_p: float = 0.95
    top_k: int = 40

    class Config:
        env_prefix = "premium_"