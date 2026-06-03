# Toolkit — Từ Evidence Đến Build Slice (Session Digest Bot)

## 1. Gom evidence thành cụm

**Cụm 1: Multi-channel fragmentation**
- "Deadline ở email, nội dung ở Discord, tài liệu ở web trường" (Quan sát trực tiếp)
- "Phải mở 3 tab mới chắc không miss" (Self-use)
- "Thông báo đổi phòng ở Discord nhưng lịch thi ở web" (Phỏng vấn bạn)
→ Cần: Aggregation layer — gom tất cả vào 1 chỗ

**Cụm 2: Miss deadline / action items**
- "Miss deadline vì chỉ đọc Discord, bỏ qua email có ngày cụ thể" (Phỏng vấn)
- "Không biết mình cần làm gì sau buổi học" (Quan sát)
→ Cần: Extracted action items + deadline rõ ràng, không chôn trong text dài

**Cụm 3: Thông tin mơ hồ không được flag**
- AI tóm tắt đúng nội dung nhưng không detect "nộp sớm" là deadline mơ hồ (Self-use test)
→ Cần: Low-confidence flagging — khi deadline không rõ, phải hỏi lại thay vì bịa

## 2. Viết insight

```text
Học viên sau buổi live session không chỉ cần tóm tắt nội dung học.
Họ thật ra cần một bản digest tổng hợp cross-channel với action items + deadlines rõ ràng,
vì:
1. Thông tin buổi học nằm rải rác trên 3+ kênh (Email, Discord, Web/LMS) → phải gom thủ công.
2. Deadline thường bị chôn trong text hoặc chỉ được nhắc ở 1 kênh → dễ miss.
3. AI tóm tắt 1 nguồn không đủ — cần merge nhiều nguồn mới giải quyết root cause.
```

## 3. Viết opportunity

```text
Cơ hội là dùng AI để:
1. Nhận paste content từ 3 kênh (Email + Discord + Web/LMS) cùng 1 lúc
2. Extract và merge thành digest cấu trúc:
   - Key concepts từ buổi học
   - Action items với deadline cụ thể
   - Flags khi deadline mơ hồ (hỏi lại user thay vì tự bịa)

Giúp user:
- Từ 3 tab xuống 1 bản digest trong < 30 giây
- Không miss action items hoặc deadline
- Biết ngay khi nào thông tin chưa đủ (flag ⚠️)

Trong khi vẫn kiểm soát risk:
- Nếu deadline mơ hồ ("nộp sớm") → flag thay vì hallucinate ngày cụ thể
- Nếu LLM trả non-JSON → hiển thị raw text thay vì crash
- User có thể bổ sung thông tin thiếu → AI re-generate digest với context mới
```

## 4. Chọn build slice

| Câu hỏi | Đạt khi | Session Digest Bot |
|---|---|---|
| User cụ thể chưa? | Nói được ai dùng, trong bối cảnh nào. | ✅ Học viên sau buổi live session, đang ngồi trước màn hình với Email + Discord + web mở sẵn. |
| Task đủ hẹp chưa? | Demo được trong 3-5 phút. | ✅ Paste content 3 kênh → bấm Generate → nhận digest 3 sections trong < 30 giây. |
| AI decision rõ chưa? | AI gợi ý/tự làm một việc cụ thể. | ✅ AI **augment**: extract + merge + flag. User verify và correct nếu sai. |
| Failure path rõ chưa? | Có một case AI không chắc hoặc sai để test. | ✅ Failure case: deadline mơ hồ ("nộp sớm") → AI flag ⚠️ thay vì tự bịa ngày. |
| Có evidence không? | Có bằng chứng từ self-use/review/user/competitor. | ✅ Self-use (3 observation), phỏng vấn 2 bạn cùng lớp, quan sát trực tiếp Batch 02. |

**Quyết định:** ✅ **BUILD** - Slice này đạt đủ 5 tiêu chí.

## 5. Quyết định: giữ, giảm scope, hay đổi hướng?

| Tình huống | Quyết định | Session Digest Bot |
|---|---|---|
| Evidence yếu, user mơ hồ | Dừng build sâu; quay lại research. | ❌ Không - evidence rõ từ self-use + phỏng vấn trực tiếp. |
| Ý tưởng quá rộng | Giữ domain, cắt xuống một flow. | ✅ **Applied** - Không build full LMS integration, không scrape kênh tự động → chỉ paste thủ công, 1 flow duy nhất. |
| AI không cần thiết | Dùng rule/manual. | ❌ Không - cần LLM để merge multi-source free text + extract deadline từ ngữ cảnh. |
| Rủi ro cao | Chọn augmentation. | ✅ **Applied** - Augmentation: AI draft digest, user verify. AI không tự gửi hay action gì. |
| Không demo được trong 1 ngày | Giữ một path nhỏ. | ✅ **Applied** - Demo 4 paths (happy/low-confidence/failure/correction). Backlog: auto-fetch từ kênh thật. |

## 6. Câu chốt cuối

```text
Dựa trên evidence từ self-use (3 observation), phỏng vấn trực tiếp (2 bạn cùng lớp), quan sát Batch 02,
nhóm sẽ build prototype "Session Digest Bot",
cho học viên sau buổi live session đang bị ngợp bởi thông tin rải rác trên 3 kênh,
để giải quyết pain: multi-channel fragmentation + miss deadline + không biết action items,
bằng cách AI nhận paste content từ Email/Discord/Web rồi extract digest cấu trúc (key concepts + action items + flags),
và sẽ test failure path: deadline mơ hồ ("nộp sớm") → AI flag ⚠️ thay vì hallucinate ngày cụ thể.
```

## 7. Backlog

Những thứ **không build trong Day 06**:

- Auto-fetch từ Discord API / Gmail API (scrape thay vì paste thủ công)
- Lưu digest theo lịch sử buổi học (database)
- Push notification khi deadline gần
- Integration với calendar (Google Calendar, Notion)
- Multi-language support
- Nhớ preference user qua session
