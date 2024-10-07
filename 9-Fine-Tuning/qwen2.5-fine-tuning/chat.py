# -*- coding: utf-8 -*-
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from peft import PeftModel
import textwrap

origin_model_path = "model/qwen/Qwen2___5-1___5B"

lora_path = "output/qwen2.5-1.5B-lora-20241001-024002"

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# 加载tokenizer
tokenizer = AutoTokenizer.from_pretrained(origin_model_path, trust_remote_code=True)

# 加载模型 .eval() 方法的作用是将模型切换到评估（evaluation）模式，而不是训练模式
model = AutoModelForCausalLM.from_pretrained(origin_model_path, device_map="auto").eval()

# 加载lora权重
model = PeftModel.from_pretrained(model, model_id=lora_path)

while True:
    prompt = input("\n\n请输入问题：")

    messages = [
        {"role": "system", "content": "你是一个医疗方面的专家，可以根据患者的问题进行解答。"},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True
    )

    # print(text)

    model_inputs = tokenizer([text], return_tensors="pt").to(device)
    generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=1000)
    # 此处的目的是为了从每个生成的序列中去除原始输入序列的部分，仅保留模型生成的新序列
    generated_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    wrapped_text = textwrap.fill(response, width=100)  # 100字符宽度自动换行
    print(wrapped_text)
