# Design — Session Digest Bot

**Track:** A — Learning OS  
**Date:** 2026-06-03  
**Team:** 1-2 người, tự code (Python + LangChain)

---

## 1. Problem

**Pain statement:**
```
Học viên vừa xong buổi live session đang bị ngợp bởi thông tin
rải rác trên 3 kênh (Email, Discord, Web/LMS),
vì không có nơi tổng hợp duy nhất,
dẫn tới miss action items hoặc deadline quan trọng.
Bằng chứng: trải nghiệm trực tiếp của người dùng trong lớp học này.
```

---

## 2. Build Slice

```
Cho học viên vừa xong buổi live session,
prototype dùng AI để nhận paste content từ 3 kênh (Email/Discord/Web),
tạo ra digest cấu trúc gồm key concepts + action items + deadlines,
và xử lý thông tin mơ hồ bằng cách flag thay vì tự bịa.
```

---

## 3. Auto/Aug Decision

- **Augmentation:** AI draft digest, user verify và correct.
- **Human role:** reviewer + corrector
- **Lý do:** Deadline và action items sai có thể gây hậu quả thật (miss nộp bài). AI không được tự quyết — chỉ đề xuất.

---

## 4. Architecture

### Components

```
UI:      Streamlit
LLM:     LangChain (langchain_openai.ChatOpenAI) → custom endpoint
Config:  .env (CUSTOM_LLM_KEY, CUSTOM_LLM_URL, CUSTOM_LLM_MODEL)
Data:    User paste thủ công từ Email / Discord / Web
```

### UI Layout

```
┌─────────────────────────────────────────┐
│  Session Digest Bot                     │
│  Buổi học / ngày: [____________]  ←required
├─────────────────────────────────────────┤
│  [Email]    text_area (optional)        │
│  [Discord]  text_area (optional)        │
│  [Web/LMS]  text_area (optional)        │
│                                         │
│  [  Generate Digest  ]                  │
├─────────────────────────────────────────┤
│  ✅ Key Concepts     (list)             │
│  📋 Action Items     (task + deadline)  │
│  ⚠️  Flags           (low-confidence)   │
│                                         │
│  [Thêm thông tin còn thiếu...]          │
└─────────────────────────────────────────┘
```

### Data Flow

```
User nhập ngày + paste content từ 1-3 kênh
        ↓
build_prompt(date, email, discord, web)
        ↓
ChatOpenAI → custom endpoint (deepseek-v4-flash)
        ↓
Parse JSON output
        ↓
Render: key_concepts + action_items + flags
        ↓ (nếu user nhập correction)
Re-call LLM với digest cũ + correction text
        ↓
Re-render digest đã cập nhật
```

---

## 5. Prompt Design

**System prompt:**
```
Bạn là trợ lý học tập. Nhận nội dung từ nhiều kênh thông tin
(email, Discord, web), hãy trích xuất và tổng hợp thành digest
có cấu trúc. Trả về JSON hợp lệ, không giải thích thêm.
Nếu deadline không rõ → đưa vào flags, không tự bịa ngày.
```

**User prompt template:**
```
Buổi học ngày: {date}

Kênh Email:
{email_content or "Không có"}

Kênh Discord:
{discord_content or "Không có"}

Kênh Web/LMS:
{web_content or "Không có"}

Trả về JSON:
{
  "key_concepts": ["..."],
  "action_items": [{"task": "...", "deadline": "..."}],
  "flags": ["nội dung mơ hồ cần hỏi lại..."]
}
```

**JSON parse fallback:** Nếu LLM trả về text không phải JSON hợp lệ → hiển thị raw text trong UI thay vì crash, kèm message "Không parse được — xem kết quả thô bên dưới".

**Correction prompt:**
```
Digest trước: {previous_json}
Thông tin bổ sung từ user: {correction_text}
Cập nhật digest, giữ nguyên phần đúng. Trả về JSON cùng format.
```

---

## 6. Four Paths

| Path | Trigger | AI output | UI |
|---|---|---|---|
| Happy | Content đủ rõ | JSON đầy đủ, flags rỗng | 3 sections sạch |
| Low-confidence | Deadline mơ hồ ("nộp sớm") | `flags: ["Discord: deadline chưa rõ"]` | Banner ⚠️ kèm câu hỏi |
| Failure | AI miss action item hoặc nhầm kênh | Output thiếu/sai | User nhập correction → re-call |
| Correction | User thêm thông tin | LLM merge vào digest cũ | Re-render digest cập nhật |

---

## 7. Failure Mode Nguy Hiểm Nhất

```
Nếu user paste nội dung từ nhiều buổi học khác nhau,
AI có thể trộn deadline buổi cũ vào action items buổi mới,
hậu quả là học viên miss deadline thật.

Mitigation:
→ Field "Buổi học / ngày" bắt buộc nhập ở đầu form
→ Prompt inject ngày đó làm anchor: "Chỉ lấy thông tin liên quan đến buổi [ngày]"
Owner kiểm thử path này: người code prototype.
```

---

## 8. Owner Plan (Day 06)

| Thành viên | Việc | Output |
|---|---|---|
| Dev | Setup .env + LangChain client | `src/llm_client.py` |
| Dev | Prompt builder + JSON parser | `src/digest.py` |
| Dev | Streamlit UI (form + render) | `app.py` |
| Dev | Test 4 paths với real data từ lớp | screenshot 4 paths |
| Dev | Demo script | `README.md` với hướng dẫn chạy |

---

## 9. Real Data Plan

- **Email:** Forward email thông báo lớp vào text area
- **Discord:** Copy messages từ channel lớp học
- **Web/LMS:** Copy nội dung bài đăng trên portal/web trường

Không cần scraping — paste thủ công là đủ cho prototype.
