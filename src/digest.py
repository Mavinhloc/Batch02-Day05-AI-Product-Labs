import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = (
    "Bạn là trợ lý học tập. Nhận nội dung từ nhiều kênh thông tin "
    "(email, Discord, web), hãy trích xuất và tổng hợp thành digest có cấu trúc. "
    "Trả về JSON hợp lệ, không giải thích thêm. "
    "Nếu deadline không rõ → đưa vào flags, không tự bịa ngày."
)

_USER_TEMPLATE = """Buổi học ngày: {date}

Kênh Email:
{email}

Kênh Discord:
{discord}

Kênh Web/LMS:
{web}

Trả về JSON theo format sau (không thêm gì ngoài JSON):
{{
  "key_concepts": ["khái niệm 1", "khái niệm 2"],
  "action_items": [{{"task": "tên task", "deadline": "ngày hoặc mô tả"}}],
  "flags": ["nội dung mơ hồ cần hỏi lại"]
}}

Chỉ lấy thông tin liên quan đến buổi học ngày {date}."""

_CORRECTION_TEMPLATE = """Digest trước:
{previous_json}

Thông tin bổ sung từ user:
{correction}

Cập nhật digest, giữ nguyên phần đúng. Trả về JSON cùng format, không thêm gì ngoài JSON:
{{
  "key_concepts": [...],
  "action_items": [...],
  "flags": [...]
}}"""


def build_prompt(date: str, email: str = "", discord: str = "", web: str = "") -> tuple:
    user_content = _USER_TEMPLATE.format(
        date=date,
        email=email or "Không có",
        discord=discord or "Không có",
        web=web or "Không có",
    )
    return SYSTEM_PROMPT, user_content


def build_correction_prompt(previous_json_str: str, correction: str) -> tuple:
    user_content = _CORRECTION_TEMPLATE.format(
        previous_json=previous_json_str,
        correction=correction,
    )
    return SYSTEM_PROMPT, user_content


def parse_digest(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        inner = lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
        text = "\n".join(inner).strip()
    try:
        data = json.loads(text)
        data.setdefault("key_concepts", [])
        data.setdefault("action_items", [])
        data.setdefault("flags", [])
        if not isinstance(data["key_concepts"], list):
            data["key_concepts"] = []
        if not isinstance(data["action_items"], list):
            data["action_items"] = []
        if not isinstance(data["flags"], list):
            data["flags"] = []
        return data
    except (json.JSONDecodeError, AttributeError):
        return {"raw": text, "parse_error": True, "key_concepts": [], "action_items": [], "flags": []}


def _get_llm():
    return ChatOpenAI(
        model=os.getenv("CUSTOM_LLM_MODEL", "deepseek-v4-flash"),
        openai_api_key=os.getenv("CUSTOM_LLM_KEY"),
        openai_api_base=os.getenv("CUSTOM_LLM_URL"),
        temperature=0,
    )


def _call_llm(system_prompt: str, user_prompt: str) -> str:
    llm = _get_llm()
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    return llm.invoke(messages).content


def generate_digest(date: str, email: str = "", discord: str = "", web: str = "") -> dict:
    system_prompt, user_prompt = build_prompt(date, email, discord, web)
    raw = _call_llm(system_prompt, user_prompt)
    return parse_digest(raw)


def correct_digest(previous_json_str: str, correction: str) -> dict:
    system_prompt, user_prompt = build_correction_prompt(previous_json_str, correction)
    raw = _call_llm(system_prompt, user_prompt)
    return parse_digest(raw)
