# Thin SPEC — AI Tutor (In-Class Learning Assistant)

## 1. Track, product/app và user

**Track:** A - Learning OS: AI cho giáo dục, LMS, trợ lý học tập  
**Product/app thật:** AI Tutor — trợ lý học tập AI giải thích khái niệm khoá học ngay khi học viên bị stuck  
**User cụ thể:** Học viên Batch 02 AI thực chiến, đang ngồi trong lớp học live (hoặc review sau buổi học) gặp khái niệm chưa hiểu, muốn hỏi ngay mà không phải gián đoạn thầy hoặc chờ đến cuối buổi.

**Nhóm có phải user thật không?**  
Có — toàn bộ nhóm đang học Batch 02, trải nghiệm đúng pain này trong mỗi buổi lab.

## 2. Evidence summary

| Evidence | Nguồn | User/pain nói lên điều gì? | SPEC phải đổi gì? |
|---|---|---|---|
| Không dám hỏi trong giờ vì sợ gián đoạn lớp | Phỏng vấn 2 bạn cùng lớp | Rào cản xã hội → câu hỏi bị giữ lại, không được giải đáp ngay | App phải riêng tư, instant — không cần giơ tay hay chờ |
| ChatGPT giải thích không match nội dung đang học | Self-use test | Thiếu context khoá học → giải thích lạc đề | AI phải biết curriculum (LLM, LangChain, Agents, RAG) và có thể nhận tài liệu buổi học |
| Bị stuck ở code example trên slide, thầy giảng qua nhanh | Quan sát trực tiếp | Cần giải thích chậm lại + ví dụ riêng | Output phải có code block cụ thể, không chỉ text abstract |
| Câu hỏi mơ hồ ("Tôi không hiểu") → AI đoán sai | Self-use test với ChatGPT | AI giải thích không đúng vấn đề học viên thật sự hỏi | AI phải hỏi lại khi câu hỏi mơ hồ trước khi giải thích |

## 3. Pain statement

```text
Học viên đang học live session (hoặc review sau buổi) gặp khó ở bước "hiểu được khái niệm đang học",
vì không có chỗ hỏi phù hợp — hỏi thầy thì gián đoạn lớp, hỏi ChatGPT thì thiếu context khoá học,
dẫn tới:
- Câu hỏi bị giữ lại → tích lũy confusion qua nhiều buổi.
- AI giải thích lạc đề → học viên hiểu sai hoặc mất thêm thời gian filter.
- Code examples không được giải thích đủ → stuck khi tự làm lab.
Bằng chứng chính là: 2 bạn cùng lớp xác nhận không hỏi vì sợ gián đoạn + self-use test ChatGPT không biết context khoá học.
```

## 4. Build slice

```text
Cho học viên Batch 02 đang bị stuck ở khái niệm trong lớp học live hoặc khi review,
prototype sẽ dùng AI để nhận câu hỏi tự do (gõ, paste) hoặc tài liệu buổi học (upload PDF/DOCX/TXT),
tạo ra giải thích có cấu trúc gồm:
- Giải thích ngắn gọn: định nghĩa / khái niệm cốt lõi
- Ví dụ code cụ thể: code block với syntax highlight (nếu applicable)
- Câu hỏi kiểm tra hiểu: "Bạn có thể giải thích lại... không?"
Và xử lý adaptive path bằng cách hỏi lại khi câu hỏi mơ hồ — "Bạn đang bị stuck ở điểm nào cụ thể?" — thay vì đoán mò.
```

## 5. Auto/Aug decision

- [x] **Augmentation:** AI gợi ý/draft/phân loại, user quyết cuối.
- [ ] **Conditional automation:** AI tự làm trong case hẹp; case mơ hồ/rủi ro chuyển người.
- [ ] **Automation:** AI tự quyết và tự hành động.

**Lý do chọn Augmentation:**  
Giải thích sai khái niệm AI/LLM → học viên hiểu sai cả chương → hậu quả tích lũy. AI cần học viên đọc và verify output trước khi internalize. Học viên vẫn là người quyết định "mình đã hiểu hay chưa".

**Human role:** learner (đọc, hỏi follow-up, tự xác nhận đã hiểu) + corrector (hỏi lại nếu giải thích chưa đúng)

## 6. Four paths

| Path | Prototype phải thể hiện gì? |
|---|---|
| **Happy** | Gõ câu hỏi rõ ("LangChain là gì?") → AI trả 3-phần đầy đủ: giải thích ngắn + code block + câu hỏi kiểm tra. Response trong ~2s. |
| **Adaptive** | Gõ câu hỏi mơ hồ ("Tôi không hiểu") → AI hỏi lại: "Bạn đang bị stuck ở điểm nào cụ thể?" thay vì đoán mò giải thích. |
| **File upload** | Upload file tài liệu buổi học (PDF/DOCX/TXT) → Sidebar xác nhận ✅ + ký tự đã đọc → hỏi về nội dung file → AI trả lời đúng context tài liệu. |
| **Error** | Upload file không hỗ trợ (ví dụ .pptx) → App hiển thị thông báo lỗi rõ ràng, không crash, vẫn cho phép chat không có context. |

## 7. Failure mode nguy hiểm nhất

```text
Nếu AI giải thích sai một khái niệm cốt lõi (ví dụ định nghĩa sai về RAG hay Agent),
học viên tin vào và internalize cái sai,
hậu quả là hiểu sai tích lũy → các bài lab sau ngày càng khó tiếp thu.

Prototype xử lý bằng:
1. System prompt inject curriculum scope rõ ràng — AI được "anchor" vào khoá AI thực chiến.
2. Structured output bắt buộc có ví dụ code cụ thể — dễ verify hơn là text abstract.
3. Câu hỏi kiểm tra hiểu cuối mỗi response — học viên tự xác nhận trước khi move on.
4. Adaptive path: khi câu hỏi mơ hồ, hỏi lại để giải thích đúng vấn đề, tránh giải thích trật.

Owner kiểm thử path này: người build prototype — test với câu hỏi có/không có context file.
```

## 8. Owner plan cho Day 06

| Thành viên | Việc phụ trách | Bằng chứng cần có trong repo |
|---|---|---|
| Dev | `src/tutor.py` — extract_text + build_prompt + chat() | File + 13 unit tests passing |
| Dev | `app.py` — Streamlit UI (sidebar upload + chat interface) | App chạy tại localhost:8501 |
| Dev | Test 3 paths với real interaction | Screenshot 3 paths |
| Dev | `demo-slides.html` — slide thuyết trình demo round | File trong repo |
| All | Demo script (3 paths: happy, adaptive, file upload) | Demo chạy được trong 3 phút |
