# AI Review Report for 2026-05-06-bao-cao-phan-tich-thi-truong-chung-khoan-my-2
- **Report URL:** https://phanmaikienhung.github.io/market-report/2026-05-06-bao-cao-phan-tich-thi-truong-chung-khoan-my-2.html
- **Report Date:** 2026-05-06
- **Review Date:** 2026-05-07
- **Reviewer:** AI Post-Deploy Reviewer (skill: review-deployed-report)
- **Verdict:** WARN

## Tổng Kết

Báo cáo 3PM Full ngày 06/05/2026 là một bản phân tích toàn diện với 9 trụ cột phân tích, cross-reference matrix, convergence/divergence points, và market microstructure. Data accuracy về cơ bản tốt (S&P, Nasdaq, Dow, VIX verified từ MarketWatch), nhưng phát hiện 1 lỗi arithmetic nghiêm trọng (30Y yield % sai hệ số 10) + 1 character encoding issue (Chinese chars). Verdict: **⚠️ WARN** (6 🟡 Major, 3 🟢 Minor, 0 🔴 Critical).

- 🔴 Critical: 0
- 🟡 Major: 6
- 🟢 Minor: 3

## Chi Tiết Lỗi

### 🟡 MAJOR — Lỗi tính phần trăm thay đổi 30Y Treasury Yield (sai hệ số 10)

- **Category:** 4.3 — Arithmetic & Units (RULE-007)
- **Vị trí:** Section II.2 "Yields Curve & Bonds" — bảng 30Y Treasury Yield ghi `Change: -0.41, %: -0.82%`
- **Vấn đề:** Yield value 4.943% với change -0.41 → % decrease = (0.41 / 4.943) × 100 = **~8.3%**, không phải -0.82%. Lỗi này xuất hiện ở cả 3 rows 10Y, 30Y, 5Y — tất cả đều bị chia sai cho 10.
  - 10Y: (0.08 / 4.35) × 100 = **1.84%** (ghi nhận 1.80% → close)
  - 30Y: (0.41 / 4.943) × 100 = **8.29%** (ghi nhận **0.82%** → sai hệ số 10)
  - 5Y: (0.07 / 4.006) × 100 = **1.75%** (ghi nhận 1.79% → close, có thể do precision khác)
- **Cách sửa:** Recompute % change formula: `abs(change) / value * 100`. Verify với calculator trước khi write.
- **Học được:** Khi yield change nhỏ (0.01-0.41pp) so với yield value (~4-5%), percentage change thường nằm trong range 1-10%. Nếu % change < 1% với yield value ~5%, cần kiểm tra lại công thức.

### 🟡 MAJOR — Chinese characters in body text (RULE-005 cross-category)

- **Category:** 4.4 — Format & Language
- **Vị trí:** Section II.4 "Economic Data Highlights" — last paragraph: "Market đang chờ CPI tiếp theo để **确认** trend."
- **Vấn đề:** Chinese character "确认" (quèrèn) xuất hiện trong body text của Vietnamese report. Chữ này lẽ ra phải là tiếng Việt "xác nhận". Lỗi encoding hoặc LLM language mixing.
- **Cách sửa:** Lint pipeline: kiểm tra regex `[\u4e00-\u9fff]` trước khi deploy. Tất cả body text phải 100% Vietnamese.
- **Học được:** Nếu model đang xử lý mixed-language context (ví dụ: source data có Chinese), cần explicit language filter trước khi đưa vào report body.

### 🟡 MAJOR — BTC price labeled as "estimate" without clear uncertainty framing

- **Category:** 4.2 — Data Accuracy (RULE-002)
- **Vị trí:** Section V.4 "Bitcoin/Crypto" — "estimate **$82,000-$84,000**"
- **Vấn đề:** Report ghi BTC là "estimate" range $82K-$84K, trong khi các asset khác có verified price tại close. BTC là asset quan trọng cần include trong Full Report nhưng bị xử lý như estimate thay vì verified data.
- **Cách sửa:** Với BTC, nếu không thể fetch live price (login required), ghi rõ giá last-known và timeframe thay vì estimate range. Ví dụ: "BTC ~$81,000 (last known ~11:30AM PDT)".
- **Học được:** Không bao giờ dùng "estimate" cho asset prices trong financial reports — dùng "approximate" hoặc "last known" với timestamp rõ ràng.

### 🟡 MAJOR — Sector performance data mismatch (11:30AM vs market close)

- **Category:** 4.6 — Cross-Reference Consistency
- **Vị trí:** Section IV.1 "Sector Performance" — note "(từ data 11:30 AM PDT — close có thể có slight change)"
- **Vấn đề:** Full Report đóng cửa phiên nhưng sector data lấy từ 11:30AM PDT snapshot. Trong 2.5 giờ còn lại, các sector có thể có biến động đáng kể (đặc biệt Energy: oil từ 95.43 xuống 95.57, nhưng energy selloff có thể gia tăng).
- **Cách sửa:** Luôn lấy sector data gần nhất với close time. Nếu không có close data, ghi rõ "approximate" hoặc skip sector-level detail.
- **Học được:** Với Full Report (closing), tất cả numeric data phải từ session close hoặc intraday snapshot gần close nhất.

### 🟡 MAJOR — Timeline table: "09:30" column header says "Giờ PDT" but value is actually 9:30 AM ET

- **Category:** 4.7 — Time & Pipeline Compliance (RULE-003)
- **Vị trí:** Section I.1 "Timeline chi tiết phiên" — row "09:30" dưới column "Giờ PDT"
- **Vấn đề:** Column header "Giờ PDT" nhưng giá trị "09:30" tương ứng với 9:30 AM ET (market open), tức là 6:30 AM PDT. Điều này gây nhầm lẫn cho người đọc. Tương tự, "10:00-11:00" và "11:30" cũng là ET times được đặt trong column PDT.
- **Cách sửa:** Either: (a) đổi column header thành "Giờ ET" (consistent với session analysis), hoặc (b) convert tất cả sang PDT: "06:30", "07:00-08:00", "08:30".
- **Học được:** Khi table header nói "Giờ PDT", MỌI giá trị trong column đó phải là PDT time. Không bao giờ trộn lẫn ET/PDT trong cùng column.

### 🟡 MAVER — Dow stock prices không được cross-verify với close data

- **Category:** 4.2 — Data Accuracy (RULE-001)
- **Vị trí:** Section IV.2 "Key Stock Movers" — tất cả 15+ stock prices trong bảng
- **Vấn đề:** Stock prices như Disney $108.06, Nvidia $207.83, Honeywell $216.86, Boeing $229.93 được ghi nhưng không clear source (pre-market? 11:30? close?). Một số prices có thể không match actual close.
  - Ví dụ: Disney được ghi là $108.06 với +7.54% — nếu prev close ~$100.48, close ~$108.06. Cần verify với closing data.
  - Nvidia được ghi là $207.83 với +5.77% — prev close 25,326.13 → cần verify Dow component price.
- **Cách sửa:** Cross-verify stock prices với closing data từ MarketWatch/Finance.yahoo.com. Chỉ ghi close prices cho Full Report.
- **Học được:** Với Full Report, tất cả stock prices phải từ market close. Nếu không thể verify, ghi rõ "pre-market" hoặc "approximate".

### 🟢 MINOR — "Confirmed" English/Vietnamese language mixing in headlines table

- **Category:** 4.4 — Format & Language
- **Vị trí:** Quick Headlines row 4: "ALL FOUR MAJOR INDICES AT ATH"
- **Vấn đề:** Text tiếng Anh trong midst of Vietnamese report — "ALL FOUR MAJOR INDICES AT ATH". Không nghiêm trọng nhưng nên dùng Vietnamese equivalent: "TẤT CẢ 4 CHỈ SỐ CHÍNH ĐẠT MỨC CAO MỚI".
- **Học được:** Toàn bộ report nên đồng nhất tiếng Việt. Tiếng Anh chỉ dùng cho terms kỹ thuật không có tương đương (ATH, yield, sector).

### 🟢 MINOR — 52W High table has markdown formatting issue in HTML

- **Category:** 4.4 — Format & Language
- **Vị trí:** Section I.1 — row "13:00": cell nội dung "**S&P 52W High: 7,369.22**" followed by text "Nasdaq 52W High: 25,850.19"
- **Vấn đề:** Trong markdown source, "**S&P 52W High: 7,369.22**" với bold markers được render đúng, nhưng row này trông giống như có 2 cột dữ liệu (S&P và Nasdaq) trong cùng 1 cell. Trong HTML rendered, nó có thể bị hiển thị sai layout.
- **Cách sửa:** Tách thành 2 row hoặc 2 column rõ ràng: một column cho S&P 52W High, một cho Nasdaq 52W High.
- **Học được:** Khi table row có multiple data points, đảm bảo mỗi data point trong column riêng biệt. Không put markdown formatting trong data cells.

### 🟢 MINOR — "Powell speech 2PM EDT" vs PDT table conversion

- **Category:** 4.7 — Time & Pipeline Compliance (RULE-003)
- **Vị trí:** Quick Headlines row 6: "Powell speech 2PM EDT: Treasury signal không thay đổi front-loading borrowing"
- **Vấn đề:** "2PM EDT" được ghi trong headline table. EDT trong May là UTC-4, tương đương PDT (UTC-7) là 11AM PDT, không phải 7AM PDT. Tuy nhiên trong timeline section I.1 ghi "Powell speech (2PM ET = 7AM PDT)" — conversion này đúng cho ET, không phải EDT. Trong May (EDT), 2PM EDT = 11AM PDT, không phải 7AM PDT.
- **Cách sửa:** Dùng "2PM ET" thay vì "2PM EDT" trong headline (ET là standard reference). Trong timeline, ghi "2PM ET = 11AM PDT" (EDT hiện tại).
- **Học được:** Luôn dùng "ET" thay vì "EDT/EST" trong reports để tránh confusion. ET trong summer = EDT = UTC-4.

## Hướng Dẫn Cho AI Report-Generator

1. **LUÔN kiểm tra percent change công thức** `(change / original * 100)` cho yield data — vì yield change nhỏ (0.01-0.41pp) so với yield value (~4-5%), percentage change sẽ nằm trong range 1-10%. Nếu kết quả < 1% với yield ~5%, có thể bị sai hệ số 10.

2. **KHÔNG BAO GIỜ để Chinese/Japanese characters trong body text** — build encoding lint step: kiểm tra regex `[\u4e00-\u9fff]` trước khi generate report. Nếu gặp character trong range này → replace với Vietnamese equivalent.

3. **KHI tạo timeline table với column "Giờ PDT"** — tất cả giá trị trong column đó PHẢI là PDT time. Nếu source data là ET time, convert thành PDT trước khi insert vào table.

4. **KHI viết Full Report closing** — tất cả numeric data (sector, stock prices, indices) phải từ market close hoặc intraday snapshot gần nhất (<30min từ close). Không dùng 11:30AM data cho closing report mà không có disclaimer rõ ràng.

5. **LUÔN verify stock prices với closing data** — dùng MarketWatch closing prices cho Dow components. Pre-market or 11:30 prices có thể khác đáng kể so với close (đặc biệt với earnings movers như Disney +7.54%).

## Rules Mới Đề Xuất

### RULE-016 — Yield percentage change phải sanity check
- **Severity:** MAJOR
- **Detection:** Khi yield value ~4-5% và yield change < 0.5pp, verify % change = (change / yield * 100). Nếu % change < 1% với change > 0.1pp → FLAG.
- **Anti-pattern:** 30Y: 4.943% (-0.41) ghi là -0.82% thay vì ~8.3%
- **Fix template:** `pct = abs(change) / value * 100; if pct < 1 and abs(change) > 0.1: print("WARN: possible decimal error")`
- **Learned from:** 2026-05-06, bao_cao_thi_truong_20260506_3PM.md (30Y yield %)

### RULE-017 — Encoding check before deploy
- **Severity:** MAJOR
- **Detection:** Regex `[\u4e00-\u9fff]` trên toàn bộ body text
- **Anti-pattern:** "Market đang chờ CPI tiếp theo để确认 trend" — Chinese char "确认"
- **Fix template:** Pre-deploy filter: remove/replace any CJK characters with Vietnamese equivalent
- **Learned from:** 2026-05-06, bao_cao_thi_truong_20260506_3PM.md (Chinese char in section 2.4)

## Checklist Cho Lần Report Tiếp Theo
- [ ] Verify tất cả yield % change: `abs(change) / yield * 100` → sanity check: yield ~5%, change 0.41pp → % ~8%
- [ ] Check encoding: grep `[\u4e00-\u9fff]` trên body text trước khi deploy
- [ ] Timeline column "Giờ PDT" — convert tất cả ET times sang PDT trước khi insert
- [ ] Full Report sector data: lấy từ market close hoặc intraday snapshot <30min từ close
- [ ] Stock prices: verify với closing prices, không chỉ pre-market hoặc midday
- [ ] BTC/Crypto: nếu không thể fetch live, ghi "last known at [time]" thay vì "estimate"
- [ ] Language check: đảm bảo 100% Vietnamese body text, English chỉ dùng cho terms kỹ thuật
