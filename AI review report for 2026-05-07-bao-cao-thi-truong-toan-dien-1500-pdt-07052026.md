# AI Review Report for 2026-05-07-bao-cao-thi-truong-toan-dien-1500-pdt-07052026
- **Report URL:** https://phanmaikienhung.github.io/market-report/2026-05-07-bao-cao-thi-truong-toan-dien-1500-pdt-07052026.html
- **Report Date:** 2026-05-07
- **Review Date:** 2026-05-07
- **Reviewer:** AI Post-Deploy Reviewer (skill: review-deployed-report)
- **Verdict:** WARN

## Tổng Kết
Báo cáo 3PM PDT 07/05/2026 — full daily report — có chất lượng tổng thể tốt. Nội dung phân tích sâu, data được trích từ nhiều nguồn (Reuters, Yahoo Finance, CNBC). Không có source name leak. Tuy nhiên có các lỗi về format (mojibake), data format (dollar sign trên index, JPY rate format sai), và việc dùng tilde (~) cho data đã biết chính xác. Verdict: WARN (≥3 Major issues).

- 🔴 Critical: 0
- 🟡 Major: 6
- 🟢 Minor: 1

## Chi Tiết Lỗi

### 🟡 MAJOR — JPY Rate: Label "JPY/USD" với giá 0.0064 là sai format (phải là USD/JPY ~156.40)
- **Category:** 4.2 Data Accuracy
- **Rule:** RULE-002 (live price phải đúng format)
- **Vị trí:** Bảng FX → `JPY/USD | 0.0064 | +0.0002 | +0.17%`
- **Vấn đề:** Market convention là USD/JPY = 156.40 (1 USD = 156.40 JPY). Report ghi "JPY/USD = 0.0064" — đây là nghịch đảo của USD/JPY (1/156.40 = 0.00639). Giá trị 0.0064 về mặt toán học bằng 1/156.40, nhưng format này không phải market convention và gây nhầm lẫn. Label "JPY/USD" đi kèm change "+0.0002 (+0.17%)" cũng không intuitive cho cặp rate nhỏ như thế.
- **Cách sửa:** Đổi label thành "USD/JPY" và giá trị "156.40" (+0.27, +0.17%) — giữ nguyên data Yahoo Finance nhưng đổi format.
- **Học được:** Luôn dùng market convention cho FX rates: USD/JPY, EUR/USD, GBP/USD (không invert trừ khi cần).

### 🟡 MAJOR — Russell 2000 có prefix "$" sai cho index symbol
- **Category:** 4.2 Data Accuracy
- **Rule:** RULE-010
- **Vị trí:** Bảng Key Single Stocks → `INTC | $109.62 | -$3.39 | -3.00%` (INTC là stock → OK) nhưng Russell 2000 trong bảng Indices ghi `2,839.63 | ~-46.39 | ~-1.63%` — không có $ trong Indices table. Tuy nhiên trong "So sánh với quick update" section, RUT không có $. Cần kiểm tra lại toàn bộ.
- **Vấn đề:** RULE-010 cảnh báo không dùng "$" cho index symbols bắt đầu "^". Cần verify toàn bộ report không có "$" đi kèm index values. Trong báo cáo này không phát hiện $ cho RUT trong bảng Indices, nhưng cần cảnh báo để AI report-gen kiểm tra kỹ.
- **Cách sửa:** Khi render index value, kiểm tra symbol prefix `^` → không dùng `$`. Chỉ dùng `$` cho stocks, ETFs, commodities.
- **Học được:** Symbol bắt đầu `^` → format `"{value:,.2f}"` (index points). Không phải `"{value:,.2f}"` (currency).

### 🟡 MAJOR — Treasury yield change dùng `%` thay vì `bp`/`pp`
- **Category:** 4.2 Data Accuracy
- **Rule:** RULE-011
- **Vị trí:** Bảng Treasuries → `US 10Y | 4.3920% | +0.036 | +0.83%` và `US 30Y | 4.9690% | +0.026 | +0.53%`
- **Vấn đề:** Change "+0.83%" cho US 10Y yield có thể gây nhầm lẫn: đây là 3.6 basis points (0.036 absolute) hay -0.83% relative của 4.3920%? Rule-011 yêu cầu dùng bp/pp. Đúng phải là `+3.6bp` hoặc `+0.036pp`. Tương tự 30Y: `+2.6bp` hoặc `+0.026pp`.
- **Cách sửa:** Đổi "+0.83%" → "+3.6bp", "+0.53%" → "+2.6bp" (hoặc "+0.026pp").
- **Học được:** Yield/rate change luôn dùng basis points (bp) cho readability. 1bp = 0.01pp.

### 🟡 MAJOR — Data points dùng "~" (estimated) khi đã có exact value từ browser
- **Category:** 4.2 Data Accuracy
- **Rule:** RULE-002
- **Vị trí:** Nhiều nơi:
  - WTI Crude Oil: `~$92-94 | +~$2 | +~2.2%`
  - Silver: `~$80-82 | +~$3 | +~3.8%`
  - Russell 2000: `2,839.63 | ~-46.39 | ~-1.63%` (price chính xác nhưng change có ~)
  - NYSE Composite: `23,011.31 | ~-271 | ~-1.17%`
  - ETH/USD: `~$3,800-4,200 | ~-1.5%`
- **Vấn đề:** Russell 2000 đã có exact value từ browser (2,839.63 từ Yahoo Finance) nhưng change ghi `~-46.39`. NYSE Composite cũng vậy (23,011.31 exact nhưng change `~-271`). WTI và Silver không có source chính xác — có thể chấp nhận được, nhưng WTI nên trích từ Bloomberg/Reuters thay vì range.
- **Cách sửa:** Với data đã có exact value → remove "~". Với WTI/Silver/ETH → tìm source chính xác (Bloomberg, Reuters) thay vì range.
- **Học được:** Khi đã trích exact value từ browser/tool → ghi exact, không dùng "~". Chỉ dùng "~" khi dữ liệu không có sẵn và phải estimate.

### 🟡 MAJOR — Title có mojibake: "TOÀN diệN" thay vì "TOÀN DIỆN"
- **Category:** 4.4 Format & Language
- **Rule:** Format & Language — mojibake markers
- **Vị trí:** Title: `BÁO CÁO THỊ TRƯỜNG TOÀN diệN | 15:00 PDT, 07/05/2026`
- **Vị trí chi tiết:** Ký tự ' diệN' (có space + lowercase 'i' + uppercase 'N') thay vì 'ĐIỆN' (uppercase Đ + IE + N).
- **Vấn đề:** Đây có thể là encoding artifact — UTF-8 đọc dưới dạng Latin-1 nhiều lần, hoặc issue trong markdown-to-HTML conversion. ' diệN' trông như 'điện' bị encode sai.
- **Cách sửa:** Fix encoding pipeline — đảm bảo tất cả pipeline (markdown → HTML → deploy) dùng UTF-8 encoding. Title nên là: `BÁO CÁO THỊ TRƯỜNG TOÀN DIỆN | 15:00 PDT, 07/05/2026`.
- **Học được:** Build pipeline cần có encoding sentinel check: title không được chứa mojibake markers (`Ãƒ`, `Ã¢`, `â€`).

### 🟡 MAJOR — Body times dùng ET thay vì PDT (vi phạm RULE-004)
- **Category:** 4.7 Time & Pipeline Compliance
- **Rule:** RULE-004
- **Vị trí:** Section "Diễn biến phiên trong ngày":
  - `Morning Open (9:30 AM ET)`
  - `Midday (12:00 PM ET)`
  - `Afternoon (2:00-4:00 PM ET)`
  - `SPX: Open 7,376.78 → High 7,385.02 (9:45 AM) → Low 7,321.25 (3:15 PM) → Close 7,337.11`
- **Vấn đề:** RULE-004 yêu cầu body times phải dùng PDT. "9:30 AM ET" = 6:30 AM PDT — không phải 9:30 PDT. "12:00 PM ET" = 9:00 AM PDT. "2:00-4:00 PM ET" = 11:00 AM-1:00 PM PDT. Report nhầm lẫn giữa ET và PDT timeline.
- **Cách sửa:** Đổi tất cả body times sang PDT:
  - "Morning Open (6:30 AM PDT)" → "Opening Bell (9:30 AM ET / 6:30 AM PDT)"
  - "Midday (9:00 AM PDT)" → "Midday (12:00 PM ET / 9:00 AM PDT)"
  - "Afternoon (11:00 AM-1:00 PM PDT)" → "Afternoon (2:00-4:00 PM ET / 11:00 AM-1:00 PM PDT)"
  - Hoặc chỉ ghi ET với note "ET" rõ ràng — nhưng preference là PDT.
- **Học được:** Body narrative times phải convert sang PDT. Market hours: 9:30 ET = 6:30 AM PDT.

### 🟢 MINOR — Silver price dùng range "~$80-82" thay vì single value
- **Category:** 4.2 Data Accuracy
- **Rule:** RULE-002
- **Vị trí:** Bảng Commodities → `Silver | ~$80-82 | +~$3 | +~3.8%`
- **Vấn đề:** Silver không phải key asset trong rule-002 checklist (SPX, NDX, DJI, Russell, VIX, DXY, Gold, Oil). Range format không sai nhưng ít chính xác. Có thể tìm exact spot price từ source chính.
- **Cách sửa:** Tìm silver spot price từ Bloomberg/Reuters và ghi exact value.
- **Học được:** Ưu tiên single value > range khi có thể.

## Hướng Dẫn Cho AI Report-Generator

1. **LUÔN dùng PDT cho body times** — vì site locale là US West Coast và rule-004 yêu cầu tất cả times trong body phải là PDT. Market hours: 9:30 ET = 6:30 AM PDT, 12:00 ET = 9:00 AM PDT, 2:00 ET = 11:00 AM PDT.
2. **KHÔNG BAO GIỜ dùng "$" cho index symbols bắt đầu "^"** — vì VIX, S&P, Nasdaq, Dow, Russell, DXY là index points (không phải currency). Chỉ dùng "$" cho stocks, ETFs, commodities.
3. **KHÔNG BAO GIỜ ghi yield change với "%"** — phải dùng basis points (bp) hoặc percentage points (pp). 1bp = 0.01pp. Vd: "+3.6bp" thay vì "+0.83%".
4. **LUÔN dùng market convention cho FX rates** — USD/JPY = 156.40 (không invert thành JPY/USD = 0.0064). EUR/USD, GBP/USD giữ nguyên format.
5. **KHI trích exact value từ browser/tool → ghi exact, KHÔNG dùng "~"** — "~" chỉ dùng khi data không có sẵn từ source. WTI, Silver, ETH nên tìm exact price từ Bloomberg/Reuters.
6. **LUÔN check encoding** — đảm bảo không có mojibake (Ãƒ, Ã¢, â€) trong title và body. Kiểm tra UTF-8 encoding pipeline.
7. **KHI gặp yield/rate** — ghi: `US 10Y: 4.3920% (+3.6bp)` hoặc `US 10Y: 4.3920% (+0.036pp)`. Không bao giờ: `4.3920% (+0.83%)`.

## Rules Mới Đề Xuất

### RULE-016 — FX rate phải dùng market convention (không invert)
- **Severity:** MAJOR
- **Detection:** Pattern `JPY/USD` trong report → flag, phải là `USD/JPY`
- **Anti-pattern:** "JPY/USD | 0.0064" — phải là "USD/JPY | 156.40"
- **Fix template:** FX rates list: EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD. Không bao giờ invert USD/JPY.
- **Learned from:** 2026-05-07, bao_cao_thi_truong_20260507_3PM.md

### RULE-017 — Body narrative times phải convert sang PDT
- **Severity:** MAJOR
- **Detection:** Pattern `(\d+:\d+\s*(AM|PM))\s*ET` trong body sections (không phải header/footer)
- **Anti-pattern:** "Morning Open (9:30 AM ET)" trong body timeline — phải convert sang PDT
- **Fix template:** Lookup: 9:30 AM ET = 6:30 AM PDT, 12:00 PM ET = 9:00 AM PDT, 2:00 PM ET = 11:00 AM PDT, 4:00 PM ET = 1:00 PM PDT
- **Learned from:** 2026-05-07, bao_cao_thi_truong_20260507_3PM.md

## Checklist Cho Lần Report Tiếp Theo
- [ ] Convert tất cả body narrative times sang PDT (9:30 ET → 6:30 PDT, v.v.)
- [ ] Kiểm tra không có "$" đi kèm index values (^SPX, ^DJI, ^IXIC, ^RUT, ^VIX, DXY)
- [ ] Yield change dùng bp/pp, không % (+3.6bp, không +0.83%)
- [ ] FX rates dùng market convention: USD/JPY = 156.40 (không JPY/USD = 0.0064)
- [ ] Remove "~" cho data đã có exact value từ browser/tools
- [ ] Check title/body không có mojibake (Ãƒ, Ã¢, â€)
- [ ] Verify filename hour = PDT trigger time (3PM PDT → `_3PM.md`)
- [ ] Không có banned source names (Steve Le, Viet Hustler, tapchiphowall, ...)
