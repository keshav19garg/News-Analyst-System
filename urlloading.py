# #Sentence Transformers is basically a Python library that wraps Hugging Face transformer models and turns them into sentence embeddings.

from langchain_community.document_loaders import WebBaseLoader
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import pandas as pd
import os
import numpy as np
import faiss
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import json

load_dotenv()

os.environ["TRANSFORMERS_NO_TF"] = "1"
# source=[
#    "https://www.moneycontrol.com/news/business/banks/hdfc-bank-re-appoints-sanmoy-chakrabarti-as-chief-risk-officer-11259771.html",
#         "https://www.moneycontrol.com/news/business/markets/market-corrects-post-rbi-ups-inflation-forecast-icrr-bet-on-these-top-10-rate-sensitive-stocks-ideas-11142611.html"
 
# ]

def get_answer(resources,query):
    source=resources

    loader = WebBaseLoader(source)

    data = loader.load()

    documents = []
    rows = []

    # ---- CLEAN TEXT ----
    for d in data:
        txt = d.page_content.split("\n")
        full_text = " ".join(t.strip() for t in txt)
        cleaned_text = re.sub(r' {2,}', ' ', full_text)

        documents.append({
            "source": d.metadata["source"],
            "full_text": cleaned_text
        })

    # ---- SPLITTER (once) ----
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=13,
    )

    for doc in documents:
        chunks = splitter.split_text(doc["full_text"])
        for c in chunks:
            rows.append({
                "source": doc["source"],
                "text": c
            })

    df = pd.DataFrame(rows)

    # ---- EMBEDDINGS ----
    embedding_model = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    embeddings = embedding_model.embed_documents(df["text"].tolist())
    embeddings=np.array(embeddings).astype("float32")

    print(len(embeddings), len(embeddings[0]))

    #---- VECTOR ----

    dim=len(embeddings[0])

    index=faiss.IndexFlatL2(dim)
    index.add(embeddings)

    query_vector=embedding_model.embed_query(query)

    query_vector = np.array([query_vector]).astype("float32")

    distances, indices = index.search(query_vector, k=5)

    print("Nearest indices:", indices)
    print("Distances:", distances)

    new_indices=indices.flatten()

    #---- Prompt ----

    new_df=df.iloc[new_indices]
    print(new_df)
    prompt_material=new_df.to_json()


    prompt = ChatPromptTemplate.from_template("You are given extracted information from multiple articles in {prompt_material} and a user question {query}. Generate an accurate ,detailed,re;evant and complete answer to the user’s question using only the provided information. Return the response strictly in JSON format with exactly two fields: answer_text and source. Use only those sourceswhere answer is mentionsed. If the provided articles do not contain relevant information to answer the question, return answer_text as The given articles do not mention the answer to this query. and source as null. Do not include any text outside the JSON response."
)

    llm = ChatOpenAI(model="gpt-5.2", temperature=0.7)


    chain = prompt | llm | JsonOutputParser()

    final_output=chain.invoke({"prompt_material":prompt_material,"query":query})

    print(final_output)
    print(type(final_output))
    return final_output


# RetrievalQA and Chain for prompt and LLM

# text= '''
#  hello, my name is keshav

#  rishabh
#  '''
# print(text.split('\n')[0])
# with open("scrapped1.txt","w",encoding="utf-8") as f:
#     txt=data[1].page_content.split("\n")
#     full_text="".join(t for t in txt)
#     cleaned_text = re.sub(r' {2,}', ' ', full_text)
#     f.write(cleaned_text)

# # from langchain_community.document_loaders import TextLoader

# # loader = TextLoader("hello.txt")
# # data=loader.load()
# # print(data)


