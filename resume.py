import spacy
import torch
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_huggingface import HuggingFaceEmbeddings

from curd.job_curd import get_job
from llm.chatModel import ChatModel


class Resume(object):
    def __init__(self, model: BaseChatModel):
        self.model = model

    def read_resume(self):
        loader = DirectoryLoader("./resume", glob="*.pdf", loader_cls=PyPDFLoader)
        pdf_pages = loader.load()
        resume_text = ""
        for page in pdf_pages:
            # print(page.metadata.get('source'))

            page_text = page.page_content
            resume_text += page_text

        return resume_text

    def get_vectorstore(self, resume_text: str):
        # text_splitter = CharacterTextSplitter(
        #     separator="\n", chunk_size=100, chunk_overlap=30, length_function=len
        # )
        # text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
        nlp = spacy.load("zh_core_web_sm")
        chunks = nlp(resume_text)
        for ent in chunks.ents:
            print(ent.text, ent.label_)
        sentences = [sent.text for sent in chunks.sents]
        EMBEDDING_DEVICE = (
            "cuda"
            if torch.cuda.is_available()
            else "mps" if torch.backends.mps.is_available() else "cpu"
        )
        # chunks = text_splitter.split_text(resume_text)
        embeddings = HuggingFaceEmbeddings(
            model_name="GanymedeNil/text2vec-large-chinese",
            model_kwargs={"device": EMBEDDING_DEVICE},
        )
        vectorstore = FAISS.from_texts(texts=sentences, embedding=embeddings)
        return vectorstore

    def get_self_introduction(
        self, vectorstore, job_description: str, character_limit: int = 300
    ) -> str:
        prompt_template = (
            f"""
        你将扮演一位求职者的角色,根据上下文里的简历内容以及应聘工作的描述,来直接给HR写一个礼貌专业, 且字数严格限制在{character_limit}以内的求职消息,要求根据简历内容中专业技能，工作经验，项目经验来结合应聘工作的描述,来阐述自己的优势,尽最大可能打动招聘者。始终使用中文来进行消息的编写。开头是招聘负责人,这是一份求职消息，不要包含简历内容以外的技术的东西，专业技能和经验，不要引用简历内容，如果招聘要求技能在简历内容中不存在则忽略。
        工作描述
        {job_description}"""
            + """
        简历内容:
        {context}
        招聘要求:
        {question} 
    """
        )
        question = "根据工作描述，寻找出简历里最合适的技能都有哪些?求职者的优势是什么?"
        prompt = PromptTemplate.from_template(prompt_template)
        chain = RetrievalQA.from_chain_type(
            self.model,
            retriever=vectorstore.as_retriever(),
            # return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )
        result = chain.invoke({"query": question})
        letter = result["result"]
        return letter


if __name__ == "__main__":
    chatModel = ChatModel(verbose=True)
    model = chatModel.get()
    resume = Resume(model)
    resume_text = resume.read_resume()
    vectorstore = resume.get_vectorstore(resume_text)
    job = get_job("7412caa0a7a94cd41HJ92dy1FFNX")
    letter = resume.get_self_introduction(vectorstore, job.detail)
    print(letter)
