import json
import pandas as pd
import os

# 配置文件路径
data_paths = [
    os.path.join("E:/Chinese-medical-dialogue-data", "样例_内科5000-6000.csv"),
    # os.path.join("E:/Chinese-medical-dialogue-data/Data_数据/Pediatric_儿科", "儿科5-14000.csv"),
    # os.path.join("E:/Chinese-medical-dialogue-data/Data_数据/Surgical_外科", "外科5-14000.csv"),
    # os.path.join("E:/Chinese-medical-dialogue-data/Data_数据/IM_内科", "内科5000-33000.csv"),
]

train_json_path = "data/train.json"
val_json_path = "data/val.json"
test_json_path = "data/test.json"

# train_json_path = "data/train-sample.json"
# val_json_path = "data/val-sample.json"
# test_json_path = "data/test-sample.json"

# 划分数据集，训练集、验证集、测试集比例：8:1:1
train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

# 使用 with 语句确保文件关闭
with open(train_json_path, "w", encoding='utf-8') as train_f, \
        open(val_json_path, "w", encoding='utf-8') as val_f, \
        open(test_json_path, 'w', encoding='utf-8') as test_f:
    def to_json(df, file):
        for index, row in df.iterrows():
            question = row["ask"]
            answer = row["answer"]
            line = {
                "question": question,
                "answer": answer
            }
            line = json.dumps(line, ensure_ascii=False)
            file.write(line + "\n")


    for path in data_paths:
        try:
            data = pd.read_csv(path, encoding='ANSI')
            # 过滤ask列为“无”的数据
            data = data[data["ask"] != "无"]

            # 随机打乱数据
            data = data.sample(frac=1).reset_index(drop=True)

            train_count = int(len(data) * train_ratio)
            val_count = int(len(data) * val_ratio)
            test_count = len(data) - train_count - val_count

            train_data = data[:train_count]
            val_data = data[train_count:train_count + val_count]
            test_data = data[train_count + val_count:]

            to_json(train_data, train_f)
            to_json(val_data, val_f)
            to_json(test_data, test_f)

        except Exception as e:
            print(f"处理 {path} 时发生错误：{e}")

print("数据处理完毕！")
