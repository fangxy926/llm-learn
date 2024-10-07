# -*- coding: utf-8 -*-
import textwrap

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

origin_model_path = "model/qwen/Qwen2___5-1___5B-Instruct"
lora_path = "output/qwen2.5-1.5B-Instruct-lora-20241001-153846"

model = AutoModelForCausalLM.from_pretrained(
    origin_model_path,
    torch_dtype="auto",
    device_map="auto"
).eval()

# 加载lora权重
model = PeftModel.from_pretrained(model, model_id=lora_path)

# 加载tokenizer
tokenizer = AutoTokenizer.from_pretrained(origin_model_path)

while True:
    prompt = input("\n\n请输入问题：")

    messages = [
        {"role": "system", "content": "你是一个医疗方面的专家，可以根据患者的问题进行解答。"},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(**model_inputs, max_new_tokens=512)
    # 此处的目的是为了从每个生成的序列中去除原始输入序列的部分，仅保留模型生成的新序列
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    wrapped_text = textwrap.fill(response, width=100)  # 100字符宽度自动换行
    print("回答：")
    print(wrapped_text)
