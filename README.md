# Session Digest Bot

Gom thông tin từ Email, Discord, Web/LMS thành một digest có cấu trúc sau mỗi buổi học.

**Track:** A — Learning OS | **Hackathon:** Batch 02 Day 06

## Setup

1. Clone repo
2. `pip install -r requirements.txt`
3. Copy `.env.example` → `.env` và điền credentials
4. `streamlit run app.py`

App mở tại `http://localhost:8501`

## Cách dùng

1. Nhập tên/ngày buổi học (bắt buộc)
2. Paste nội dung từ Email / Discord / Web (ít nhất 1 kênh)
3. Bấm **Generate Digest ✨**
4. Nếu có flag ⚠️ → deadline hoặc thông tin chưa rõ, cần làm rõ
5. Bổ sung vào ô bên dưới → **Cập nhật Digest 🔄**

## 4 Paths

| Path | Cách test |
|---|---|
| Happy | Paste content đủ rõ từ 3 kênh — digest sạch, không flag |
| Low-confidence | Paste deadline mơ hồ ("nộp sớm") — flag ⚠️ xuất hiện |
| Correction | Sau low-confidence, nhập deadline cụ thể → digest cập nhật |
| Failure | LLM trả về non-JSON → raw text fallback, không crash |

## Architecture

```
User paste (Email/Discord/Web)
  → src/digest.py (build_prompt → LangChain → parse JSON)
  → app.py (Streamlit UI + session state)
```

**LLM:** DeepSeek via custom OpenAI-compatible endpoint (LangChain)
