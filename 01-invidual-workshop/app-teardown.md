# Workshop — Mổ App AI Thật

**Thời gian:** 35-45 phút  
**Hình thức:** cá nhân trước, chia sẻ theo nhóm sau  
**Output:** finding note + sketch `as-is / to-be`

Mục tiêu không phải chấm "UI đẹp hay xấu". Mục tiêu là dùng sản phẩm thật như một bài needfinding: tìm chỗ product gãy trong workflow thật, rồi viết finding đó thành quyết định product.

## 1. Chọn một sản phẩm để dùng thử

| Sản phẩm | AI feature | Cách truy cập |
|---|---|---|
| MoMo — Moni | Trợ thủ tài chính, phân tích chi tiêu, chatbot | App MoMo |
| Vietnam Airlines — NEO | Chatbot hỗ trợ vé, hành lý, khiếu nại | Website/Zalo VNA |
| V-App — V-AI | Trợ lý voice/text, gợi ý theo ngữ cảnh | App V-App |

## 2. Dùng thử: promise vs reality

Ghi nhanh:

- Product hứa gì?
- User nào được hứa sẽ được giúp?
- Bạn kỳ vọng AI làm được task nào?
- Khi dùng thật, điểm gãy xuất hiện ở đâu?

Evidence cần có:

- screenshot,
- quote từ app/web/review,
- prompt/input đã thử,
- hành vi quan sát được.

## 3. Vẽ 4 paths

| Path | Câu hỏi cần trả lời |
|---|---|
| Happy | Khi AI đúng và tự tin, user thấy gì? |
| Low-confidence | Khi AI không chắc, hệ thống có hỏi lại, show options hoặc chuyển người không? |
| Failure | Khi AI sai, user biết bằng cách nào và sửa thế nào? |
| Correction | Khi user sửa, correction có được lưu/log/học lại không hay biến mất? |

## 4. Viết finding thành quyết định

Không viết:

```text
Bot ngu, trả lời sai.
```

Viết:

```text
Khi user [trigger],
AI/product [failure],
hậu quả là [impact].
Lỗi thuộc layer [promise / intent / data-tool / safety / UX recovery].
Nên sửa bằng [requirement / UX / fallback / human role / test case].
```

Ví dụ:

```text
Khi user hỏi "chi tiêu linh tinh là gì?",
AI hiểu như keyword thay vì nhận ra intent mơ hồ,
hậu quả là user không biết sửa phân loại chi tiêu ở đâu.
Lỗi thuộc Intent + UX Recovery.
Nên sửa bằng low-confidence path: hỏi lại tiêu chí hoặc đưa 2-3 nhóm giao dịch để chọn.
```

## 5. Sketch as-is / to-be

Vẽ 2 cột:

- **As-is:** flow hiện tại, đánh dấu điểm gãy.
- **To-be:** flow đề xuất, đánh dấu path đã sửa.

Không cần đẹp. Cần nhìn vào là hiểu:

- user làm gì,
- AI làm gì,
- lúc AI không chắc thì sao,
- lúc AI sai user recover thế nào.

## 6. Tự kiểm trước khi nộp

- [x] Có ít nhất 1 screenshot hoặc observation cụ thể.
- [x] Có đủ 4 paths hoặc nói rõ path nào chưa có trong product.
- [x] Finding được viết thành product decision, không chỉ là nhận xét.
- [x] Sketch có as-is và to-be.
- [x] Có một câu nói rõ finding này sẽ đổi gì trong SPEC.

---

## Kết quả — Mavinhloc (V-App / V-AI)

### 1. Sản phẩm: V-App — V-AI

### 2. Promise vs Reality

**Product hứa:** Trợ lý AI voice/text, hỗ trợ mọi tác vụ theo ngữ cảnh người dùng.

**User được hứa:** Người dùng phổ thông cần trợ lý thực hiện task nhanh — viết, tìm kiếm, tạo nội dung.

**Kỳ vọng:** Gõ "hãy lập trình game xo bằng html cho tôi" → nhận được file code chạy được.

**Điểm gãy:** V-AI từ chối viết code trực tiếp, chuyển sang chế độ hướng dẫn (tutorial) với danh sách bullet points và trích dẫn từ 10 nguồn ngoài (labex, codingartistweb...) — không có một dòng code nào được tạo ra.

**Evidence:**
- Screenshot `b5e56faa`: V-AI nói rõ *"V-AI rất tiếc, V-AI không thể trực tiếp cung cấp mã lập trình hoàn chỉnh"* → explicit refusal
- Screenshot `c7b7754a`: Input "Hãy lập trình game xo bằng html cho tôi" → output là tutorial 3 mục HTML/CSS/JS với nguồn ngoài, không có code
- Screenshot `01d1a16a`: V-AI từ chối câu hỏi về cờ bạc → safety filter hoạt động đúng (contrast: safety đúng, intent detection sai)

### 3. Bốn Paths

| Path | Quan sát thực tế |
|---|---|
| **Happy** | User hỏi câu hỏi thông tin thông thường → V-AI trả lời trực tiếp, có nguồn |
| **Low-confidence** | Không rõ V-AI có hỏi lại khi intent mơ hồ không — chưa observe được path này |
| **Failure** | User yêu cầu viết code rõ ràng → V-AI phân loại sai thành "cần hướng dẫn", từ chối thực thi, trả tutorial |
| **Correction** | User đổi cách hỏi (vẫn cùng intent) → V-AI vẫn giữ tutorial mode, không adapt — correction không có tác dụng |

### 4. Finding → Product Decision

```
Khi user yêu cầu "hãy lập trình game xo bằng html cho tôi" (động từ hành động rõ: "lập trình"),
V-AI phân loại request là "educational query" thay vì "execution request",
từ chối viết code và trả về hướng dẫn nhiều bước kèm nguồn ngoài,
hậu quả là user không nhận được output cần thiết và phải tự tìm code ở nơi khác.
Lỗi thuộc layer: Intent (AI hiểu sai loại task) + UX Recovery (không có fallback để user báo "tôi muốn code, không phải hướng dẫn").
Nên sửa bằng:
- Phân biệt intent "explain how" vs "just do it": khi request có động từ thực thi rõ ("viết", "tạo", "lập trình", "code") → thực thi trước.
- Thêm quick-reply sau response: [Tôi muốn code luôn] [Giải thích thêm] để user chọn path.
- Nếu có policy cấm viết code hoàn chỉnh → nói rõ lý do ngay, không giả vờ hướng dẫn thay thế.
```

### 5. Sketch As-is / To-be

```
AS-IS (flow hiện tại):
────────────────────────────────────────────────────
User: "Hãy lập trình game xo bằng html cho tôi"
  ↓
V-AI: tìm kiếm 10 nguồn bên ngoài
  ↓
V-AI: phân loại = "coding tutorial request" ← [ĐIỂM GÃY: intent sai]
  ↓
V-AI: từ chối viết code trực tiếp ← [ĐIỂM GÃY: policy không rõ]
  ↓
V-AI: trả bullet list HTML/CSS/JS steps + nguồn ngoài
  ↓
User: nhận hướng dẫn không cần, phải google thêm ← [IMPACT]
────────────────────────────────────────────────────

TO-BE (flow đề xuất):
────────────────────────────────────────────────────
User: "Hãy lập trình game xo bằng html cho tôi"
  ↓
V-AI: detect động từ "lập trình" + object "game xo" = execution intent rõ
  ↓
  [Nếu policy cho phép code]
  V-AI: viết code HTML/CSS/JS hoàn chỉnh
  V-AI: (optional) thêm giải thích ngắn bên dưới
  → User: copy-paste và dùng ngay ✓

  [Nếu policy không cho phép code hoàn chỉnh]
  V-AI: nói rõ "V-AI không hỗ trợ viết code hoàn chỉnh vì [lý do]"
  V-AI: đưa 2 option [Xem hướng dẫn từng bước] [Tìm trên GitHub]
  → User: biết rõ giới hạn, chọn path phù hợp ✓
────────────────────────────────────────────────────
```

### Finding → SPEC Impact

Finding này thay đổi SPEC ở chỗ: **bất kỳ AI assistant nào** trong product của nhóm cần phân biệt rõ hai mode — *explain* và *execute* — và mặc định chọn *execute* khi user dùng động từ hành động rõ. Nếu có giới hạn, phải nói thẳng lý do thay vì redirect sang tutorial.
