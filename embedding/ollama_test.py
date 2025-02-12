# from langchain_openai import ChatOpenAI
# import os
#
# os.environ['OPENAI_BASE_URL'] = 'http://10.104.60.47:21434/v1'
# os.environ['OPENAI_API_KEY'] = 'sk-fake'
#
# llm = ChatOpenAI(temperature=0, model_name='qwen2:7b-instruct')
#
# from langchain_core.messages import HumanMessage, SystemMessage
#
# content = "你好，你是谁？"
# print("问：" + content)
# messages = [
#     # SystemMessage(content="你是一个情感小助手，你叫TT"),
#     HumanMessage(content=content),
# ]
# response = llm.invoke(messages)
# print(response)

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager

template = """Question: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)
# 配置流式输出
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

model = ChatOllama(base_url='http://10.104.60.47:21434', model="qwen2:7b-instruct", callbacks=callback_manager)

chain = prompt | model

response = chain.invoke({"question": "介绍一下你自己"})

print(response)
