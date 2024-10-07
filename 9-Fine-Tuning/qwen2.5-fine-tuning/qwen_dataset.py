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
        messages = [
            {"role": "system", "content": "你是一个医疗方面的专家，可以根据患者的问题进行解答。"},
            {"role": "user", "content": question}
        ]
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        instruction = self.tokenizer(prompt, add_special_tokens=False, max_length=self.max_source_length)
        response = self.tokenizer(answer, add_special_tokens=False, max_length=self.max_target_length)
        input_ids = instruction["input_ids"] + response["input_ids"] + [self.tokenizer.pad_token_id]
        attention_mask = instruction["attention_mask"] + response["attention_mask"] + [1]
        labels = [-100] * len(instruction["input_ids"]) + response["input_ids"] + [self.tokenizer.pad_token_id]
        if len(input_ids) > self.max_seq_length:
            input_ids = input_ids[:self.max_seq_length]
            attention_mask = attention_mask[:self.max_seq_length]
            labels = labels[:self.max_seq_length]
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
