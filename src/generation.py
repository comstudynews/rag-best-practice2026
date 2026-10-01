from langchain_openai import ChatOpenAI

from src.config import CHAT_MODEL, TOP_K
from src.prompts import GROUNDED_PROMPT


def build_llm():
    return ChatOpenAI(model=CHAT_MODEL, temperature=0)


def retrieve_docs(retriever, question):
    return list(retriever.invoke(question))[:TOP_K]


def build_context(docs):
    blocks = []
    for i, doc in enumerate(docs, start=1):
        doc_id = doc.metadata.get("doc_id", "unknown")
        blocks.append(f"[{i}] 문서ID={doc_id}\n{doc.page_content}")
    return "\n\n".join(blocks)


def answer_question(retriever, question, llm=None):
    docs = retrieve_docs(retriever, question)
    llm = llm or build_llm()

    prompt_value = GROUNDED_PROMPT.invoke(
        {
            "context": build_context(docs),
            "question": question,
        }
    )
    answer = llm.invoke(prompt_value).content
    return answer, docs
