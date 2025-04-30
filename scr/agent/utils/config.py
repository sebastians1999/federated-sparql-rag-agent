"""Define the configurable parameters for the SPARQL RAG agent."""

from __future__ import annotations
import os
from dataclasses import dataclass, field, fields
from typing import Optional, Dict, Any, List

from langchain_core.runnables import RunnableConfig


@dataclass
class LLMConfig:
    """Configuration for the Language Model."""

    # Supported models for parsing:
    # meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo(32K context)
    # meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo
    # meta-llama/Llama-3.2-3B-Instruct-Turbo
    # meta-llama/Llama-3.3-70B-Instruct-Turbo
    # deepseek-ai/DeepSeek-V3


    temperature: Dict[str, float] = field(default_factory=lambda: {
        "question_understanding": 0.2,
        "sparql_construction": 0.8,
    })
    max_tokens: Dict[str, int] = field(default_factory=lambda: {
        "question_understanding": 4000,
        "sparql_construction": 15000,
    })
    top_p: Dict[str, float] = field(default_factory=lambda: {
        "question_understanding": 1.0,
        "sparql_construction": 1.0,
    })

    # Model/provider selection
    provider_question_understanding: str = "google-genai"
    provider_sparql_construction: str = "google-genai"
    question_understanding_model: str = "gemini-2.0-flash"
    #sparql_construction_model: str = "gemini-2.0-flash"
    #sparql_construction_model: str = "gemini-2.5-flash-preview-04-17"
    sparql_construction_model: str = "gemini-2.5-pro-exp-03-25"
    #question_understanding_model: str = "gemini-2.0-flash-thinking-exp-01-21"



    extra_params: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "google-genai": {
            "gemini-2.5-flash-preview-04-17": {
                "thinkingBudget": 0
            }
        }
    })


    # provider_1: str = "together"
    # provider_2: str = "openai"
    # provider_3: str = "anthropic"
    # provider_4: str = "groq"
    # provider_5: str = "google-genai"
    # Model configurations for each provider

    # Together models
    # together_model_1: str = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
    # together_model_2: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
    
    # # OpenAI models
    # openai_model_1: str = "gpt-3.5-turbo"
    # openai_model_2: str = "gpt-4"
    
    # # Anthropic models
    # anthropic_model_1: str = "claude-3-opus-20240229"
    # anthropic_model_2: str = "claude-3-sonnet-20240229"
    
    # # Groq models
    #groq_model_1: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    # groq_model_2: str = "mixtral-8x7b-32768"
    
    # Google GenAI models
    # google_genai_model_1: str = "gemini-2.0-flash"
    # google_genai_model_2: str = "gemini-2.0-flash-thinking-exp-01-21"
    # google_genai_model_2: str = "models/gemini-2.5.pro-exp-03-25"
    
    # # For backward compatibility
    # model_1: str = "meta-llama/Llama-3.3-3B-Instruct-Turbo"
    # model_2: str = "meta-llama/Llama-3.2-3B-Instruct-Turbo"
    
    # API keys for different providers
    together_api_key: Optional[str] = os.environ.get("TOGETHER_API_KEY")
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    google_genai_api_key: Optional[str] = os.environ.get("GOOGLE_API_KEY")
    
    
    # For backward compatibility
    provider: str = "together"
    api_key: Optional[str] = None
    api_base: Optional[str] = None

    @property
    def meta_data(self):
        return {
            "question_understanding_model": self.question_understanding_model,
            "sparql_query_construction_model": self.sparql_construction_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "extra_params": self.extra_params
        }


@dataclass
class RAGConfig:
    """Configuration for Retrieval Augmented Generation."""
    
    vectordb_url: str = "http://vectordb:6334/"
    host: str = "localhost"
    grpc_port: int = 6334
    timeout: int = 60  

    collection_name: Optional[str] = "biomedical_entity_collection_v4.0"
    dense_embedding_model: str = "BAAI/bge-small-en-v1.5"
    sparse_embedding_model: str = "Qdrant/bm25"
    embeddings_cache_dir: str = "./embeddings_model_cache"
    
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 5


@dataclass
class LoggingConfig:
    """Configuration for logging."""
    
    log_level: str = "INFO"
    log_file: Optional[str] = None
    enable_console_logging: bool = True
    enable_file_logging: bool = False


@dataclass(kw_only=True)
class Configuration:
    """Main configuration for the agent runner."""
    
    llm_config: LLMConfig = field(default_factory=LLMConfig)
    rag_config: RAGConfig = field(default_factory=RAGConfig)
    logging_config: LoggingConfig = field(default_factory=LoggingConfig)
    
    recursion_limit: int = 10
    timeout: int = 300  # seconds
    
    # Additional parameters
    cache_results: bool = True
    cache_dir: str = ".cache"
    
    # Test mode flag for retrieval of Qdrant
    test_mode: bool = True
    
    
    # Custom parameters for specific nodes
    node_params: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # List of enabled nodes/components
    enabled_components: List[str] = field(default_factory=list)
    
    
    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> Configuration:
        """Create a RunnerConfig instance from a RunnableConfig object."""
        configurable = (config.get("configurable") or {}) if config else {}
        
        # Extract top-level fields
        _fields = {f.name for f in fields(cls) if f.init}
        top_level_params = {k: v for k, v in configurable.items() if k in _fields and k not in ["llm_config", "rag_config", "logging_config"]}
        
        # Extract nested config fields
        llm_config_params = configurable.get("llm_config", {})
        rag_config_params = configurable.get("rag_config", {})
        logging_config_params = configurable.get("logging_config", {})
        
        # Create nested configs
        llm_config = LLMConfig(**llm_config_params) if llm_config_params else LLMConfig()
        rag_config = RAGConfig(**rag_config_params) if rag_config_params else RAGConfig()
        logging_config = LoggingConfig(**logging_config_params) if logging_config_params else LoggingConfig()
        
        # Create and return the RunnerConfig
        return cls(
            llm_config=llm_config,
            rag_config=rag_config,
            logging_config=logging_config,
            **top_level_params
        )