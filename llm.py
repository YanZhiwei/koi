import json
import os

import torch
from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

from manager.job import Job as JobManager


def main():
    manager = JobManager()
    job = manager.get_job("4acc74496348f6ba1nZ50ty5EFdQ")
    job_json=json.dumps(job.as_dict(),ensure_ascii=False) 
    EMBEDDING_DEVICE = (
        "cuda"
        if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )
    embeddings = HuggingFaceEmbeddings(
        model_name="moka-ai/m3e-base",
        model_kwargs={"device": EMBEDDING_DEVICE},
    )
    faiss_db_path = f"./cache/job/{job.id}"
    if not os.path.exists(faiss_db_path):
        print("FAISS vector database not found. Creating and saving...")
        splitter = CharacterTextSplitter(
            separator=",", chunk_size=200, chunk_overlap=50
        )
        splits = splitter.split_text(job_json)
        for i, split in enumerate(splits):
            print(f"Segment {i+1}:\n{split}\n")

        documents = [Document(page_content=text) for text in splits]
        vectordb = FAISS.from_documents(documents=documents, embedding=embeddings)
        vectordb.save_local(faiss_db_path)
    else:
        print("Loading FAISS vector database from disk...")
        vectordb = FAISS.load_local(
            faiss_db_path, embeddings, allow_dangerous_deserialization=True
        )
        # **添加新的文档到现有的数据库**
        # print("Adding new documents to the FAISS vector database...")
        # vectordb.add_documents(documents)
        # vectordb.save_local(faiss_db_path)

    retriever = vectordb.as_retriever()
    prompt = PromptTemplate.from_template(
        """仅根据提供的上下文回答以下问题:
    <上下文>
    {context}
    </上下文>

    问题: {input}"""
    )
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("LLM_MODEL_KEY")
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY, verbose=True
    )
    document_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": "该岗位名称是什么？"})
    print(response["answer"])


if __name__ == "__main__":
    
    main()
