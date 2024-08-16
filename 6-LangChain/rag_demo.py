from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader

from dotenv import find_dotenv, load_dotenv
_ = load_dotenv(find_dotenv())

# 加载文档
loader = PyPDFLoader("llama2.pdf")
pages = loader.load_and_split()

# 文档切分
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300, 
    chunk_overlap=100,
    length_function=len,
    add_start_index=True,
)

texts = text_splitter.create_documents([pages[2].page_content,pages[3].page_content])
for para in texts:
    print(para.page_content)
    print('-------')

# 灌库
embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(texts, embeddings)

print("db: ", db)

# LangChain内置的 RAG 实现
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0), 
    retriever=db.as_retriever() 
)

query = "llama 2有多少参数？"
response = qa_chain.run(query)

print("======response=======")
print(response)