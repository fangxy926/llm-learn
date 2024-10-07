from modelscope import snapshot_download

from transformers import AutoModelForCausalLM

model_id = 'qwen/Qwen2.5-1.5B'
model_dir = './model'

# 使用modelscope镜像加速下载
model_dir = snapshot_download(model_id, cache_dir=model_dir, revision='master')

# 加载模型
model = AutoModelForCausalLM.from_pretrained('./model/qwen/Qwen2___5-1___5B/', device_map="auto")

print(model)
