import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from pypdf import PdfReader
from docx import Document
from dotenv import load_dotenv

load_dotenv()

MAX_DOC_CHARS = 50_000

SYSTEM_PROMPT = (
    "Bạn là AI Tutor cho khoá AI thực chiến (LLM, LangChain, Agents, RAG, Python).\n"
    "Khi giải thích, luôn theo cấu trúc:\n"
    "1. Giải thích ngắn gọn\n"
    "2. Ví dụ code cụ thể (nếu áp dụng)\n"
    "3. Câu hỏi kiểm tra hiểu: \"Bạn có thể giải thích lại... không?\"\n"
    "Nếu câu hỏi mơ hồ → hỏi lại: \"Bạn đang bị stuck ở điểm nào cụ thể?\" trước khi giải thích.\n"
    "Trả lời bằng tiếng Việt. Dùng code block khi có code."
)


def extract_text(file) -> str:
    name = file.name.lower()
    if name.endswith(".pdf"):
        reader = PdfReader(file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif name.endswith(".docx"):
        doc = Document(file)
        text = "\n".join(p.text for p in doc.paragraphs)
    elif name.endswith(".txt"):
        text = file.read().decode("utf-8", errors="replace")
    else:
        raise ValueError(f"Unsupported file type: {file.name}")
    return text[:MAX_DOC_CHARS]


def build_prompt(doc_context: str, history: list, question: str) -> tuple:
    system = SYSTEM_PROMPT
    if doc_context:
        system += f"\n\nTài liệu buổi học:\n{doc_context}"

    lines = []
    for msg in history:
        role = "Học viên" if msg["role"] == "user" else "AI Tutor"
        lines.append(f"{role}: {msg['content']}")
    lines.append(f"Học viên: {question}")

    return system, "\n".join(lines)


def _get_llm():
    return ChatOpenAI(
        model=os.getenv("CUSTOM_LLM_MODEL", "deepseek-v4-flash"),
        openai_api_key=os.getenv("CUSTOM_LLM_KEY"),
        openai_api_base=os.getenv("CUSTOM_LLM_URL"),
        temperature=0.3,
    )


def _call_llm(system_prompt: str, user_prompt: str) -> str:
    llm = _get_llm()
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    return llm.invoke(messages).content


def chat(doc_context: str, history: list, question: str) -> str:
    system, user_prompt = build_prompt(doc_context, history, question)
    return _call_llm(system, user_prompt)
