from langchain_classic.retrievers.ensemble import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from src.config import EMBEDDING_MODEL, TOP_K


def build_retrievers(chunks):
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    baseline = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )

    dense = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )

    sparse = BM25Retriever.from_documents(chunks)
    sparse.k = TOP_K

    improved = EnsembleRetriever(
        retrievers=[dense, sparse],
        weights=[0.6, 0.4],
    )

    return baseline, improved
