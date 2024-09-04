from langchain_core.runnables import Runnable
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())

# 向量数据库
vectorstore = Chroma(
    collection_name="example_collection",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./chroma_langchain_db",  # 演示代码使用本地存储
)
# 演示需要，先重置向量数据库
vectorstore.reset_collection()

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

# 添加知识库
vectorstore.add_documents(documents=docs)

# 检索接口
retriever = vectorstore.as_retriever()

# Prompt模板
template = """仅根据以下知识回答问题:
{context}

问题: {question}
"""
prompt = PromptTemplate.from_template(template)

# 模型
model = OpenAI()


# 用于打印检索到的知识
class PrintContext(Runnable):
    def invoke(self, inputs, config):
        print("Context:", inputs["context"])
        return inputs


# LCEL 表达式
retrieval_chain = (
        {"question": RunnablePassthrough(), "context": retriever}
        | PrintContext()  # 打印检索到的知识
        | prompt
        | model
        | StrOutputParser()
)

output = retrieval_chain.invoke("空腹可以体检嘛？")

print(output)
