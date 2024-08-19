from datasets import load_dataset
import json

# Load the Wiki QA dataset from HuggingFace
wiki_qa = load_dataset('wiki_qa')

# Filter out only the positive examples (where the answer is a valid answer to the question)
positive_examples = wiki_qa['train'].filter(lambda example: example['label'] == 1)

# Create a list of dictionaries, each containing a question-answer pair
qa_pairs = [{'question': example['question'], 'answer': example['answer']} for example in positive_examples]

n = 100
cache = {}
with open('example_dataset.jsonl','w',encoding='utf-8') as fp:
    for item in qa_pairs:
        question = item['question']
        if not question in cache:
            fp.write(json.dumps(item,ensure_ascii=False)+'\n')
            cache[question]=1
            if len(cache.items()) >= n:
                break
        
