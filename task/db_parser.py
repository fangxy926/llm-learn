from typing import List

from openai import OpenAI
import os
import json
import requests

from dotenv import load_dotenv, find_dotenv

from task import ColumnInfo

_ = load_dotenv(find_dotenv())

client = OpenAI()


# 调用接口获取字段信息接口
def get_fields_info(owner: str, table: str):
    url = "http://10.104.141.230:38081/app-wyyycode/v1/database/getFieldsInfo"
    request_body = {
        "owner": owner,
        "table": table
    }
    response = requests.post(url, data=request_body)
    if response.status_code == 200:
        data = response.json()
        if data['hasError'] == -1:
            raise Exception(data['errorMessage'])
        return data['data']
    else:
        raise Exception("请求失败")


# 写文件函数
def write_file(file_name: str, content: str):
    with open(file_name, "w", encoding='UTF-8') as f:
        f.write(content)


# 可以被回调的函数放入此字典
function_mapper = {
    "get_fields_info": get_fields_info,
    "write_file": write_file
}


# 读取prompt文件
def load_prompt(file_path: str):
    with open(file_path, "r", encoding='UTF-8') as f:
        return f.read()


# 写文件


def get_completion(messages, model="gpt-3.5-turbo"):
    print("=====messages=====")
    print(messages)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        seed=1024,  # 随机种子保持不变，temperature 和 prompt 不变的情况下，输出就会不变
        tool_choice="auto",  # 默认值，由系统自动决定，返回function call还是返回文字回复
        tools=[{
            "type": "function",
            "function": {
                "name": "get_fields_info",
                "description": "根据owner和table获取字段信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "owner": {
                            "type": "string",
                            "description": "owner 用户名",
                        },
                        "table": {
                            "type": "string",
                            "description": "table 表名",
                        }
                    },
                    "required": ["owner", "table"],
                }
            }
        },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "将内容写入本地文件",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_name": {
                                "type": "string",
                                "description": "文件名",
                            },
                            "content": {
                                "type": "string",
                                "description": "内容",
                            }
                        },
                        "required": ["file_name", "content"],
                    }
                }
            }
        ]
    )
    print("=====GPT回复=====")
    print(response.choices[0])
    return response.choices[0].message


if __name__ == '__main__':

    model = "gpt-4o"

    system_prompt = load_prompt('sysprompt.txt')

    # prompt = "生成XTGL3用户下XTGL_RJKF_PSJGMX表的po文件"
    prompt = "生成XTGL3用户下xtgl_rjkf_bdys表的po文件"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    response = get_completion(messages, model)
    messages.append(response)  # 把大模型的回复加入到对话中

    # 如果返回的是函数调用结果，则打印出来
    while (response.tool_calls):
        # 1106 版新模型支持一次返回多个函数调用请求
        for tool_call in response.tool_calls:
            function_name = tool_call.function.name
            function_to_call = function_mapper[function_name]
            function_args = json.loads(tool_call.function.arguments)
            print("=====函数入参=====")
            print(function_args)
            function_response = function_to_call(**function_args)
            print("=====函数返回=====")
            print(function_response)
            messages.append({
                "tool_call_id": tool_call.id,  # 用于标识函数调用的 ID
                "role": "tool",
                "name": function_name,
                "content": str(function_response)  # 数值result 必须转成字符串
            })
        response = get_completion(messages, model)
        messages.append(response)  # 把大模型的回复加入到对话中

    print("=====最终回复=====")
    po_content = response.content
    print(po_content)
