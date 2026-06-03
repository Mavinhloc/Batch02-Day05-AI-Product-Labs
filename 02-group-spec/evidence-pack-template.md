# Evidence Pack — Session Digest Bot

## 1. Nhóm và track

**Tên nhóm:** Học chăm  
**Track:** A - Learning OS: AI cho giáo dục, LMS, trợ lý học tập  
**Product/app đã chọn:** Session Digest Bot — AI tổng hợp thông tin buổi học từ nhiều kênh  
**Build slice đang nghĩ:** AI nhận paste content từ Email/Discord/Web → tóm tắt thành key concepts + action items + deadline flags trong 1 lượt

## 2. Self-use evidence

| Observation | Screenshot/link | Path liên quan | Điều học được |
|---|---|---|---|
| Sau buổi lab, thông báo bài tập được gửi trên Discord, link tài liệu ở web trường, reminder qua email — 3 nơi khác nhau, không có chỗ tổng hợp. | Trải nghiệm trực tiếp trong lớp Batch 02 | Failure | Học viên phải mở 3 tab, đọc lại 3 lần mới chắc không miss gì. |
| Hỏi bạn cùng lớp "hôm nay có bài nộp không?" — bạn không biết vì chỉ đọc Discord, bỏ qua email có deadline cụ thể. | Quan sát trực tiếp trong lớp | Failure | Thông tin bị phân mảnh → học viên miss deadline thật. |
| Thử dùng AI tóm tắt một đoạn Discord: AI cho ra tóm tắt đúng nội dung nhưng không extract được deadline vì deadline nằm trong email khác. | Self-use test | Low-confidence | AI cần nhận input từ nhiều nguồn cùng lúc mới đủ context. |

## 3. User / review / social evidence

| Quote / review / observation | Nguồn | User là ai? | Pain/failure mode |
|---|---|---|---|
| "Mình miss deadline vì nghĩ thầy chỉ nhắc trên Discord, hoá ra email mới có ngày cụ thể." | Phỏng vấn nhanh 2 bạn cùng lớp | Học viên năm 1-2, 19-21 tuổi | Multi-channel → miss thông tin quan trọng |
| "Sau buổi học online mình hay không biết mình cần làm gì tiếp theo, phải scroll lại toàn bộ chat mới nhớ." | Quan sát trực tiếp | Học viên học hybrid/online | Không có single source of truth sau buổi học |
| "Thông báo lịch thi ở web trường, nhưng đổi phòng thì Discord, còn tài liệu thì email — mệt lắm." | Nói chuyện nhóm trước giờ học | Học viên đại học | Fragmented channels → cognitive overload |

## 4. Competitor / analog evidence

| App / mô hình tham khảo | Họ xử lý task này thế nào? | Pattern học được | Có áp dụng trong 1 ngày không? |
|---|---|---|---|
| Notion AI / Summarize | Tóm tắt 1 document/page, không tổng hợp cross-channel | Single source summary | Yes — nhưng thiếu multi-channel merge |
| Slack AI summarize | Tóm tắt thread/channel, nhưng chỉ trong Slack | Channel-scoped summary | Partial — cần mở rộng ra ngoài 1 app |
| Google NotebookLM | Nhận nhiều nguồn → hỏi đáp, tóm tắt | Multi-source RAG | Partial — quá phức tạp cho 1 ngày, nhưng pattern đúng |
| Manual note-taking | Học viên tự ghi chú sau mỗi buổi | Human digest | Yes — AI thay thế bước thủ công này |

## 5. Evidence → Insight

```text
Evidence nổi bật nhất:
- Học viên nhận thông tin từ 3-4 kênh khác nhau sau mỗi buổi học.
- Không có kênh nào là "single source of truth" — deadline ở email, nội dung ở Discord, tài liệu ở web.
- Kết quả thực tế: miss deadline, phải hỏi lại bạn, mất thời gian scroll tìm thông tin.

Insight:
Học viên không chỉ cần tóm tắt nội dung học.
Thật ra họ cần:
1. Một bản digest tổng hợp từ tất cả kênh sau mỗi buổi — không cần mở nhiều tab.
2. Action items + deadline rõ ràng — biết ngay hôm nay cần làm gì.
3. Flag khi thông tin không đầy đủ — biết khi nào cần hỏi thêm thay vì miss.

Vì pattern từ evidence cho thấy:
- Có nhiều kênh thông tin nhưng không có aggregation layer
- Học viên tự làm thủ công (scroll, đọc lại) — tốn thời gian và dễ miss
- AI có thể thay thế bước aggregate + extract này trong vài giây

Opportunity:
AI có thể giúp bằng cách:
- Nhận paste content từ Email + Discord + Web cùng lúc
- Extract: key concepts + action items + deadlines
- Flag khi deadline mơ hồ thay vì tự bịa ngày
- Cho phép user bổ sung thông tin thiếu và re-generate
```

## 6. Evidence đổi SPEC như thế nào?

- [x] Đổi user chính.
- [x] Đổi pain statement.
- [x] Đổi build slice.
- [x] Đổi Auto/Aug decision.
- [x] Đổi 4 paths.
- [x] Đổi failure mode.
- [x] Đổi owner/test plan.

```text
Trước evidence, nhóm định:
- Làm "AI tóm tắt bài học" generic (1 nguồn, 1 lượt summarize)
- User: "Học viên muốn ôn bài"
- Không xử lý được case deadline không rõ hoặc thông tin thiếu

Sau evidence, nhóm đổi thành:
- Làm "Session Digest Bot" — tổng hợp cross-channel (Email + Discord + Web)
- User: "Học viên sau buổi live session bị ngợp bởi thông tin rải rác"
- Có 4 paths: happy (digest sạch), low-confidence (flag deadline mơ hồ), failure (parse error fallback), correction (user bổ sung → re-generate)

Lý do:
- Self-use + phỏng vấn bạn cùng lớp cho thấy pain thật: miss deadline vì multi-channel.
- Tóm tắt 1 nguồn không đủ — cần merge nhiều nguồn mới giải quyết được root cause.
- Failure path quan trọng: AI không được tự bịa deadline → phải flag và hỏi lại.
```
