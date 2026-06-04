# Evidence Pack — AI Tutor (In-Class Learning Assistant)

## 1. Nhóm và track

**Tên nhóm:** Học chăm  
**Track:** A - Learning OS: AI cho giáo dục, LMS, trợ lý học tập  
**Product/app đã chọn:** AI Tutor — trợ lý học tập AI hỗ trợ học viên giải thích khái niệm ngay trong lớp  
**Build slice đang nghĩ:** Học viên gõ câu hỏi (hoặc upload tài liệu buổi học) → AI giải thích có cấu trúc (giải thích ngắn + code + câu hỏi kiểm tra), adaptive khi câu hỏi mơ hồ

## 2. Self-use evidence

| Observation | Screenshot/link | Path liên quan | Điều học được |
|---|---|---|---|
| Trong buổi lab Day 05, có khái niệm về LangChain chain không rõ — muốn hỏi nhưng thầy đang giảng phần khác. | Trải nghiệm trực tiếp Batch 02 | Failure | Học viên giữ câu hỏi lại, đến cuối buổi quên hoặc mất cơ hội hỏi. |
| Thử hỏi ChatGPT về LangChain — AI giải thích đúng về mặt kỹ thuật nhưng không biết lớp đang dùng version nào, pattern nào. | Self-use test | Low-confidence | ChatGPT không có context khoá học → giải thích lạc đề so với nội dung thầy dạy. |
| Bạn cùng nhóm hỏi: "Agents khác Chain thế nào?" sau buổi học — câu hỏi thật, không có chỗ hỏi phù hợp ngay lúc đó. | Quan sát trực tiếp trong lớp | Failure | Câu hỏi "nhỏ" không được giải đáp tích lũy thành confusion lớn. |

## 3. User / review / social evidence

| Quote / review / observation | Nguồn | User là ai? | Pain/failure mode |
|---|---|---|---|
| "Mình không dám hỏi vì sợ làm mất thời gian của cả lớp, toàn đợi ra ngoài hỏi bạn." | Phỏng vấn nhanh 2 bạn cùng lớp | Học viên Batch 02, 19-22 tuổi | Rào cản xã hội → câu hỏi không được giải đáp ngay |
| "ChatGPT giải thích đúng nhưng không biết đang học đến phần gì, giải thích từ đầu mà mình cần hiểu phần nâng cao hơn." | Quan sát trực tiếp khi bạn dùng ChatGPT trong giờ | Học viên đang học LangChain | AI không có context khoá học → giải thích không match trình độ / nội dung |
| "Mình hay bị stuck ở code example — thầy show nhanh trên slide, không kịp hiểu." | Nói chuyện nhóm trước giờ học | Học viên học live session | Code examples trên slide không có giải thích đủ chậm |

## 4. Competitor / analog evidence

| App / mô hình tham khảo | Họ xử lý task này thế nào? | Pattern học được | Có áp dụng trong 1 ngày không? |
|---|---|---|---|
| ChatGPT / Claude | Trả lời câu hỏi tự do nhưng không có context khoá học cụ thể | Free-form Q&A | Yes — nhưng thiếu curriculum context + structured output |
| Khan Academy AI Tutor | Giải thích từng bước, hỏi lại khi học sinh chưa hiểu | Adaptive + structured explanation | Partial — quá phức tạp cho 1 ngày, nhưng pattern đúng |
| GitHub Copilot Chat | Giải thích code trong context của project | Context-aware explanation | Partial — chỉ cho code, không cho khái niệm học thuật |
| Giáo viên dạy thêm (offline) | Giải thích lại khái niệm theo 3 bước: định nghĩa → ví dụ → kiểm tra | Structured pedagogy | Yes — đây chính xác là pattern AI Tutor implement |

## 5. Evidence → Insight

```text
Evidence nổi bật nhất:
- Học viên không hỏi trong giờ vì sợ gián đoạn lớp — pain thật, rào cản xã hội.
- ChatGPT thiếu context khoá học → giải thích không match nội dung đang học.
- Câu hỏi "nhỏ" không được giải đáp tích lũy → confusion lớn ở bài sau.

Insight:
Học viên không chỉ cần "một chỗ hỏi".
Thật ra họ cần:
1. Một AI biết mình đang học gì (LLM, LangChain, Agents, RAG) — không giải thích lạc đề.
2. Giải thích có cấu trúc — không phải wall of text: định nghĩa → code → kiểm tra.
3. Adaptive khi câu hỏi mơ hồ — hỏi lại thay vì đoán sai.
4. Tùy chọn upload tài liệu buổi học — AI có thêm context bài hôm nay.

Vì pattern từ evidence cho thấy:
- Rào cản là xã hội (sợ gián đoạn), không phải kỹ thuật → giải pháp là riêng tư, instant
- Vấn đề của ChatGPT là thiếu context, không phải thiếu năng lực → inject curriculum context vào prompt
- Structured output quan trọng: học viên cần code example, không chỉ text giải thích

Opportunity:
AI có thể giúp bằng cách:
- Nhận câu hỏi tự do hoặc tài liệu upload từ học viên
- Trả lời có cấu trúc cố định: 1. Giải thích ngắn → 2. Code → 3. Câu hỏi kiểm tra hiểu
- Hỏi lại khi câu hỏi mơ hồ: "Bạn đang bị stuck ở điểm nào cụ thể?"
- Dùng context tài liệu buổi học nếu học viên upload
```

## 6. Evidence đổi SPEC như thế nào?

- [x] Đổi user chính.
- [x] Đổi pain statement.
- [x] Đổi build slice.
- [x] Đổi Auto/Aug decision.
- [x] Đổi 3 paths (happy, adaptive, file upload).
- [x] Đổi failure mode.
- [x] Đổi owner/test plan.

```text
Trước evidence, nhóm định:
- Làm Session Digest Bot — tổng hợp thông tin cross-channel (Email, Discord, Web)
- User: "Học viên sau buổi học bị ngợp bởi thông tin rải rác"
- Flow: paste content → AI extract digest → correction

Sau evidence, nhóm đổi thành:
- Làm AI Tutor — trợ lý học tập real-time trong và sau lớp học
- User: "Học viên đang học live bị stuck ở khái niệm, không có chỗ hỏi phù hợp"
- Flow: gõ câu hỏi (hoặc upload file) → AI giải thích có cấu trúc → follow-up chat
- Có 3 paths: happy (câu hỏi rõ), adaptive (câu hỏi mơ hồ → AI hỏi lại), file upload

Lý do:
- Self-use + phỏng vấn bạn cùng lớp cho thấy pain thật: không hiểu nhưng không có chỗ hỏi.
- Digest flow giải quyết problem khác (information overload sau buổi học), không phải real-time confusion.
- AI Tutor giải đúng root cause: thiếu context-aware explanation ngay lúc học.
```
