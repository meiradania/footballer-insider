from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

## Loading 
print('--------- Step 1: Data Loader ---------')

loader = JSONLoader(
    file_path='./data/dataset_spain.json',
    jq_schema='.[].summary')

json_files = loader.load()

# print(json_files)

## Transform 
print('--------- Step 2: Data Transformer ---------')

chunk_size = 500
chunk_overlap = 5

text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
texts = text_splitter.split_documents(json_files)

print(f"Split into {len(texts)} chunks of text (max. {chunk_size} tokens each)")


## Data Embedding 
print('--------- Step 3: Data Embedding ---------')

from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings()
text = "This is test document."

query_result = embeddings.embed_query(text)

print(query_result)

## Store 


## Retrive 
print('--------- Step 5: Data Retriver ---------')

from langchain.vectorstores import Chroma

db = Chroma.from_documents(texts, embeddings)

query = "what was the year that FC Barcelona got founded."
answers = db.similarity_search(query)

for answer in answers:
    print('-------------------------------')
    print(answer.page_content)


