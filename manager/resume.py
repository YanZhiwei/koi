import hashlib
import sys
from os import path

import torch
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter

sys.path.append("./")
from llm.chatModel import ChatModel
from manager.job import Job as JobManager
from models.job import Job as DB_Job_Model


class Resume(object):
    def __init__(self ,model: BaseChatModel,resume_pdf:str):
        self.model = model
        self.resume_pdf=resume_pdf
        if(self.resume_pdf is None):
            raise Exception("resume_pdf is None")
        self.resume_pdf_path = "./resume/" +self.resume_pdf
        if path.exists(self.resume_pdf_path) == False:
            raise Exception(f"{self.resume_pdf_path} not exists")
        self.key= hashlib.sha256(resume_pdf.encode()).hexdigest()[:32]
        

    def read_resume(self):
        pdf_loader = PyPDFLoader(file_path=self.resume_pdf_path)
        pdf_pages = pdf_loader.load()
        resume_text = ""
        for page in pdf_pages:
            # print(page.metadata.get('source'))
            page_text = page.page_content
            resume_text += page_text

        return resume_text

    def get_vectorstore(self):
        vectorstore_key= f"./cache/resume/{self.key}"
        EMBEDDING_DEVICE = (
            "cuda"
            if torch.cuda.is_available()
            else "mps" if torch.backends.mps.is_available() else "cpu"
        )
        embeddings = HuggingFaceEmbeddings(
            model_name="moka-ai/m3e-base",
            model_kwargs={"device": EMBEDDING_DEVICE},
        )
        if path.exists(vectorstore_key):
            return FAISS.load_local(vectorstore_key, embeddings, allow_dangerous_deserialization=True)
        resume_text = self.read_resume()
        text_splitter = CharacterTextSplitter(separator="\n\n",chunk_size=1200,chunk_overlap=100,length_function=len,is_separator_regex=False)
        chunks = text_splitter.split_text(resume_text)
        vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
        vectorstore.save_local(vectorstore_key)
        return vectorstore

    def get_self_introduction(
        self,
        vectorstore,
        job:DB_Job_Model,
        character_limit: int = 300,
    ) -> str:
        prompt_template = (
            f"""
        你将扮演一位求职者的角色,正在应聘：{job.title}岗位,根据上下文里的简历内容以及应聘工作的描述,来直接给HR写一个礼貌专业, 且字数严格限制在{character_limit}以内的求职消息,要求能够用专业的语言结合简历中的经历和技能,并结合应聘工作的描述,来阐述自己的优势,尽最大可能打动招聘者。始终使用中文来进行消息的编写,开发技能不要出现精通字眼,工作描述中要求开发技能如果不匹配则忽略。开头是招聘负责人,这是一份求职消息，不要包含求职内容以外的东西。,例如“根据您上传的求职要求和个人简历,我来帮您起草一封求职邮件：”这一类的内容，以便于我直接自动化复制粘贴发送。
        工作描述
        {job.detail}"""
            + """
        简历内容:
        {context}
        要求:
        {question} 
    """
        )
        question = "根据工作描述，寻找出简历里最合适的技能都有哪些?求职者的优势是什么?"
        prompt = PromptTemplate.from_template(prompt_template)
        chain = RetrievalQA.from_chain_type(
            self.model,
            retriever=vectorstore.as_retriever(),
            return_source_documents=False,
            chain_type_kwargs={"prompt": prompt},
        )
        result = chain.invoke({"query": question})
        letter = result["result"]
        return letter.replace("\n", " ")


if __name__ == "__main__":
    chatModel = ChatModel(verbose=True)
    model = chatModel.get()
    resume = Resume(model,"2024-言志伟-研发简历.pdf")
    vectorstore = resume.get_vectorstore()
    manager=JobManager()
    job = manager.get_job("ce4a6b2e5fb2719f1nV92d-9EVQ~")
    letter = resume.get_self_introduction(vectorstore, job)
    print(letter)
