import os
import json
from typing import Any
from dataclasses import asdict, is_dataclass

def write_experiment_metadata(output_dir, graph_config, extraction_prompt, query_generation_prompt, timeout):
    meta = {
        'graph_config': {},
        'extraction_prompt': extraction_prompt,
        'query_generation_prompt': query_generation_prompt,
        'timeout for result retrieval': timeout
    }
    try:
        if is_dataclass(graph_config):
            # Only keep meta_data from LLMConfig and all of RAGConfig
            llm_meta = {}
            rag_meta = {}
            if hasattr(graph_config, 'llm_config'):
                llm = graph_config.llm_config
                llm_meta = llm.meta_data if hasattr(llm, 'meta_data') else None
            if hasattr(graph_config, 'rag_config'):
                rag = graph_config.rag_config
                rag_meta = asdict(rag)
            meta['graph_config'] = {
                'llm_meta_data': llm_meta,
                'rag_config': rag_meta
            }
        else:
            meta['graph_config'] = str(graph_config)
    except Exception as e:
        meta['graph_config'] = f"[Unserializable config: {e}]"

    os.makedirs(output_dir, exist_ok=True)
    meta_path = os.path.join(output_dir, 'experiment_metadata.txt')
    with open(meta_path, 'w', encoding='utf-8') as f:
        f.write("# Experiment Metadata\n\n")
        f.write("## Graph Configuration\n")
        f.write(json.dumps(meta['graph_config'], indent=2))
        f.write("\n\n## Extraction Prompt (Question Understanding)\n")
        f.write(meta['extraction_prompt'])
        f.write("\n\n## Query Generation Prompt (SPARQL Construction)\n")
        f.write(meta['query_generation_prompt'])
        f.write("\n")
