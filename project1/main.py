from dotenv import find_dotenv, load_dotenv
from langchain_unstructured import UnstructuredLoader

_ = load_dotenv(find_dotenv())

file_path = "C:/Users/Internet/Desktop/微服务例会文档/微服务开发沟通例会2024-10-11.pdf"

loader = UnstructuredLoader(
    file_path=file_path,
    strategy="hi_res"
)
docs = []
for doc in loader.lazy_load():
    docs.append(doc)
print(len(docs))

first_page_docs = [doc for doc in docs if doc.metadata.get("page_number") == 1]

for doc in first_page_docs:
    print(doc.page_content)
