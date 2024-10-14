import json
import pandas as pd
import os


def process_csv_files(input_paths, output_file, eval_ratio=0.1,
                      instruction='你是一个医疗方面的专家，可以根据患者的问题进行解答。'):
    # 创建一个空列表，用于存储转换后的数据
    alpaca_data = []

    # 遍历文件列表，读取并处理每一个CSV文件
    for csv_file in input_paths:
        # 读取当前CSV文件
        df = pd.read_csv(csv_file, encoding='ANSI')
        # 随机打乱数据
        df = df.sample(frac=1).reset_index(drop=True)

        # 遍历每一行数据，并将其转换为AlpaCA格式
        for index, row in df.iterrows():
            data = {
                "instruction": instruction,
                "input": row['ask'],
                "output": row['answer']
            }
            alpaca_data.append(data)

    # 将数据划分出训练集和验证集
    train_data = alpaca_data[:int(len(alpaca_data) * (1 - eval_ratio))]
    eval_data = alpaca_data[int(len(alpaca_data) * (1 - eval_ratio)):]

    print(f"数据已处理完毕，共 {len(alpaca_data)} 条数据，其中 {len(train_data)} 条用于训练，{len(eval_data)} 条用于验证")

    # 将训练集和验证集数据保存为JSON格式文件，文件分开保存
    with open(f"data/{output_file}_train.json", "w", encoding='utf-8') as f:
        json.dump(train_data, f, ensure_ascii=False, indent=4)
        print(f"训练集数据已保存到 {f.name}")
    with open(f"data/{output_file}_eval.json", "w", encoding='utf-8') as f:
        json.dump(eval_data, f, ensure_ascii=False, indent=4)
        print(f"验证集数据已保存到 {f.name}")


# 配置文件路径
data_paths = [
    os.path.join("E:/Chinese-medical-dialogue-data", "样例_内科5000-6000.csv"),
    # os.path.join("E:/Chinese-medical-dialogue-data/Data_数据/Pediatric_儿科", "儿科5-14000.csv"),
    # os.path.join("E:/Chinese-medical-dialogue-data/Data_数据/Surgical_外科", "外科5-14000.csv"),
    # os.path.join("E:/Chinese-medical-dialogue-data/Data_数据/IM_内科", "内科5000-33000.csv"),
]

output_file_name = "chinese-medical-dialogue"

# 处理并保存为JSON文件
process_csv_files(data_paths, output_file_name)
