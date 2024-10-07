# -*- coding: utf-8 -*-
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from peft import PeftModel

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model_path = "./model/qwen/Qwen2___5-0___5B"
lora_dir = "output/qwen2.5-lora-20240930-071740"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
model = PeftModel.from_pretrained(model, lora_dir).to(device)
print(model)
# 合并model, 同时保存 token
model = model.merge_and_unload()
model.save_pretrained("lora_output")
tokenizer.save_pretrained("lora_output")

