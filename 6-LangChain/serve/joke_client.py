from langserve import RemoteRunnable

joke_chain = RemoteRunnable("http://localhost:19999/joke/")

response = joke_chain.invoke({"topic": "小明"})
print(response)
