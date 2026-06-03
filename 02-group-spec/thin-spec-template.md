# Thin SPEC — Session Digest Bot

## 1. Track, product/app và user

**Track:** A - Learning OS: AI cho giáo dục, LMS, trợ lý học tập  
**Product/app thật:** Session Digest Bot — AI tổng hợp thông tin buổi học từ Email, Discord, Web/LMS  
**User cụ thể:** Học viên sau buổi live session, đang ngồi trước màn hình với 3 kênh thông tin mở sẵn (Email, Discord, Web/LMS) và không biết mình cần làm gì tiếp theo.

**Nhóm có phải user thật không?**  
Có — toàn bộ nhóm đang học Batch 02, trải nghiệm đúng pain này sau mỗi buổi lab.

## 2. Evidence summary

| Evidence | Nguồn | User/pain nói lên điều gì? | SPEC phải đổi gì? |
|---|---|---|---|
| Deadline ở email, nội dung ở Discord, tài liệu ở web trường — phải mở 3 tab | Self-use, Batch 02 | Không có single source of truth sau buổi học | App phải nhận input từ 3 kênh cùng lúc, không chỉ 1 nguồn |
| Bạn cùng lớp miss deadline vì chỉ đọc Discord, bỏ qua email | Phỏng vấn trực tiếp | Multi-channel → miss thông tin thật | Output phải highlight deadline riêng, không chôn trong text |
| AI tóm tắt 1 nguồn đúng nội dung nhưng miss deadline ở kênh khác | Self-use test | Single-source AI không đủ | AI phải merge từ nhiều nguồn trước khi extract |
| "Nộp sớm nhé" trên Discord không có ngày cụ thể | Quan sát trực tiếp | Deadline mơ hồ rất phổ biến | AI phải flag thay vì tự bịa ngày → low-confidence path |

## 3. Pain statement

```text
Học viên sau buổi live session đang gặp khó ở bước "nắm được mình cần làm gì tiếp theo",
vì thông tin buổi học bị phân mảnh trên 3+ kênh (Email, Discord, Web/LMS) không có aggregation,
dẫn tới:
- Miss deadline vì không đọc đủ tất cả kênh.
- Mất thời gian scroll lại toàn bộ chat để tìm action items.
- Không biết khi nào thông tin đã đủ hay còn thiếu.
Bằng chứng chính là: 2 bạn cùng lớp xác nhận miss deadline vì multi-channel + self-use test cho thấy AI 1 nguồn không đủ context.
```

## 4. Build slice

```text
Cho học viên sau buổi live session đang bị ngợp bởi thông tin rải rác trên 3 kênh,
prototype sẽ dùng AI để nhận paste content từ Email + Discord + Web/LMS cùng lúc,
tạo ra digest cấu trúc gồm:
- Key concepts: những khái niệm/nội dung chính của buổi học
- Action items: việc cần làm, kèm deadline nếu có
- Flags ⚠️: thông tin mơ hồ cần làm rõ (deadline không rõ ngày, thiếu link...)
Và xử lý failure mode bằng cách flag thay vì hallucinate — nếu deadline không rõ → hỏi lại user, không tự bịa ngày.
```

## 5. Auto/Aug decision

- [x] **Augmentation:** AI gợi ý/draft/phân loại, user quyết cuối.
- [ ] **Conditional automation:** AI tự làm trong case hẹp; case mơ hồ/rủi ro chuyển người.
- [ ] **Automation:** AI tự quyết và tự hành động.

**Lý do chọn Augmentation:**  
Deadline sai → học viên miss bài → hậu quả thật. AI không được tự claim deadline khi không chắc. User phải verify output trước khi rely vào.

**Human role:** reviewer (kiểm tra digest trước khi action) + corrector (bổ sung thông tin thiếu)

## 6. Four paths

| Path | Prototype phải thể hiện gì? |
|---|---|
| **Happy** | Paste content rõ từ 3 kênh → digest sạch 3 sections, không có flag → user thấy key concepts + action items + deadline cụ thể |
| **Low-confidence** | Deadline mơ hồ ("nộp sớm") → AI flag ⚠️ với câu hỏi cụ thể: "Discord chỉ nói 'nộp sớm' — deadline cụ thể là bao giờ?" |
| **Failure** | AI miss hoặc sai 1 action item → user nhập correction → AI re-generate digest với context mới |
| **Correction** | User thêm thông tin còn thiếu vào correction box → digest cập nhật, flag về thông tin đó biến mất |

## 7. Failure mode nguy hiểm nhất

```text
Nếu user paste content từ nhiều buổi học khác nhau không phân biệt ngày,
AI có thể trộn deadline của buổi cũ vào action items buổi mới,
hậu quả là học viên miss deadline thật vì tin vào digest sai.

Prototype xử lý bằng:
1. Field "Buổi học / ngày" bắt buộc nhập — dùng làm anchor trong prompt.
2. Prompt instruction: "Chỉ lấy thông tin liên quan đến buổi học ngày [date]."
3. Nếu deadline không rõ ngày cụ thể → đưa vào flags, không đưa vào action items.

Owner kiểm thử path này: người build prototype.
```

## 8. Owner plan cho sáng Day 06

| Thành viên | Việc phụ trách | Bằng chứng cần có trong repo |
|---|---|---|
| Dev | `src/digest.py` — prompt builder + LLM call + JSON parser | File + 11 unit tests passing |
| Dev | `app.py` — Streamlit UI (form + render + correction flow) | App chạy tại localhost:8501 |
| Dev | Test 4 paths với real data từ lớp | Screenshot 4 paths |
| Dev | `README.md` — setup + hướng dẫn chạy | File committed |
| All | Demo script (3 paths: happy, low-confidence, correction) | Demo chạy được trong 3 phút |
