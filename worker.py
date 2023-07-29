from core.celery_app import celery_app
from transformers import (TokenClassificationPipeline, AutoModelForTokenClassification, AutoTokenizer)
from transformers.pipelines import AggregationStrategy
import numpy as np
    
class KeyphraseExtractionPipeline(TokenClassificationPipeline):
    def __init__(self, model="ml6team/keyphrase-extraction-kbir-inspec", *args, **kwargs):
        super().__init__(
            model=AutoModelForTokenClassification.from_pretrained(model),
            tokenizer=AutoTokenizer.from_pretrained(model),
            *args,
            **kwargs
        )

    def postprocess(self, all_outputs):
        results = super().postprocess(
            all_outputs=all_outputs,
            aggregation_strategy=AggregationStrategy.SIMPLE,
        )
        return np.unique([result.get("word").strip() for result in results])

kw_model = KeyphraseExtractionPipeline()
@celery_app.task(bind=True)
def keyword_extraction(self,content):
    try:
        key_words = kw_model(content)
        return True, list(key_words)
    except Exception as e:
        return False, []

    
    
        
        