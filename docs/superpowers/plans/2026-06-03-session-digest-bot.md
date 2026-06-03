# Session Digest Bot — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Streamlit app that aggregates pasted content from Email, Discord, and Web/LMS into a structured digest (key concepts + action items + deadline flags).

**Architecture:** Single-page Streamlit UI → calls `src/digest.py` → invokes LangChain ChatOpenAI (custom endpoint) → parses JSON → renders 3 sections + flags. Correction flow re-calls LLM with previous digest + new info.

**Tech Stack:** Python 3.10+, Streamlit, LangChain (`langchain-openai`), python-dotenv, pytest

---

## File Map

| File | Responsibility |
|---|---|
| `.env` | Secrets — gitignored |
| `.env.example` | Template for secrets |
| `requirements.txt` | All dependencies |
| `src/__init__.py` | Make src a package |
| `src/digest.py` | Prompt building + LLM call + JSON parsing |
| `app.py` | Streamlit UI only — no business logic |
| `tests/test_digest.py` | Unit tests for `src/digest.py` |

---

## Task 1: Project Setup

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.env`
- Create: `src/__init__.py`

- [ ] **Step 1: Create requirements.txt**

```
streamlit>=1.30.0
langchain>=0.1.0
langchain-openai>=0.0.5
python-dotenv>=1.0.0
pytest>=7.0.0
```

- [ ] **Step 2: Create .env.example**

```
CUSTOM_LLM_KEY=your-key-here
CUSTOM_LLM_URL=https://opencode.ai/zen/go/v1
CUSTOM_LLM_MODEL=deepseek-v4-flash
```

- [ ] **Step 3: Create .env với credentials thật**

```
CUSTOM_LLM_KEY=sk-MCkLdiMLeEi443oKQ3IipGBuiup7k28wpabKS3Sk3BbKwHT0w5vC7Vgjdkjkv8Xa
CUSTOM_LLM_URL=https://opencode.ai/zen/go/v1
CUSTOM_LLM_MODEL=deepseek-v4-flash
```

- [ ] **Step 4: Thêm .env vào .gitignore**

```
echo ".env" >> .gitignore
```

- [ ] **Step 5: Tạo src/__init__.py rỗng**

```bash
mkdir src
touch src/__init__.py   # Windows: type nul > src\__init__.py
```

- [ ] **Step 6: Install dependencies**

```bash
pip install -r requirements.txt
```

Expected: tất cả packages cài xong không lỗi.

- [ ] **Step 7: Commit**

```bash
git add requirements.txt .env.example .gitignore src/__init__.py
git commit -m "chore: project setup for Session Digest Bot"
```

---

## Task 2: Core Logic — `src/digest.py` (TDD)

**Files:**
- Create: `tests/test_digest.py`
- Create: `src/digest.py`

### Step 1-2: Viết tests trước

- [ ] **Step 1: Tạo tests/test_digest.py**

```python
import json
import pytest
from src.digest import build_prompt, build_correction_prompt, parse_digest


# --- build_prompt ---

def test_build_prompt_includes_date():
    _, user = build_prompt(date="2026-06-03", email="test email")
    assert "2026-06-03" in user


def test_build_prompt_includes_email():
    _, user = build_prompt(date="Day 05", email="Assignment due Friday")
    assert "Assignment due Friday" in user


def test_build_prompt_missing_channels_show_placeholder():
    _, user = build_prompt(date="Day 05", email="", discord="", web="")
    assert user.count("Không có") == 3


def test_build_prompt_includes_discord():
    _, user = build_prompt(date="Day 05", discord="Submit lab by Monday")
    assert "Submit lab by Monday" in user


def test_build_prompt_date_used_as_anchor():
    _, user = build_prompt(date="Day 05", email="some content")
    # date appears at least twice: in header and in anchor instruction
    assert user.count("Day 05") >= 2


# --- parse_digest ---

def test_parse_digest_valid_json():
    valid = json.dumps({
        "key_concepts": ["AI", "LLM"],
        "action_items": [{"task": "Nộp bài", "deadline": "2026-06-05"}],
        "flags": []
    })
    result = parse_digest(valid)
    assert result["key_concepts"] == ["AI", "LLM"]
    assert result["action_items"][0]["task"] == "Nộp bài"
    assert result["flags"] == []
    assert "parse_error" not in result


def test_parse_digest_invalid_json_returns_fallback():
    result = parse_digest("This is not JSON at all")
    assert result["parse_error"] is True
    assert result["raw"] == "This is not JSON at all"
    assert result["key_concepts"] == []
    assert result["action_items"] == []
    assert result["flags"] == []


def test_parse_digest_strips_markdown_code_block():
    wrapped = '```json\n{"key_concepts": ["test"], "action_items": [], "flags": []}\n```'
    result = parse_digest(wrapped)
    assert result["key_concepts"] == ["test"]
    assert "parse_error" not in result


def test_parse_digest_missing_fields_default_to_empty_lists():
    result = parse_digest('{"key_concepts": ["x"]}')
    assert result["action_items"] == []
    assert result["flags"] == []


# --- build_correction_prompt ---

def test_build_correction_prompt_includes_previous_json():
    prev = '{"key_concepts": ["A"], "action_items": [], "flags": []}'
    _, user = build_correction_prompt(prev, "Deadline is June 10")
    assert "June 10" in user
    assert prev in user


def test_build_correction_prompt_includes_correction_text():
    prev = '{"key_concepts": [], "action_items": [], "flags": []}'
    _, user = build_correction_prompt(prev, "Lab submission on Friday 5pm")
    assert "Lab submission on Friday 5pm" in user
```

- [ ] **Step 2: Chạy tests để xác nhận tất cả FAIL**

```bash
pytest tests/test_digest.py -v
```

Expected: `ImportError` hoặc `ModuleNotFoundError` — `src/digest.py` chưa tồn tại.

### Step 3-4: Implement

- [ ] **Step 3: Tạo src/digest.py**

```python
import json
import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
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
```

- [ ] **Step 4: Chạy tests để xác nhận tất cả PASS**

```bash
pytest tests/test_digest.py -v
```

Expected output:
```
tests/test_digest.py::test_build_prompt_includes_date PASSED
tests/test_digest.py::test_build_prompt_includes_email PASSED
tests/test_digest.py::test_build_prompt_missing_channels_show_placeholder PASSED
tests/test_digest.py::test_build_prompt_includes_discord PASSED
tests/test_digest.py::test_build_prompt_date_used_as_anchor PASSED
tests/test_digest.py::test_parse_digest_valid_json PASSED
tests/test_digest.py::test_parse_digest_invalid_json_returns_fallback PASSED
tests/test_digest.py::test_parse_digest_strips_markdown_code_block PASSED
tests/test_digest.py::test_parse_digest_missing_fields_default_to_empty_lists PASSED
tests/test_digest.py::test_build_correction_prompt_includes_previous_json PASSED
tests/test_digest.py::test_build_correction_prompt_includes_correction_text PASSED
11 passed
```

Nếu có test fail → fix `src/digest.py`, không sửa test.

- [ ] **Step 5: Commit**

```bash
git add src/digest.py tests/test_digest.py
git commit -m "feat: add digest core logic with TDD (prompt builder + parser)"
```

---

## Task 3: Streamlit UI — `app.py`

**Files:**
- Create: `app.py`

- [ ] **Step 1: Tạo app.py**

```python
import json
import streamlit as st
from src.digest import generate_digest, correct_digest

st.set_page_config(page_title="Session Digest Bot", layout="wide")
st.title("📚 Session Digest Bot")
st.caption("Gom thông tin từ Email / Discord / Web thành một bản tóm tắt duy nhất.")

# --- Input Form ---
with st.form("digest_form"):
    date = st.text_input(
        "Buổi học / ngày *",
        placeholder="ví dụ: 2026-06-03 hoặc Day 05"
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        email = st.text_area("📧 Email", height=200, placeholder="Paste nội dung email...")
    with col2:
        discord = st.text_area("💬 Discord", height=200, placeholder="Paste tin nhắn Discord...")
    with col3:
        web = st.text_area("🌐 Web / LMS", height=200, placeholder="Paste nội dung từ web trường...")
    submitted = st.form_submit_button("Generate Digest ✨", type="primary")

if submitted:
    if not date.strip():
        st.error("Vui lòng nhập ngày buổi học.")
    elif not any([email.strip(), discord.strip(), web.strip()]):
        st.error("Vui lòng paste nội dung từ ít nhất một kênh.")
    else:
        with st.spinner("Đang tạo digest..."):
            result = generate_digest(date, email, discord, web)
            st.session_state["digest"] = result
            st.session_state["digest_json_str"] = json.dumps(
                result, ensure_ascii=False, indent=2
            )

# --- Results ---
if "digest" in st.session_state:
    digest = st.session_state["digest"]

    st.divider()

    if digest.get("parse_error"):
        st.warning("⚠️ Không parse được — xem kết quả thô bên dưới.")
        st.text(digest.get("raw", ""))
    else:
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader("✅ Key Concepts")
            concepts = digest.get("key_concepts", [])
            if concepts:
                for concept in concepts:
                    st.markdown(f"- {concept}")
            else:
                st.markdown("_Không tìm thấy key concepts._")

            st.subheader("📋 Action Items")
            items = digest.get("action_items", [])
            if items:
                for item in items:
                    task = item.get("task", "")
                    deadline = item.get("deadline", "")
                    label = f"**{task}** — `{deadline}`" if deadline else f"**{task}**"
                    st.markdown(f"- {label}")
            else:
                st.markdown("_Không có action items._")

        with col_right:
            flags = digest.get("flags", [])
            if flags:
                st.subheader("⚠️ Cần làm rõ")
                for flag in flags:
                    st.warning(flag)
            else:
                st.success("Không có thông tin mơ hồ.")

    # --- Correction ---
    st.divider()
    st.subheader("💬 Thêm thông tin còn thiếu")
    correction = st.text_area(
        "Nhập thông tin bổ sung...",
        height=80,
        placeholder="ví dụ: Deadline nộp bài là 23:59 ngày 5/6"
    )
    if st.button("Cập nhật Digest 🔄"):
        if correction.strip():
            with st.spinner("Đang cập nhật..."):
                updated = correct_digest(
                    st.session_state["digest_json_str"],
                    correction
                )
                st.session_state["digest"] = updated
                st.session_state["digest_json_str"] = json.dumps(
                    updated, ensure_ascii=False, indent=2
                )
                st.rerun()
        else:
            st.warning("Vui lòng nhập thông tin bổ sung.")
```

- [ ] **Step 2: Chạy app lần đầu để kiểm tra không có import error**

```bash
streamlit run app.py
```

Expected: App mở tại `http://localhost:8501`, không có lỗi đỏ.
Nếu lỗi `ModuleNotFoundError` → kiểm tra `pip install -r requirements.txt` đã chạy chưa.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "feat: add Streamlit UI for Session Digest Bot"
```

---

## Task 4: Test 4 Paths với Real Data

**Files:** Không tạo file mới — chạy app với data thật.

Mở `http://localhost:8501` và test từng path theo thứ tự.

- [ ] **Step 1: Happy Path**

Paste content rõ ràng vào cả 3 kênh. Ví dụ:

```
Email:    "Subject: Day 05 Lab — hạn nộp bài là 23:59 ngày 04/06/2026"
Discord:  "Nhớ nộp thin SPEC trước 11pm tối nay. File để trong repo cá nhân."
Web/LMS:  "Day 05: Lab kickoff. Xem README để biết cấu trúc repo nộp bài."
```

Expected: Digest hiển thị key concepts, action items với deadline rõ, flags rỗng (banner xanh "Không có thông tin mơ hồ").

- [ ] **Step 2: Low-confidence Path**

Paste content có deadline mơ hồ:

```
Discord: "Nộp bài sớm nhé mọi người"
Email:   "Nhắc nhở: hoàn thành lab trước cuối tuần"
```

Expected: `flags` không rỗng, banner ⚠️ xuất hiện với câu hỏi cụ thể về deadline.

- [ ] **Step 3: Correction Path**

Sau khi có digest từ Step 2, nhập vào correction box:

```
Deadline cụ thể là 23:59 ngày 05/06/2026
```

Bấm "Cập nhật Digest".
Expected: `action_items` cập nhật deadline, flags về deadline đó biến mất.

- [ ] **Step 4: Failure Path (parse_error)**

Không có cách force LLM trả về non-JSON trực tiếp — test bằng cách mock hoặc quan sát nếu LLM tự nhiên trả lỗi format. Để simulate:

Mở `src/digest.py`, tạm thời thay `_call_llm` để trả về plain text:

```python
def _call_llm(system_prompt, user_prompt):
    return "Đây là kết quả không phải JSON"
```

Chạy lại app → Expected: banner vàng "Không parse được" + raw text hiển thị.
Sau khi test xong → revert thay đổi này:

```bash
git checkout src/digest.py
```

- [ ] **Step 5: Screenshot 4 paths**

Chụp màn hình 4 states: happy, low-confidence, correction, parse_error fallback.
Lưu vào `docs/screenshots/` để dùng trong demo.

```bash
mkdir -p docs/screenshots
# Lưu screenshots vào đây
git add docs/screenshots/
git commit -m "test: 4-path manual test screenshots"
```

---

## Task 5: README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Tạo README.md**

```markdown
# Session Digest Bot

Gom thông tin từ Email, Discord, Web/LMS thành một digest có cấu trúc sau mỗi buổi học.

## Setup

1. Clone repo
2. `pip install -r requirements.txt`
3. Copy `.env.example` → `.env` và điền credentials
4. `streamlit run app.py`

## Cách dùng

1. Nhập tên/ngày buổi học
2. Paste nội dung từ Email / Discord / Web (ít nhất 1 kênh)
3. Bấm **Generate Digest**
4. Nếu có flag ⚠️ → kiểm tra và bổ sung thông tin
5. Bổ sung vào ô bên dưới → **Cập nhật Digest**

## 4 Paths

| Path | Cách test |
|---|---|
| Happy | Paste content đủ rõ 3 kênh |
| Low-confidence | Paste deadline mơ hồ ("nộp sớm") |
| Correction | Sau low-confidence, nhập deadline cụ thể vào correction box |
| Failure | LLM trả về non-JSON → raw text fallback hiển thị |
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with setup and 4-path test guide"
```

---

## Checklist cuối

- [ ] `pytest tests/test_digest.py` → 11 passed, 0 failed
- [ ] `streamlit run app.py` → app chạy không lỗi
- [ ] Happy path demo được bằng real data từ lớp
- [ ] Low-confidence path hiển thị flag ⚠️
- [ ] Correction path cập nhật digest đúng
- [ ] Failure fallback hiển thị raw text thay vì crash
- [ ] Screenshots 4 paths trong `docs/screenshots/`
