import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:256"

from transformers import AutoTokenizer, AutoModelForCausalLM
from openai import OpenAI

import models.config as config
from utils.mylogger import MyLogger
from models.llm import LLM

_model_name_map_local = {
    "deepseekcoder-33b": "deepseek-ai/deepseek-coder-33b-instruct",
    "deepseekcoder-7b": "deepseek-ai/deepseek-coder-7b-instruct-v1.5",
    "deepseekcoder-v2-15b": "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct",
}

_model_name_map_api = {
    "deepseek-chat": "deepseek-chat",
    "deepseek-coder": "deepseek-coder",
}

_API_DEFAULT_PARAMS = {"temperature": 0, "n": 1, "max_tokens": 2048, "stop": ""}


class DeepSeekModel(LLM):
    def __init__(self, model_name, logger: MyLogger, **kwargs):
        # If caller wants to use an OpenAI-compatible DeepSeek endpoint, skip local model loading.
        use_api = kwargs.get("use_api", False) or model_name.lower() in _model_name_map_api or bool(os.getenv("DEEPSEEK_BASE_URL")) or bool(os.getenv("OPENAI_BASE_URL"))
        if use_api:
            self.model_name = model_name
            self.model_id = _model_name_map_api.get(model_name.lower(), model_name)
            self.kwargs = kwargs
            self.log = (lambda x: print(x)) if logger is None else (lambda x: logger.log(x))
            api_key = kwargs.get("deepseek_api_key") or kwargs.get("openai_api_key") or os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
            base_url = kwargs.get("openai_base_url") or os.getenv("OPENAI_BASE_URL") or os.getenv("DEEPSEEK_BASE_URL")
            self.client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
            self.use_api = True
            return

        # Fallback to local HF weights
        super().__init__(model_name, logger, _model_name_map_local, **kwargs)
        self.terminators = [
            self.pipe.tokenizer.eos_token_id,
            # self.pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
        self.use_api = False

    def predict(self, main_prompt, batch_size=0, no_progress_bar=False):
        if getattr(self, "use_api", False):
            # expecting list of two messages: system + user
            system_prompt = main_prompt[0]["content"]
            user_prompt = main_prompt[1]["content"]
            prompt = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
            response = self.client.chat.completions.create(model=self.model_id, messages=prompt, **_API_DEFAULT_PARAMS)
            return response.choices[0].message.content

        def rename(d):
            newd = dict()
            newd["role"] = "user"
            newd["content"] = d[0]["content"] + "\n" + d[1]["content"]
            return [newd]

        if batch_size > 0:
            prompts = [self.pipe.tokenizer.apply_chat_template(rename(p), tokenize=False, add_generation_prompt=True) for p in main_prompt]
            self.model_hyperparams["temperature"] = 0.0
            return self.predict_main(prompts, batch_size=batch_size, no_progress_bar=no_progress_bar)
        else:
            prompt = self.pipe.tokenizer.apply_chat_template(
                main_prompt,
                tokenize=False,
                add_generation_prompt=True,
            )
            l = len(self.tokenizer.tokenize(prompt))
            self.log("Prompt length:" + str(l))
            limit = 16000 if self.kwargs["max_input_tokens"] is None else self.kwargs["max_input_tokens"]
            if l > limit:
                return "Too long, skipping: " + str(l)
            self.model_hyperparams["temperature"] = 0.01
            return self.predict_main(prompt, no_progress_bar=no_progress_bar)
