# Disaster recovery

query = "Hurricane helene helplines"

folder_path = query

### Loading the text files

import os

# Function to load a single text file
def load_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = file.read()
    return text_data

# Folder containing the text files
# folder_path = 'webpage_contents'  # Adjust folder name if needed

# Initialize an empty list to hold the documents
documents = []

# Loop through each file in the folder and load its content
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):  # Only process .txt files
        file_path = os.path.join(folder_path, filename)  # Full path to the file
        document = load_text_file(file_path)
        documents.append(document)

file_paths = [query +' search_results.txt']

# Loop through each file and load its content
for file_path in file_paths:
    document = load_text_file(file_path)
    documents.append(document)

print(f"Loaded {len(documents)} documents.")



### RAG pipeline

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load SentenceTransformer model for FAISS
model = SentenceTransformer('Alibaba-NLP/gte-base-en-v1.5', trust_remote_code=True)

# Convert documents to embeddings
document_embeddings = model.encode(documents, normalize_embeddings=True)

# Initialize FAISS index
d = document_embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(np.array(document_embeddings))

# Rank-BERT model and tokenizer for reranking
rank_bert_model = AutoModelForSequenceClassification.from_pretrained("castorini/monobert-large-msmarco-finetune-only")
rank_bert_tokenizer = AutoTokenizer.from_pretrained("castorini/monobert-large-msmarco-finetune-only")

# T5 model and tokenizer for answer generation
t5_model_name = "t5-large"
t5_tokenizer = T5Tokenizer.from_pretrained(t5_model_name)
t5_model = T5ForConditionalGeneration.from_pretrained(t5_model_name)
print("Models loaded successfully.")

# Function to rerank documents using Rank-BERT
def rerank_with_rank_bert(query, retrieved_docs):
    inputs = []
    for doc in retrieved_docs:
        inputs.append(rank_bert_tokenizer.encode_plus(query, doc, return_tensors='pt', truncation=True))

    scores = []
    with torch.no_grad():
        for input_data in inputs:
            outputs = rank_bert_model(**input_data)
            score = outputs.logits[0][1].item()  # Assuming binary classification for ranking
            scores.append(score)
    print("Reranking complete.")
    doc_scores = list(zip(retrieved_docs, scores))
    ranked_docs = sorted(doc_scores, key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked_docs]

# Function to generate an answer using T5 model
def generate_answer_with_t5(query, context):
    prompt = f"use the following CONTEXT to answer the QUESTION: {context} QUESTION: {query}"
    inputs = t5_tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = t5_model.generate(inputs.input_ids, max_length=150, num_beams=5, early_stopping=True)
    return t5_tokenizer.decode(outputs[0], skip_special_tokens=True)

# RAG pipeline with FAISS, reranking, and T5 model
def rag_pipeline(query):
    # Step 1: Retrieve relevant documents from FAISS
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, k=5)  # Retrieve top 5 documents
    retrieved_docs = [documents[i] for i in I[0]]
    print("Documents retrieved.")

    # Step 2: Rerank using Rank-BERT
    reranked_docs = rerank_with_rank_bert(query, retrieved_docs)

    # Step 3: Generate an answer using T5
    context = " ".join(reranked_docs)  # Joining reranked docs as context
    answer = generate_answer_with_t5(query, context)
    print("Answer generated.")
    return answer

# Test the pipeline
query = "Who to call for hurricane disastor help?"
answer = rag_pipeline(query)


# Save the query and answer to a text file

# Create a folder based on the first word of the query
firstword = query.split(" ")[0]
folder_name = firstword
os.makedirs(folder_name, exist_ok=True)

# Define the filename
filename = os.path.join(folder_name, f"{firstword}_query_answer.txt")

# Save the query and answer to the text file
with open(filename, 'w', encoding='utf-8') as file:
    file.write(f"Query: {query}\n\n")
    file.write(f"Answer: {answer}\n")

print(f"Query and answer saved to {filename}")
