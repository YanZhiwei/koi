import faiss
from text2vec import SentenceModel

if __name__ == "__main__":
    sentences = [
        "如何更换花呗绑定银行卡",
        "花呗更改绑定银行卡",
        "怎么换银行卡",
        "银行卡毁坏如何补办",
        "花呗如何打开",
    ]

    model = SentenceModel("GanymedeNil/text2vec-large-chinese")
    embeddings = model.encode(sentences)
    if embeddings.dtype != "float32":
        embeddings = embeddings.astype("float32")
    else:
        pass

    num, d = embeddings.shape
    index = faiss.IndexFlatL2(d)
    print(index.is_trained)
    index.add(embeddings)
    print(index.ntotal)
