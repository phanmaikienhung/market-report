# AI Review Report for 2026-05-06-cap-nhat-thi-truong-1130-06052026
- **Report URL:** https://phanmaikienhung.github.io/market-report/2026-05-06-cap-nhat-thi-truong-1130-06052026.html
- **Report Date:** 2026-05-06
- **Review Date:** 2026-05-06
- **Reviewer:** AI Post-Deploy Reviewer (skill: review-deployed-report)
- **Verdict:** WARN

## Tổng Kết
Quick update 11:30 AM PDT chất lượng cao. Dữ liệu indices, commodities, FX và sectors đều chính xác và match live data. Một vấn đề chính: inconsistency giữa giá WTI trong bảng (~$94.79, từ ground truth live) và trong narrative ($94.38, từ snapshot 11:30), dẫn đến percent change khác nhau (~-5.7% vs -7.71%). Ngoài ra có 2 minor formatting issues.

- 🔴 Critical: 0
- 🟡 Major: 1
- 🟢 Minor: 2

## Chi Tiết Lỗi

### 🟡 MAJOR — WTI Price & % Change Inconsistency (Table vs Narrative)
- **Category:** 4.2 Data Accuracy / 4.6 Cross-Reference Consistency
- **Table:** `WTI Crude | $94.79 | ~-5.7% | ~-5.7%` (dùng ground truth live data)
- **Narrative:** `WTI giảm sâu từ $95.34 (9AM) xuống $94.38 (-7.71%)`
- **Vấn đề:** Bảng và narrative dùng hai giá WTI khác nhau ($94.79 vs $94.38) dẫn đến % change khác nhau (~-5.7% vs -7.71%). Ground truth live data (yfinance) cho WTI $94.79 với prev close $100.53 → ~-5.7%. Giá $94.38 với prev close ~$102.27 → -7.71%. Đây là conflict giữa hai nguồn dữ liệu/timestamp khác nhau.
- **Cách sửa:** Dùng duy nhất một nguồn giá cho cả table và narrative. Prefer live yfinance data cho cả hai. Nếu so sánh intraday (9AM → 11:30AM), ghi rõ "from 9AM price" và tính % change từ đó.
- **Học được:** Khi viết quick update so sánh với baseline, tính % change từ baseline price (9AM) cho intraday comparison, và từ prev close cho daily change — phân biệt rõ hai metric này.

### 🟢 MINOR — English word "gains" in Vietnamese summary
- **Category:** 4.4 Format & Language
- **Vị trí:** Tóm tắt paragraph: `S&P 500 và Nasdaq mở rộng gains`
- **Vấn đề:** Từ tiếng Anh "gains" xuất hiện trong báo cáo tiếng Việt. Mặc dù từ vựng tài chính tiếng Anh thường được chấp nhận, nhưng để consistent với toàn bộ report (vẫn dùng tiếng Việt thuần túy), nên thay bằng "mở rộng" hoặc "tăng thêm".
- **Cách sửa:** `S&P 500 và Nasdaq mở rộng đà tăng` hoặc `S&P 500 và Nasdaq tiếp tục tăng`
- **Học được:** Giữ toàn bộ body report bằng tiếng Việt thuần túy (hoặc tối thiểu hóa English loanwords).

### 🟢 MINOR — Duplicate % column in table header
- **Category:** 4.4 Format & Language
- **Vị trí:** Tất cả tables: `| Index | Giá | Thay đổi | % | 52W High |`
- **Vấn đề:** Cột "%" (percentage change) bị lặp — một cột "Thay đổi" ghi % và một cột "%" cũng ghi %. Ví dụ: `| S&P 500 | 7,353.73 | +1.30% | +1.30% | 7,348.35 |`. Đây có thể là render issue từ build script (markdown → HTML).
- **Cách sửa:** Dùng 1 cột duy nhất ghi "% Change" hoặc tách thành "Giá" và "% Change".
- **Học được:** Sau khi viết markdown table, preview HTML để check column duplication trước khi deploy.

## Hướng Dẫn Cho AI Report-Generator
1. **LUÔN dùng cùng một source giá cho cả table và narrative** — vì mismatch giữa sources (Yahoo Finance snapshot vs yfinance live) sẽ tạo inconsistency trong cùng report. Prefer yfinance live data cho cả hai.

2. **LUÔN phân biệt intraday % change vs daily % change** — khi so sánh với baseline (9AM), ghi rõ "% từ 9AM" cho intraday và "% từ prev close" cho daily. Không gộp chung.

3. **KHÔNG BAO GIỜ mix English words vào body Vietnamese** — kể cả từ tài chính phổ biến như "gains", "breakout", "rally". Dùng tiếng Việt tương đương.

4. **KHI viết quick update so sánh với baseline**, tính delta % từ baseline price: `(current - baseline) / baseline * 100`. Ví dụ: WTI 9AM $95.34 → 11:30 $94.79 = -0.57%, KHÔNG dùng daily change (-5.7%) cho intraday comparison.

## Rules Mới Đề Xuất

### RULE-016 — Quick update baseline comparison: intraday delta must use baseline price as denominator
- **Severity:** MAJOR
- **Detection:** Khi có phrase so sánh với baseline (9AM/6AM), kiểm tra % change được tính từ baseline price hay từ prev close
- **Anti-pattern:** "Oil -7.71% từ 9AM" khi -7.71% là daily change (từ prev close), không phải intraday change (từ 9AM price)
- **Fix template:** 
  ```
  daily_change = (current - prev_close) / prev_close * 100
  intraday_from_baseline = (current - baseline_price) / baseline_price * 100
  Ghi rõ: "daily -7.71% (từ prev close) / intraday -0.6% (từ 9AM)"
  ```
- **Learned from:** 2026-05-06, quick_update_1130.md (WTI -7.71% vs -0.57%)

## Checklist Cho Lần Report Tiếp Theo
- [ ] Dùng yfinance live data cho TẤT CẢ giá trong cả table và narrative (không mix Yahoo Finance snapshot)
- [ ] Tính intraday delta % từ baseline price, daily delta % từ prev close — phân biệt rõ
- [ ] Verify mỗi % change trong narrative bằng cách tính lại từ price đã ghi
- [ ] Toàn bộ body tiếng Việt — không English loanwords trừ ticker symbols
- [ ] Preview HTML table trước deploy để check duplicate columns
