# Review Report: MARKET REPORT — QUICK 11:30 AM PDT (2026-05-05)
- **Report URL (reviewed):** https://phanmaikienhung.github.io/market-report/2026-05-05-cap-nhat-thi-truong-1130-05052026.html
- **Report URL (also deployed):** https://phanmaikienhung.github.io/market-report/2026-05-05-bao-cao-tong-quan-thi-truong-thu-2-05052026-0600-a.html (6 AM PDT Full — from prior build)
- **Report Date:** 2026-05-05
- **Review Date:** 2026-05-05
- **Reviewer:** AI Post-Deploy Reviewer (task: review-deployed-report)
- **Verdict:** FAIL

## Tổng Kết
Báo cáo Quick 11:30 AM PDT (2026-05-05) có cấu trúc tốt với dữ liệu mid-session khá chính xác, nhưng chứa lỗi nghiêm trọng: (1) chữ Trung Quốc trong Dashboard Summary, (2) VIX change direction bị mâu thuẫn giữa 6AM và 11:30AM report, và (3) nhiều lỗi format trong bảng dữ liệu (yield change dùng %, DXY ~$ prefix, Russell 2000 missing change). Báo cáo 6AM Full cũng có lỗi language leak (chữ Trung Quốc).
- 🔴 Critical: 1
- 🟡 Major: 6
- 🟢 Minor: 4

## Chi Tiết Lỗi

### 🔴 CRITICAL — Chinese characters in Dashboard Summary
- **Category:** 4.4 Format & Language
- **Vị trí:** 6AM Full report, section "📋 DASHBOARD SUMMARY"
- **Quote:** `📈 S&P 500: 7,254.75 +0.75% 🟢接近ATH` (Chinese: "接近" = "接近")
- **Vấn đề:** Có character tiếng Trung trong phần dashboard của report tiếng Việt. Đây là pattern encoding/cross-language contamination — có thể do pipeline đọc data từ source tiếng Trung hoặc prompt leakage.
- **Cách sửa:** Build pipeline phải scan title/content cho non-ASCII characters ngoài Unicode tiếng Việt (phải có diacritic: `â, ê, ô, ơ, ư`). Flag khi thấy CJK chars (U+4E00-U+9FFF).
- **Học được:** RULE đề xuất: Scan output cho CJK characters (Chinese/Japanese/Korean) — không bao giờ xuất hiện trong report Việt Nam.

### 🟡 MAJOR — VIX change direction inconsistency between reports
- **Category:** 4.2 Data Accuracy / 4.6 Cross-Reference Consistency
- **Rule:** RULE-002, AP-002
- **Vị trí:** So sánh 6AM report (VIX 17.44, +2.65%) vs 11:30AM report (VIX 17.23, -5.80%)
- **Vấn đề:** 
  - 6AM report ghi VIX: `17.44, +0.45, +2.65%` (tăng so với prev close 16.99)
  - 11:30AM report ghi VIX: `17.23, -1.06, -5.80%` (giảm so với gì đó ~18.28)
  - Cả hai cùng timestamp (05/05/2026) nhưng direction ngược nhau. Nếu prev close thật sự là 16.99 (Friday close), thì +2.65% = 17.44 là đúng (17.44 - 16.99 = +0.45). Nhưng -5.80% so với 16.99 thì phải = 16.04, không phải 17.23. Dữ liệu 11:30AM có vẻ sai.
- **Cách sửa:** Kiểm tra cross-report consistency cho VIX — các report trong cùng ngày phải dùng base price thống nhất (prev day close). Nếu có discrepancy > 1% → flag MAJOR.
- **Học được:** Khi multiple reports cùng ngày, baseline phải đồng nhất. Nếu VIX ở 11:30AM là 17.23 thì change phải so với 6AM price (17.44) = -1.37%, không phải -5.80%.

### 🟡 MAJOR — Russell 2000 missing change value
- **Category:** 4.2 Data Accuracy
- **Rule:** RULE-002
- **Vị trí:** 11:30AM report, bảng Major Indices, row Russell 2000
- **Quote:** `Russell 2000 (^RUT) | 2,842.12 | — | +1.65% | 2,841.67 | 🔥 Phá ATH liên tục`
- **Vấn đề:** Cột "Thay đổi" (change) trống (chỉ có `—`). Người đọc không biết Russell 2000 thay đổi bao nhiêu points. Chỉ có % change (+1.65%) là có.
- **Cách sửa:** Template bảng phải đảm bảo tất cả columns đầy đủ. Change value = Price - Prev Close = 2,842.12 - 2,812.82 = +29.30.
- **Học được:** RULE đề xuất: Tất cả bảng giá phải có 4 fields: Price, Change, %, 52w. Không được thiếu field nào.

### 🟡 MAJOR — Yield change column uses % instead of bp
- **Category:** 4.3 Arithmetic & Units
- **Rule:** RULE-011 (anti-pattern: yield change phải ghi bp hoặc pp, không %)
- **Vị trí:** 11:30AM report, bảng Commodities & Yields, row 10Y Treasury Yield
- **Quote:** `10Y Treasury Yield (^TNX) | 4.416% | -0.030 | -0.67%`
- **Vấn đề:** Change column ghi `-0.030` (absolute) nhưng % column ghi `-0.67%` (tương đối). Quy tắc RULE-011 yêu cầu yield change phải dùng bp/pp để tránh nhầm lẫn. Đúng phải là: `-2.8bp` hoặc `-0.67pp`. Không ghi `-0.67%` vì nhầm lẫn với pct change.
- **Cách sửa:** Template phải auto-convert yield change từ absolute pp sang bp: `change_bp = (yield - prev_yield) * 10000`
- **Học được:** RULE-011 đã có trong reviewer_rules.md. Report generator phải tuân thủ.

### 🟡 MAJOR — DXY value inconsistency (~$110.6 vs live ~98.45)
- **Category:** 4.2 Data Accuracy
- **Rule:** RULE-002
- **Vị trí:** 6AM Full report, bảng Bond Yields & Dollar
- **Quote:** `DXY (Dollar Index) | ~110.6 | -0.11%` và `DXY ước tính từ UUP ETF ($27.45, -0.11%) × ~4.03`
- **Vấn đề:** DXY hiện tại (~98.45) hoàn toàn khác với ~110.6 được ghi trong report. UUP ETF = ~$27.45 và DXY/4.03 ≈ 97.4, không phải 110.6. Có vẻ đây là giá DXY cũ (từ khoảng tháng 1-2/2026 khi DXY còn ở ~106-110). Data source đã stale.
- **Cách sửa:** DXY phải search live từ Yahoo Finance `^DXY` mỗi lần generate report. Không dùng UUP proxy trừ khi không có live data.
- **Học được:** Khi proxy data (UUP → DXY), phải verify timestamp. Proxy từ UUP có thể stale nếu UUP ETF tracking đã drift.

### 🟡 MAJOR — Oil WTI uses `~$` prefix for commodity price
- **Category:** 4.3 Arithmetic & Units
- **Rule:** New pattern (prefix notation)
- **Vị trí:** 11:30AM report, bảng Commodities & Yields
- **Quote:** `Oil WTI | ~$102 | Giảm sâu | -3.91% (prev close)`
- **Vấn đề:** 
  1. `~$` prefix cho commodity price — dấu `~` biểu thị "approximate" nhưng không cần thiết trong report chính thức. 
  2. Change column ghi "Giảm sâu" thay vì số points change (như format các báo cáo khác).
  3. Oil price format `$102.68` (không ~) nên đồng nhất.
- **Cách sửa:** Dùng exact hoặc rounded number: `102.68` hoặc `102.7`. Change column: absolute value như các rows khác.
- **Học được:** Format commodity price phải nhất quán across all reports. Không dùng `~` prefix.

### 🟡 MAJOR — DXY missing absolute change value
- **Category:** 4.2 Data Accuracy
- **Rule:** RULE-002
- **Vị trí:** 11:30AM report, bảng Commodities & Yields
- **Quote:** `DXY (Dollar Index) | 98.45 | — | +0.07%`
- **Vấn đề:** Cột "Thay đổi" chỉ có `—`. Missing absolute change value. Không thể xác định DXY thay đổi bao nhiêu points (dựa trên +0.07% và giá ~98.45 thì change ≈ +0.07, nhưng người đọc phải tự tính).
- **Cách sửa:** Đủ đầy đủ cả 3 cột: Price, Change (absolute), Change (%).
- **Học được:** Tất cả bảng giá phải có change column ở dạng absolute value, không chỉ %.

### 🟢 MINOR — Oil WTI price format inconsistent
- **Category:** 4.4 Format & Language
- **Vị trí:** 11:30AM report
- **Quote:** `~$102` (không có decimal)
- **Vấn đề:** Oil price chỉ có 0 decimal places (`$102`) trong khi các assets khác có 2 decimal (`7,268.03`, `25,348.42`). Không nhất quán về precision.
- **Cách sửa:** Commodity price nên có 2 decimal places: `$102.68`
- **Học được:** Precision standard: indices = 2 decimals, commodities = 2 decimals (hoặc 1 cho oil), yields = 4 decimals.

### 🟢 MINOR — Russell 2000 52w High < Current Price (logical inconsistency)
- **Category:** 4.6 Cross-Reference Consistency
- **Vị trí:** 11:30AM report, bảng Major Indices
- **Quote:** `Russell 2000 | 2,842.12 | 2,841.67 | 🔥 Phá ATH liên tục`
- **Vấn đề:** Current Price (2,842.12) > 52w High (2,841.67) — đây là hiện tượng "new ATH" nhưng bảng ghi 52w High là mức cũ (pre-breakout). 52w High phải được update lên mức mới hoặc ghi chú là "ATH just broke".
- **Cách sửa:** Khi ghi 52w High > current price → phải ghi chú rõ "new ATH" và dùng giá break level thay vì pre-ATH level.
- **Học được:** ATH breakout phải được ghi nhận rõ ràng trong 52w High column.

### 🟢 MINOR — VIX description says "từ 16.99" nhưng VIX 6AM report là +2.65%
- **Category:** 4.5 Logic & Reasoning
- **Rule:** RULE-006
- **Vị trí:** 11:30AM report, section "Biến động đáng chú ý"
- **Quote:** "VIX giảm sâu -5.8% — Xuống 17.23 (từ 16.99). Fear index thấp nhất kể từ tháng 3/2026."
- **Vấn đề:** "từ 16.99" có vẻ là Friday close nhưng VIX 6AM report ghi +2.65% từ 16.99 → 17.44. Vậy VIX đã tăng lên 17.44 trước khi giảm xuống 17.23. Narrative "từ 16.99" bỏ qua diễn biến intraday (tăng rồi giảm).
- **Cách sửa:** Narrative phải reflect full intraday journey: "từ 17.44 (6AM) xuống 17.23 (11:30AM), vẫn thấp hơn mức 18.28 của ngày trước"
- **Học được:** Khi VIX giảm so với prev day nhưng tăng intraday ngày hiện tại, narrative phải chính xác về timeline.

### 🟢 MINOR — "ISM Manufacturing Employment Index — 48 (mới) vs 45.2 (prior)"
- **Category:** 4.5 Logic & Reasoning
- **Vị trí:** 11:30AM report
- **Quote:** "48 (mới) vs 45.2 (prior), ngày 5/5 10:00 AM EDT. Cải thiện, tuy vẫn dưới 50 (contraction zone) nhưng xu hướng phục hồi."
- **Vấn đề:** ISM Manufacturing Employment là monthly data (tháng 4/2026), không phải ngày 5/5. Đây là dữ liệu được công bố ngày 5/5, nhưng giá trị 48 là cho tháng 4 (không phải tháng 5). Cách ghi "ngày 5/5 10:00 AM EDT" dễ gây hiểu nhầm là giá trị mới nhất của ngày 5/5.
- **Cách sửa:** "ISM Manufacturing Employment Index — 48 (tháng 4/2026) vs 45.2 (tháng 3/2026), công bố 5/5/2026 10:00 AM EDT"
- **Học được:** Economic data phải ghi rõ: (1) month covered, (2) release date, (3) prior value.

### 🟢 MINOR — Missing Gold price in 11:30AM report
- **Category:** 4.2 Data Accuracy
- **Vị trí:** 11:30AM report
- **Vấn đề:** 11:30AM report không có Gold trong bảng Commodities & Yields. Gold là một trong 5 tài sản chính cần theo dõi theo skill spec. 6AM report có GLD ($420.30). Quick report nên có ít nhất Gold cho completeness.
- **Cách sửa:** Quick update phải include Gold trong Commodities section.
- **Học được:** Template Quick Update phải yêu cầu ≥3 tài sản: Oil, Gold, 10Y Treasury.

## Hướng Dẫn Cho AI Report-Generator

1. **KHÔNG BAO GIỜ dùng chữ ngoài bộ ký tự Việt Nam** — scan output cho CJK characters (Chinese/Japanese/Korean). Nếu thấy → report bị hỏng.
2. **VIX change phải dùng common baseline** — cùng ngày, các report phải so với cùng prev close. Không mix baseline.
3. **Tất cả columns trong bảng giá phải đầy đủ** — Price, Change (absolute), %, 52w. Không được có column trống (`—`).
4. **Yield change phải dùng bp/pp** — RULE-011: `-0.030pp` hoặc `-3.0bp`, không dùng `-0.67%`.
5. **DXY phải live data** — không proxy qua UUP. Search `^DXY` trực tiếp từ Yahoo Finance.
6. **Commodity price format phải nhất quán** — không dùng `~` prefix, decimal places phải đều (2 digits).
7. **Economic data phải ghi rõ month covered + release date** — không ghi "ngày X" cho monthly data.
8. **Quick update phải có Gold** — ≥3 tài sản: Oil, Gold, 10Y Treasury.
9. **ATH breakout phải update 52w High** — khi index phá ATH, 52w High phải reflect giá trị mới.
10. **Intraday VIX narrative phải chính xác** — nếu VIX tăng rồi giảm trong ngày, narrative phải reflect full journey.

## Rules Mới Đề Xuất

### RULE-012 — Non-Vietnamese character scan (CJK detection)
- **Severity:** CRITICAL
- **Detection:** Regex `\p{IsCJKUnifiedIdeographs}` trong content → fail.
- **Anti-pattern:** "接近ATH" (Chinese chars in Vietnamese report)
- **Fix template:** Sau khi generate HTML, scan toàn bộ content cho CJK chars. Flag và remove before deploy.
- **Learned from:** 2026-05-05, bao-cao-tong-quan-thi-truong-thu-2-05052026-0600-a.html

### RULE-013 — Cross-report consistency for VIX
- **Severity:** MAJOR
- **Detection:** Khi có ≥2 reports cùng ngày, verify VIX prev close base là thống nhất.
- **Anti-pattern:** 6AM report VIX +2.65%, 11:30AM report VIX -5.80% (không reconcilable)
- **Fix template:** Store prev day close trong cache. Mỗi report phải so với cùng baseline.
- **Learned from:** 2026-05-05, cross-comparison của 6AM và 11:30AM reports.

## Checklist Cho Lần Report Tiếp Theo
- [ ] Build pipeline scan output cho CJK characters (CJK detection).
- [ ] Report generator đảm bảo tất cả table columns đầy đủ (không có `—`).
- [ ] Report generator dùng bp/pp cho yield change (RULE-011).
- [ ] Report generator DXY live search (không proxy).
- [ ] Quick update template phải có Gold ≥1 row.
- [ ] Cross-report cache: store prev day close để all reports trong cùng ngày dùng chung baseline.
- [ ] ATH breakout phải update 52w High trong cùng report.
- [ ] Economic data: ghi rõ month covered + release date.
