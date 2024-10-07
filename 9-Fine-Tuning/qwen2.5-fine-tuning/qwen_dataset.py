from torch.utils.data import Dataset
import json


class QwenDataset(Dataset):
    def __init__(self, data_path, tokenizer, max_source_length, max_target_length) -> None:
        super().__init__()
        self.tokenizer = tokenizer
        self.max_source_length = max_source_length
        self.max_target_length = max_target_length
        self.max_seq_length = self.max_source_length + self.max_target_length

        self.data = []
        if data_path:
            with open(data_path, "r", encoding='utf-8') as f:
                for line in f:
                    if not line or line == "":
                        continue
                    json_line = json.loads(line)
                    question = json_line["question"]
                    answer = json_line["answer"]
                    self.data.append({
                        "question": question,
                        "answer": answer
                    })
        print("data load， size：", len(self.data))

    def preprocess(self, question, answer):
        # 构建对话模板，包括系统角色的描述和用户的问题
        messages = [
            {"role": "system", "content": "你是一个医疗方面的专家，可以根据患者的问题进行解答。"},
            {"role": "user", "content": question}
        ]
        # 使用tokenizer将对话模板转换为prompt
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        # 对问题进行编码，生成instruction的input_ids和attention_mask
        instruction = self.tokenizer(prompt, add_special_tokens=False, max_length=self.max_source_length)
        # 对答案进行编码，生成response的input_ids和attention_mask
        response = self.tokenizer(answer, add_special_tokens=False, max_length=self.max_target_length)
        # 拼接instruction和response的input_ids，并在末尾添加padding token id
        input_ids = instruction["input_ids"] + response["input_ids"] + [self.tokenizer.pad_token_id]
        # 拼接instruction和response的attention_mask，并在末尾添加1，表示这些位置都是有效信息
        attention_mask = instruction["attention_mask"] + response["attention_mask"] + [1]
        # 生成标签序列，问题部分的标签设置为-100（表示忽略），答案部分的标签为答案的token id，末尾添加padding token id
        labels = [-100] * len(instruction["input_ids"]) + response["input_ids"] + [self.tokenizer.pad_token_id]
        # 如果输入序列的长度超过了最大序列长度，进行截断
        if len(input_ids) > self.max_seq_length:
            input_ids = input_ids[:self.max_seq_length]
            attention_mask = attention_mask[:self.max_seq_length]
            labels = labels[:self.max_seq_length]
        # 返回处理后的输入序列，注意力掩码和标签序列
        return input_ids, attention_mask, labels

    def __getitem__(self, index):
        item_data = self.data[index]

        input_ids, attention_mask, labels = self.preprocess(**item_data)

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels
        }

    def __len__(self):
        return len(self.data)
