# AI Review Report for 2026-05-08-cap-nhat-thi-truong-2000-08052026
- **Report URL:** https://phanmaikienhung.github.io/market-report/2026-05-08-cap-nhat-thi-truong-2000-08052026.html
- **Report Date:** 2026-05-08
- **Review Date:** 2026-05-09
- **Reviewer:** AI Post-Deploy Reviewer (skill: review-deployed-report)
- **Verdict:** WARN

## Tổng Kết
Quick Update 20:00 PDT — báo cáo sau-hours Memorial Day Early Close. Dữ liệu indices và commodities chính xác, format tiếng Việt tốt, không source name leak. Tuy nhiên có **lỗi dữ liệu USD/JPY nghiêm trọng** (giá trị 0.6401 sai hoàn toàn so với giá trị thực ~155+) — khả năng bị nhầm symbol hoặc data source. Verdict **WARN** do 1 lỗi MAJOR (USD/JPY) + 2 lỗi MINOR.

- 🔴 Critical: 0
- 🟡 Major: 1
- 🟢 Minor: 2

## Chi Tiết Lỗi

### 🟡 MAJOR — USD/JPY giá trị sai hoàn toàn

- **Category:** 4.2 Data Accuracy — RULE-001
- **Vị trí:** "### Bonds & FX" section
- **Quote:** "USD/JPY | 0.6401 | +0.0001 | +0.02%"
- **Vấn đề:** USD/JPY hiện tại (~May 2026) phải vào khoảng 150+, không phải 0.6401. Giá trị 0.6401 có thể là EUR/JPY hay một cross-rate khác bị gán nhầm symbol. Đây là lỗi data source/caption sai, gây hiểu nhầm nghiêm trọng cho người đọc.
- **Cách sửa:** Kiểm tra kỹ symbol trước khi ghi vào report. Dùng MarketWatch hoặc Yahoo Finance để verify từng symbol cụ thể. Nếu không có dữ liệu USD/JPY → bỏ qua section FX hoặc ghi "Unavailable".
- **Học được:** FX pairs cần verify symbol chính xác. Không copy-paste data từ source khác mà không kiểm tra label.

### 🟢 MINOR — EUR/USD change +0.31% không xác minh độc lập

- **Category:** 4.2 Data Accuracy — RULE-001
- **Vị trí:** "### Bonds & FX" section
- **Quote:** "EUR/USD | 1.1807 | +0.0036 | +0.31%"
- **Vấn đề:** Giá trị 1.1807 match MarketWatch, nhưng change +0.0036 / +0.31% không được verify độc lập. Recomputed: (1.1807 - 1.1771) / 1.1771 × 100 = +0.31% → khớp. Nhưng chỉ dựa vào 1 source (MarketWatch).
- **Cách sửa:** Với FX, thêm 1 source check (ví dụ: OANDA, Investing.com) cho các giá trị quan trọng.
- **Học được:** FX data cần ≥1 source cross-check ngoài MarketWatch.

### 🟢 MINOR — NDX (NASDAQ 100) không có trong MarketWatch snapshot ban đầu

- **Category:** 4.2 Data Accuracy — RULE-001
- **Vị trí:** "### Equity Indices" section
- **Quote:** "NASDAQ 100 (.NDX) | 29,234.99 | +671.05 | +2.35%"
- **Vấn đề:** Giá trị này được lấy từ MarketWatch sau-hours snapshot, không được cross-check với source khác. NDX có thể có slight discrepancy so với Nasdaq Composite.
- **Cách sửa:** NDX nên verify với Nasdaq.com hoặc Investing.com để đảm bảo accuracy.
- **Học được:** Khi report NDX, nên cross-check ít nhất 1 source bổ sung.

## Hướng Dẫn Cho AI Report-Generator

1. **LUÔN verify USD/JPY value nằm trong range ~140-160** — vì đây là tỷ giá thường day và sai số 100x (ghi 0.64 thay vì 155+) là lỗi critical dễ phát hiện khi sanity-check.
2. **KHÔNG copy FX data từ MarketWatch mà không kiểm tra symbol labels** — vì MarketWatch hiển thị nhiều currency pairs và có thể nhầm label nếu copy-paste từ section khác.
3. **KHI không có dữ liệu cho một asset cụ thể** thì bỏ qua hoàn toàn — không điền giá trị từ asset khác (vd EUR/JPY vào slot USD/JPY).
4. **LUÔN sanity-check tỷ giá JPY** — USD/JPY > 100 luôn. Nếu thấy giá trị < 10 → nghi ngờ ngay.

## Rules Mới Đề Xuất

### RULE-016 — USD/JPY sanity check phải nằm trong range hợp lý
- **Severity:** MAJOR
- **Detection:** Regex match `USD/JPY` kèm giá trị < 130 hoặc > 200
- **Anti-pattern:** "USD/JPY 0.6401" — sai 2 orders of magnitude
- **Fix template:** Sanity check: 130 ≤ USD/JPY ≤ 200 (range hợp lý historical 2024-2026). Nếu ngoài range → flag error.
- **Learned from:** 2026-05-08, quick_update_2000 (USD/JPY 0.6401)

## Checklist Cho Lần Report Tiếp Theo
- [ ] Sanity-check USD/JPY > 100 trước khi ghi vào report
- [ ] Cross-check ít nhất 1 FX pair (EUR/USD) với source ngoài MarketWatch
- [ ] Verify NDX với 1 source bổ sung (Nasdaq.com hoặc Investing.com)
- [ ] Kiểm tra kỹ symbol labels khi copy FX data từ MarketWatch
