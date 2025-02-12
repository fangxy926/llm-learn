from sentence_transformers import SentenceTransformer
from modelscope import snapshot_download

model_dir = snapshot_download("iic/gte_Qwen2-1.5B-instruct")

model = SentenceTransformer(model_dir, trust_remote_code=True)
# In case you want to reduce the maximum length:
model.max_seq_length = 8192

queries = [
    "how much protein should a female eat",
    "summit define",
]
documents = [
    "As a general guideline, the CDC's average requirement of protein for women ages 19 to 70 is 46 grams per day. "
    "But, as you can see from this chart, you'll need to increase that if you're expecting or training for a "
    "marathon. Check out the chart below to see how much protein you should be eating each day.",
    "Definition of summit for English Language Learners. : 1  the highest point of a mountain : the top of a "
    "mountain. : 2  the highest level. : 3  a meeting or series of meetings between the leaders of two or more "
    "governments.",
]

query_embeddings = model.encode(queries, prompt_name="query")
document_embeddings = model.encode(documents)

scores = (query_embeddings @ document_embeddings.T) * 100
print(scores.tolist())
# [[70.00668334960938, 8.184843063354492], [14.62419319152832, 77.71407318115234]]
