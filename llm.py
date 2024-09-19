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

from curd.job_curd import get_job


def main():
    job = get_job("7412caa0a7a94cd41HJ92dy1FFNX")
    EMBEDDING_DEVICE = (
        "cuda"
        if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )
    embeddings = HuggingFaceEmbeddings(
        model_name="GanymedeNil/text2vec-large-chinese",
        model_kwargs={"device": EMBEDDING_DEVICE},
    )
    faiss_db_path = "faiss_job_vector_store"
    if not os.path.exists(faiss_db_path):
        print("FAISS vector database not found. Creating and saving...")
        splitter = CharacterTextSplitter(
            separator="<br>", chunk_size=20, chunk_overlap=0
        )
        splits = splitter.split_text(job.detail)
        # for i, split in enumerate(splits):
        #     print(f"Segment {i+1}:\n{split}\n")

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
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY, verbose=True
    )
    document_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": "该岗位需要熟悉什么数据库？"})
    print(response["answer"])


if __name__ == "__main__":
    main()
