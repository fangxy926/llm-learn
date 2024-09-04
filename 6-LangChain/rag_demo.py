from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import Docx2txtLoader

from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())

# 加载文档
loader = Docx2txtLoader("体检中心问答.docx")
doc = loader.load()
content = doc[0].page_content

# 文档切分
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n\n\n"],
    chunk_size=0,
    chunk_overlap=0,
    length_function=len
)
docs = text_splitter.create_documents([content])

# 灌库
vectorstore = Chroma(
    collection_name="example_collection",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./chroma_langchain_db",  # 演示代码使用本地存储
)

# 演示需要，先重置向量数据库
vectorstore.reset_collection()
# 添加知识库
vectorstore.add_documents(documents=docs)

# LangChain内置的 RAG 实现
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    retriever=vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={'k': 2}
    ),
    return_source_documents=True  # 返回参考的知识
)

query = "空腹可以体检吗"
response = qa_chain.invoke(query)

print("======response=======")
print(response)
