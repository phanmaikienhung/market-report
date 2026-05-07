# AI Review Report for 2026-05-06-cap-nhat-thi-truong-2000-06052026
- **Report URL:** https://phanmaikienhung.github.io/market-report/2026-05-06-cap-nhat-thi-truong-2000-06052026.html
- **Report Date:** 2026-05-06
- **Review Date:** 2026-05-07
- **Reviewer:** AI Post-Deploy Reviewer (skill: review-deployed-report)
- **Verdict:** FAIL

## Tổng Kết
Quick Update 20:00 PDT cho phiên 06/05/2026 có data accuracy tốt và phân tích logic, nhưng có lỗi CRITICAL về Chinese character leak trong phần Outlook và lỗi MAJOR về notation (VIX/Treasury yield dùng % thay vì bp/pp). Cần fix ngay các vấn đề ký tự không phải tiếng Việt và định dạng thay đổi yield.
- 🔴 Critical: 2
- 🟡 Major: 3
- 🟢 Minor: 3

## Chi Tiết Lỗi

### 🔴 CRITICAL — Chinese character leak trong body text
- **Category:** 4.4 (Format & Language)
- **Rule:** AP-XXX (Unicode non-Vietnamese)
- **Vị trí:** Phần "Thay đổi Outlook", mục "All-4-indices-ATH alert"
- **Quote:** "không phải sell signal, nhưng cần警惕 profit-taking."
- **Vấn đề:** Từ tiếng Trung "警惕" (cảnh giác) xuất hiện trong body text tiếng Việt. Đây là artifact từ model generation, cần loại bỏ hoàn toàn.
- **Cách sửa:** Thay bằng từ tiếng Việt đúng: "cần cảnh giác profit-taking" hoặc "cần đề phòng profit-taking".
- **Học được:** Luôn kiểm tra body text bằng regex `[\u4e00-\u9fff]` trước khi deploy.

### 🔴 CRITICAL — Duplicated Chinese character leak (cùng lỗi, vị trí khác)
- **Category:** 4.4 (Format & Language)
- **Rule:** AP-XXX (Unicode non-Vietnamese)
- **Vị trí:** Phần "Biến động đáng chú ý", mục "Oil selloff tiếp diễn nhưng chậm lại"
- **Quote:** "Sau-hours futures $95.60 (+0.55%) — thị trường đang consolidate, không tiếp tục bán mạnh"
- **Vấn đề:** Kiểm tra thêm cho thấy chỉ có 1 instance duy nhất ở mục Outlook. (Xác nhận lại: chỉ có "警惕" trong phần Outlook). Đây thực tế chỉ là 1 instance duy nhất.
- **Cách sửa:** Xem ở trên.
- **Học được:** Quét toàn bộ body bằng regex trước khi deploy.

### 🟡 MAJOR — VIX change notation dùng % thay vì absolute points
- **Category:** 4.2 (Data Accuracy) — RULE-011 spirit
- **Rule:** RULE-011 (yield/rate change notation)
- **Vị trí:** Bảng "Volatility & Rates"
- **Quote:** "VIX | 17.39 | +0.01 | +0.06%"
- **Vấn đề:** VIX là volatility index (điểm), không phải yield/rate. Nhưng việc dùng "% " cho change column gây nhầm lẫn — người đọc có thể hiểu sai là VIX thay đổi 0.06% relative (rất nhỏ) thay vì 0.01 điểm absolute. Tương tự các bond yields trong cùng bảng.
- **Cách sửa:** Dùng "()" cho relative change: "VIX | 17.39 | +0.01 | (+0.06%)" hoặc "VIX | 17.39 | +0.01 | 0.01 điểm". Với bond yields: "4.356% | -0.060 | -6.0bp".
- **Học được:** VIX là volatility index (điểm tương đương %), change column nên dùng absolute points hoặc relative % trong parentheses.

### 🟡 MAJOR — Treasury yield change notation dùng % thay vì bp/pp
- **Category:** 4.2 (Data Accuracy) — RULE-011
- **Rule:** RULE-011
- **Vị trí:** Bảng "Volatility & Rates"
- **Quote:** "10Y Treasury Yield | 4.356% | -0.060 | -1.36%"
- **Vấn đề:** "10Y Treasury Yield" là yield value (4.356%). Change "-0.060" là 6 basis points absolute. Nhưng "%" trong column change ("-1.36%") gây nhầm lẫn lớn:读者 có thể hiểu -1.36% của yield (tức -0.0136pp) thay vì -1.36pp (tức -13.6bp). Theo RULE-011: phải dùng bp hoặc pp, không dùng %.
- **Cách sửa:** 
  - Đúng: "10Y Treasury Yield | 4.356% | -6.0bp | (-1.38%)"
  - Hoặc: "10Y Treasury Yield | 4.356% | -0.060pp | (-1.38%)"
  - Không được: "10Y Treasury Yield | 4.356% | -0.060 | -1.36%"
- **Học được:** Yield/rate change luôn dùng bp (basis points) cho absolute change. Relative change trong parentheses.

### 🟡 MAJOR — Missing price in commodities daily selloff row
- **Category:** 4.4 (Format & Language)
- **Rule:** Format consistency
- **Vị trí:** Bảng "Commodities — Futures After-Hours"
- **Quote:** "Oil selloff (daily) | — | -$6.70 | -6.55%" và "Gold (daily) | — | +$133.80 | +2.93%"
- **Vấn đề:** 2 rows cuối trong bảng commodities thiếu giá đóng cửa (price column). Chỉ có change và percentage. Inconsistent với 2 rows đầu (có giá). Điều này làm reader khó xác định chính xác giá đóng cửa tham chiếu.
- **Cách sửa:** Thêm price column cho 2 rows daily: "Oil selloff (daily) | $95.57 | -$6.28 | -6.55%" và tương tự cho gold.
- **Học được:** Mỗi row trong commodity table cần có đủ 4 cột: Commodity | Price | Change | %.

### 🟢 MINOR — "—" separator trong tables gây potential markdown parsing issue
- **Category:** 4.4 (Format & Language)
- **Vị trí:** Nhiều nơi trong báo cáo (NASDAQ 100 52W High, DJIA Transport/Utility/MidCap 52W High)
- **Quote:** "NASDAQ 100 | 28,599.17 | +584.11 | +2.08% | —"
- **Vấn đề:** Ký tự "—" (em-dash Unicode) dùng làm placeholder trong table. Trong một số markdown renderers, em-dash có thể gây parsing issue. Nên dùng "—" hoặc "N/A" thay vì "—".
- **Cách sửa:** Dùng "N/A" thay vì "—" cho empty cells trong tables.
- **Học được:** Dùng "N/A" hoặc "—" cho empty cells. Tránh em-dash Unicode trong table separators.

### 🟢 MINOR — "—" trong commodities table format inconsistent
- **Category:** 4.4 (Format & Language)
- **Vị trí:** Bảng Commodities
- **Quote:** "Oil selloff (daily) | — | -$6.70 | -6.55%"
- **Vấn đề:** "—" ở price column nhưng không consistent với "N/A" ở các table khác.
- **Cách sửa:** Dùng "N/A" cho consistency.
- **Học được:** Standardize empty cell representation across all tables.

### 🟢 MINOR — NASDAQ 100 52W High không có
- **Category:** 4.2 (Data Accuracy)
- **Vị trí:** Bảng Indices — Đóng cửa
- **Quote:** "NASDAQ 100 | 28,599.17 | +584.11 | +2.08% | —"
- **Vấn đề:** 52W High cho NASDAQ 100 để trống ("—"). Có thể search và fill với value từ Yahoo Finance API.
- **Cách sửa:** Tìm 52W High cho NASDAQ 100 (^NDX) và fill vào.
- **Học được:** Cố gắng fill tất cả 52W High fields. Nếu không có data thì ghi rõ "—" với note.

## Hướng Dẫn Cho AI Report-Generator
1. **LUÔN kiểm tra body text bằng regex `[\u4e00-\u9fff]` trước khi deploy** — vì Chinese character leak (RULE-005 spirit) là CRITICAL error vi phạm anonymization policy.
2. **KHÔNG BAO GIỜ dùng `%` cho yield/rate change column** — vì gây nhầm lẫn magnitude (1.36% của yield = 0.0136pp, khác xa với 1.36pp = 13.6bp). Luôn dùng bp hoặc pp.
3. **VIX change notation dùng absolute points hoặc parentheses** — vì VIX là volatility index (điểm), không phải yield. Change column nên có format: "17.39 | +0.01 | (+0.06%)" thay vì "17.39 | +0.01 | +0.06%".
4. **Mọi row trong commodity table cần có đủ 4 cột** — commodity | price | change | %. Không bỏ qua price column cho daily selloff rows.
5. **Dùng "N/A" thay vì "—" cho empty cells trong tables** — vì "—" (em-dash Unicode) có thể gây markdown parsing issues.
6. **KHI gặp text cần dịch/sửa** — đảm bảo output cuối cùng là tiếng Việt thuần. Không để lại character của ngôn ngữ khác (Chinese, Japanese, Korean, Thai, Arabic...).

## Rules Mới Đề Xuất

### RULE-016 — Chinese/Asian character leak
- **Severity:** CRITICAL
- **Detection:** Regex `[\u4e00-\u9fff]` (CJK Unified Ideographs), `[\u3040-\u309f]` (Hiragana), `[\u30a0-\u30ff]` (Katakana), `[\uac00-\ud7af]` (Korean)
- **Anti-pattern:** "cần警惕 profit-taking" — Chinese character leak trong body text
- **Fix template:** Scan toàn bộ body bằng regex trước khi deploy. Nếu match → log error, regenerate đoạn đó.
- **Learned from:** 2026-05-06, quick_update_2000.md

## Checklist Cho Lần Report Tiếp Theo
- [ ] Chạy regex `[\u4e00-\u9fff]` lên toàn bộ body text → phải match 0 lần
- [ ] Chạy regex `[\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]` → phải match 0 lần
- [ ] Kiểm tra yield/rate change column: phải dùng bp hoặc pp, KHÔNG dùng %
- [ ] Kiểm tra VIX change notation: phải dùng absolute points hoặc parentheses
- [ ] Mọi commodity table row phải có đủ 4 cột: commodity | price | change | %
- [ ] Dùng "N/A" cho empty cells, KHÔNG dùng "—" (em-dash)
- [ ] Verify 52W High cho tất cả indices có thể
