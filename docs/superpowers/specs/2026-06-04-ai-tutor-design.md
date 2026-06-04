# Design — AI Tutor (In-Class Learning Assistant)

**Date:** 2026-06-04  
**Track:** A - Learning OS  
**Replaces:** Session Digest Bot (`src/digest.py`, `app.py`)

---

## 1. Problem

Học viên trong buổi học live (hoặc review sau buổi học) gặp khái niệm chưa hiểu nhưng không có chỗ hỏi ngay — hỏi to làm gián đoạn lớp, hỏi ChatGPT thì không có context bài học. Cần một tutor AI biết ngữ cảnh khoá học và trả lời có cấu trúc.

---

## 2. User

Học viên Batch 02 AI thực chiến, dùng app:
- **Trong giờ học:** hỏi nhanh khi không hiểu, không cần gián đoạn thầy
- **Sau giờ học:** review lại tài liệu, hỏi sâu hơn về phần chưa rõ

---

## 3. Architecture

```
app.py          — Streamlit UI: sidebar (file upload) + main (chat)
src/tutor.py    — core logic: file extractor, prompt builder, LLM call
tests/test_tutor.py — unit tests
```

Không dùng RAG / vector store. Document text inject thẳng vào prompt context.

---

## 4. UI Layout — Sidebar + Chat (Layout B)

```
┌─────────────────┬────────────────────────────────┐
│  📚 Tài liệu    │  💬 Chat với AI Tutor           │
│                 │                                 │
│  [Kéo thả file] │  🤖 Xin chào! Bạn đang stuck   │
│                 │     ở phần nào?                 │
│  ✅ slides.pdf  │                                 │
│  32 trang · đã  │  🧑 LangChain là gì?            │
│  đọc            │                                 │
│                 │  🤖 Giải thích: ...             │
│  📖 Chủ đề:     │     Ví dụ: ChatOpenAI(...)      │
│  LangChain,     │     Kiểm tra: Bạn có thể...?   │
│  Agents, RAG    │                                 │
│                 │  [Gõ câu hỏi...        ] [Gửi] │
└─────────────────┴────────────────────────────────┘
```

---

## 5. Input Methods (3 loại)

| Input | Cách dùng |
|---|---|
| Free-text | Gõ câu hỏi trực tiếp vào chat input |
| Paste context | Paste đoạn slide/note vào chat rồi hỏi về nó |
| Upload file | Upload PDF/DOCX/TXT qua sidebar → AI đọc toàn bộ |

---

## 6. Prompt Design

```
SYSTEM:
Bạn là AI Tutor cho khoá AI thực chiến (LLM, LangChain, Agents, RAG, Python).
Khi giải thích, luôn theo cấu trúc:
  1. Giải thích ngắn gọn
  2. Ví dụ code cụ thể (nếu áp dụng)
  3. Câu hỏi kiểm tra hiểu: "Bạn có thể giải thích lại... không?"
Nếu câu hỏi mơ hồ → hỏi lại: "Bạn đang bị stuck ở điểm nào cụ thể?" trước khi giải thích.
Trả lời bằng tiếng Việt. Dùng code block khi có code.

[DOCUMENT CONTEXT - chỉ khi có file upload]
Tài liệu buổi học:
{doc_text}

[CHAT HISTORY]
{history}

USER: {question}
```

Adaptive logic nằm hoàn toàn trong system prompt — không cần code riêng.

---

## 7. Data Flow

```
Upload file
  → extract_text(file) → plain text
  → truncate nếu > 50,000 ký tự (thông báo user)
  → lưu vào st.session_state["doc_context"]
  → reset st.session_state["chat_history"] = []

Chat input
  → build_prompt(doc_context, chat_history, question)
  → _call_llm(system, user_prompt)
  → append (question, answer) vào chat_history
  → render với st.chat_message
```

---

## 8. src/tutor.py — Public API

```python
def extract_text(file) -> str:
    # Đọc PDF / DOCX / TXT, trả về plain text
    # Truncate ở 50,000 ký tự nếu quá dài

def build_prompt(doc_context: str, history: list, question: str) -> tuple[str, str]:
    # Trả về (system_prompt, user_prompt)

def chat(doc_context: str, history: list, question: str) -> str:
    # Gọi LLM, trả về answer string
```

---

## 9. Session State

| Key | Giá trị | Reset khi |
|---|---|---|
| `doc_context` | plain text từ file upload | Upload file mới |
| `doc_name` | tên file | Upload file mới |
| `chat_history` | list of `{"role": "user"/"assistant", "content": str}` | Upload file mới |

---

## 10. Error Handling

| Tình huống | Xử lý |
|---|---|
| File không đọc được | `st.warning(...)`, cho phép chat không có context |
| File > 50k ký tự | Truncate + `st.info("Chỉ đọc được X trang đầu")` |
| LLM fail / timeout | `st.error(...)`, giữ nguyên chat history, cho retry |
| Chat input rỗng | Không gửi |

---

## 11. Tests (src/tutor.py)

- `test_extract_text_pdf` — đọc được text từ PDF
- `test_extract_text_truncates_long_file` — file > 50k ký tự bị truncate
- `test_extract_text_unknown_format` — file không hỗ trợ → raise ValueError
- `test_build_prompt_includes_question` — question có trong user_prompt
- `test_build_prompt_includes_doc_context` — doc_context có trong prompt khi được cung cấp
- `test_build_prompt_no_doc_context` — không có "DOCUMENT CONTEXT" khi doc_context rỗng
- `test_build_prompt_includes_history` — history được format đúng

---

## 12. Dependencies mới cần thêm

```
pypdf>=3.0.0       # đọc PDF
python-docx>=0.8.11  # đọc DOCX
```

TXT đọc bằng built-in Python, không cần thêm package.

---

## 14. LLM Provider (thực tế triển khai)

Cấu hình qua `.env` — không hardcode trong code:

| Biến | Giá trị mặc định | Ghi chú |
|---|---|---|
| `CUSTOM_LLM_KEY` | Groq API key | Free tier đủ dùng |
| `CUSTOM_LLM_URL` | `https://api.groq.com/openai/v1` | OpenAI-compatible |
| `CUSTOM_LLM_MODEL` | `llama-3.3-70b-versatile` | ~1-2s response time |

Ban đầu dùng Ollama `qwen3.5:9b` local nhưng chạy chủ yếu trên CPU (~400s/request). Chuyển sang Groq giải quyết hoàn toàn vấn đề tốc độ.

---

## 15. Testing Results (thực tế)

3 paths đã test end-to-end:

| Path | Input | Expected | Kết quả |
|---|---|---|---|
| Happy path | "LangChain là gì?" | 3-phần có structured answer | ✅ Pass |
| Adaptive | "Tôi không hiểu" | AI hỏi lại "stuck ở đâu?" | ✅ Pass |
| File upload | Upload `.txt` → hỏi về nội dung | AI dùng file context | ✅ Pass |

---

## 13. Out of Scope

- RAG / vector store / embeddings
- Lưu lịch sử chat qua session (database)
- Multi-user / authentication
- Hỗ trợ môn học ngoài AI curriculum
