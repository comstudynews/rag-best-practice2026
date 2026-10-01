from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import KNOWLEDGE_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def load_knowledge() -> list[Document]:
    docs: list[Document] = []

    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        loaded = TextLoader(str(path), encoding="utf-8").load()

        for doc in loaded:
            doc.metadata["doc_id"] = path.stem
            doc.metadata["source"] = path.name

        docs.extend(loaded)

    if not docs:
        raise RuntimeError(f"문서를 찾을 수 없습니다: {KNOWLEDGE_DIR}")

    return docs


def split_knowledge(docs: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(docs)
