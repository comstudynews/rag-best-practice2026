"""RAG Evaluation Template"""

questions = [
    "제품 설치 방법은 무엇인가?",
    "오류 코드 DEMO-001 해결 방법은?",
    "문서에 없는 질문 테스트"
]


def evaluate_answer(question, answer, context):
    """Retrieval과 Generation 평가 기준 예시"""
    return {
        "question": question,
        "has_context": bool(context),
        "answer": answer,
    }


if __name__ == "__main__":
    for q in questions:
        print(evaluate_answer(q, "sample answer", "sample context"))
