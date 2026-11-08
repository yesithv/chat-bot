try:
    import truststore
    truststore.inject_into_ssl()  # use system CA certificates instead of bundled ones
except ImportError:
    pass

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from chatbot.engine import ChatEngine

MODEL_NAME = 'facebook/blenderbot-400M-distill'


class BlenderBotEngine(ChatEngine):
    """Local open-domain dialogue engine based on Facebook BlenderBot."""

    def __init__(self, model_name: str = MODEL_NAME):
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)  # downloaded once and cached in ~/.cache/huggingface
        self._model     = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self._model.eval()

    def generate(self, prompt: str) -> str:
        with torch.no_grad():  # disables gradient tracking to save memory during inference

            inputs = self._tokenizer(
                prompt,
                return_tensors = 'pt',
                truncation     = True,
                max_length     = 128  # hard limit for blenderbot-400M-distill positional embeddings
            )

            outputs = self._model.generate(
                **inputs,
                max_new_tokens       = 60,
                no_repeat_ngram_size = 3,   # blocks repeating any 3-word sequence
                repetition_penalty   = 1.3, # penalizes tokens already seen in the output
                do_sample            = True, # enables sampling instead of greedy decoding
                temperature          = 0.6, # lower = more focused, higher = more creative
                top_p                = 0.85 # nucleus sampling: keeps tokens covering 85% probability mass
            )
        return self._tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
