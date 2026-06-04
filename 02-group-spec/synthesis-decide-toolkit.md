# Toolkit — Từ Evidence Đến Build Slice (AI Tutor)

## 1. Gom evidence thành cụm

**Cụm 1: Rào cản xã hội — không dám hỏi trong giờ**
- "Không dám hỏi vì sợ làm mất thời gian của cả lớp" (Phỏng vấn bạn)
- Quan sát: học viên giữ câu hỏi lại, đến cuối buổi quên hoặc không còn cơ hội (Self-use)
→ Cần: kênh hỏi riêng tư, instant, không gián đoạn lớp

**Cụm 2: AI không có context khoá học**
- ChatGPT giải thích đúng kỹ thuật nhưng không biết khoá đang học version/pattern nào (Self-use test)
- Giải thích lạc đề so với nội dung thầy dạy → học viên mất thêm thời gian filter (Quan sát)
→ Cần: AI biết curriculum (LLM, LangChain, Agents, RAG) + có thể nhận tài liệu buổi học

**Cụm 3: Giải thích không có cấu trúc phù hợp**
- Code examples trên slide qua nhanh, không có giải thích step-by-step (Quan sát trực tiếp)
- Wall of text từ AI khó tiêu hóa khi đang học nhanh trong lớp (Self-use)
→ Cần: Output cố định 3 phần: định nghĩa ngắn → code cụ thể → kiểm tra hiểu

## 2. Viết insight

```text
Học viên không chỉ cần "một chỗ hỏi AI".
Họ thật ra cần một AI tutor biết context khoá học, giải thích có cấu trúc sư phạm,
vì:
1. Rào cản hỏi trong lớp là xã hội, không phải kỹ thuật → cần riêng tư, instant.
2. ChatGPT có năng lực nhưng thiếu context → inject curriculum + tài liệu buổi học vào prompt là đủ.
3. Structured output (định nghĩa → code → kiểm tra) hiệu quả hơn free-form explanation cho technical content.
```

## 3. Viết opportunity

```text
Cơ hội là dùng AI để:
1. Nhận câu hỏi tự do (gõ/paste) hoặc tài liệu buổi học (upload PDF/DOCX/TXT)
2. Giải thích có cấu trúc cố định:
   - Giải thích ngắn gọn: định nghĩa / khái niệm cốt lõi
   - Ví dụ code cụ thể (nếu áp dụng)
   - Câu hỏi kiểm tra hiểu: "Bạn có thể giải thích lại... không?"
3. Adaptive khi câu hỏi mơ hồ: hỏi lại trước khi giải thích

Giúp user:
- Hỏi ngay trong giờ mà không gián đoạn thầy — riêng tư, instant
- Nhận giải thích đúng context khoá học, không lạc đề
- Verify hiểu qua code example cụ thể + câu hỏi kiểm tra

Trong khi vẫn kiểm soát risk:
- Nếu câu hỏi mơ hồ → hỏi lại thay vì đoán sai
- Nếu LLM fail → thông báo lỗi rõ, giữ nguyên chat history, cho retry
- Nếu file không hỗ trợ → thông báo lỗi, vẫn cho phép chat không có context
```

## 4. Chọn build slice

| Câu hỏi | Đạt khi | AI Tutor |
|---|---|---|
| User cụ thể chưa? | Nói được ai dùng, trong bối cảnh nào. | ✅ Học viên Batch 02 đang học live, bị stuck ở khái niệm, không có chỗ hỏi phù hợp. |
| Task đủ hẹp chưa? | Demo được trong 3-5 phút. | ✅ Gõ câu hỏi → AI giải thích 3 phần → follow-up chat. Demo 3 paths trong < 3 phút. |
| AI decision rõ chưa? | AI gợi ý/tự làm một việc cụ thể. | ✅ AI **augment**: giải thích có cấu trúc + adaptive khi mơ hồ. User verify và hỏi follow-up. |
| Failure path rõ chưa? | Có một case AI không chắc hoặc sai để test. | ✅ Adaptive path: câu hỏi mơ hồ ("Tôi không hiểu") → AI hỏi lại, không đoán. |
| Có evidence không? | Có bằng chứng từ self-use/review/user/competitor. | ✅ Self-use (3 observation), phỏng vấn 2 bạn cùng lớp, quan sát trực tiếp Batch 02. |

**Quyết định:** ✅ **BUILD** - Slice này đạt đủ 5 tiêu chí.

## 5. Quyết định: giữ, giảm scope, hay đổi hướng?

| Tình huống | Quyết định | AI Tutor |
|---|---|---|
| Evidence yếu, user mơ hồ | Dừng build sâu; quay lại research. | ❌ Không - evidence rõ từ self-use + phỏng vấn trực tiếp. |
| Ý tưởng quá rộng | Giữ domain, cắt xuống một flow. | ✅ **Applied** - Không build quiz engine, không build learning path, không lưu progress → chỉ chat Q&A 1 flow. |
| AI không cần thiết | Dùng rule/manual. | ❌ Không - cần LLM để giải thích khái niệm technical theo context + adaptive response. |
| Rủi ro cao | Chọn augmentation. | ✅ **Applied** - Augmentation: AI draft giải thích, user verify và internalize. AI không tự quyết học viên "đã hiểu". |
| Không demo được trong 1 ngày | Giữ một path nhỏ. | ✅ **Applied** - Demo 3 paths (happy/adaptive/file upload). Backlog: quiz tự động, lưu history, learning analytics. |

## 6. Câu chốt cuối

```text
Dựa trên evidence từ self-use (3 observation), phỏng vấn trực tiếp (2 bạn cùng lớp), quan sát Batch 02,
nhóm sẽ build prototype "AI Tutor",
cho học viên Batch 02 đang học live session bị stuck ở khái niệm kỹ thuật,
để giải quyết pain: không có chỗ hỏi phù hợp (rào cản xã hội) + AI generic thiếu context khoá học,
bằng cách AI nhận câu hỏi / tài liệu buổi học rồi giải thích có cấu trúc (định nghĩa + code + kiểm tra),
và sẽ test adaptive path: câu hỏi mơ hồ ("Tôi không hiểu") → AI hỏi lại thay vì đoán sai.
```

## 7. Backlog

Những thứ **không build trong Day 05-06**:

- Quiz tự động sau mỗi buổi học
- Lưu lịch sử Q&A qua nhiều session (database)
- Learning analytics — theo dõi học viên stuck ở đâu nhiều nhất
- Hỗ trợ môn học ngoài AI curriculum
- Multi-user / authentication
- Auto-fetch tài liệu từ LMS (scrape thay vì upload thủ công)
- Integration với lịch học / calendar
