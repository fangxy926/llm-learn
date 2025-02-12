# from langchain_ollama import OllamaEmbeddings
#
# embeddings = OllamaEmbeddings(
#     base_url="http://10.104.60.47:21434",
#     model="rjmalagon/gte-qwen2-1.5b-instruct-embed-f16:latest",
#     # model='mxbai-embed-large',
# )
# # text = "你好，今天是星期几？"
# text = "hello!"
#
# single_vector = embeddings.embed_query(text)
# print("Vector length:")
# print(len(single_vector))
# print("Single vector:")
# print(single_vector[:100])
#
# text2 = (
#     "LangGraph is a library for building stateful, multi-actor applications with LLMs"
# )
# two_vectors = embeddings.embed_documents([text, text2])
# for vector in two_vectors:
#     print(str(vector)[:100])  # Show the first 100 characters of the vector


#### 原生写法
from ollama import Client

client = Client(host='http://10.104.60.47:21434')
vector = client.embeddings(
    # model='rjmalagon/gte-qwen2-1.5b-instruct-embed-f16:latest',
    model='rjmalagon/gte-qwen2-7b-instruct:f16',
    prompt='你好，今天是星期几？',
)['embedding']

print("Vector length: ", len(vector))
print("Single vector:")
print(vector)

