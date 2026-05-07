# AI Review Report for 2026-05-06-cap-nhat-thi-truong-2300-06052026
- **Report URL:** https://phanmaikienhung.github.io/market-report/2026-05-06-cap-nhat-thi-truong-2300-06052026.html
- **Report Date:** 2026-05-06
- **Review Date:** 2026-05-07
- **Reviewer:** AI Post-Deploy Reviewer (skill: review-deployed-report)
- **Verdict:** WARN

## Tổng Kết
Quick update 23:00 PDT chất lượng cao, cấu trúc rõ ràng, data chính xác cho hầu hết asset. Không có source name leak —合规 tốt. Có 1 vấn đề MAJOR (estimated RTY futures) và 2 MINOR (table formatting, BTC rounding). Nhìn chung report tốt, phù hợp với format quick update where overnight data có limited scope.
- 🔴 Critical: 0
- 🟡 Major: 1
- 🟢 Minor: 2

## Chi Tiết Lỗi

### 🟡 MAJOR — RTY Futures không có giá tuyệt đối (RULE-002 variant)
- **Category:** 4.2 (Data Accuracy)
- **Rule:** Không có specific rule ID nhưng dựa trên yêu cầu "Futures ES/NQ/YM/RTY: BẮT BUỘC có mức giá điểm cụ thể"
- **Vị trí:** Bảng Futures — "Russell 2000 (RTY) ~2,903 ~+16 ~+0.55%"
- **Vấn đề:** RTY futures có ~ prefix (estimated) thay vì giá tuyệt đối như ES, NQ, YM. MarketWatch search "rt00" không trả về data, không có source nào cho RTY futures tại thời điểm report.
- **Cách sửa:** Tìm RTY futures trên CMME website (cmegroup.com/markets/equities/russell2000.html) hoặc dùng API yfinance. Nếu không có, bỏ RTY ra khỏi bảng futures và thay bằng note "RTY futures không available".
- **Học được:** Khi cần RTY futures và không tìm được từ MarketWatch, thử CMCE hoặc CME group website — đừng dùng estimated value.

### 🟢 MINOR — BTC rounding
- **Category:** 4.2 (Data Accuracy)
- **Vị trí:** "BTC/USD $81,051 -$377.63 -0.46%"
- **Vấn đề:** BTC actual từ Google Finance: $81,051.22. Report ghi $81,051 — rounded xuống 1 dollar. Sai số $0.22 (negligible) nhưng không nhất quán với các asset khác đều giữ 2 decimal places.
- **Cách sửa:** Dùng giá chính xác hoặc làm tròn đến $.22 không phải $.00 — hoặc ghi "$81,051" (như report) nhưng chấp nhận rounded value.
- **Học được:** Crypto có thể rounded đến $1 (không cần 2 decimals) vì volatility cao — nhưng phải consistent. Report này OK vì BTC có volatility cao hơn indices.

### 🟢 MINOR — VIX không cần "%" ở change column
- **Category:** 4.3 (Arithmetic & Units)
- **Rule:** RULE-007 (VIX là volatility index, số raw, không %)
- **Vị trí:** Bảng Volatility — "10Y Treasury Yield ~4.35% — — (price: 110.797, flat)" và "30Y Treasury Bond ~4.94% — — (price: 113.688, +0.06)"
- **Vấn đề:** Yields section có column "%" nhưng values là "—" thay vì số, gây hiểu nhầm. Yield change nên ghi "-bp" hoặc "-pp" thay vì bỏ trống.
- **Cách sửa:** Ghi "— (flat)" hoặc bỏ column "%" đi cho row yield.
- **Học được:** Column header "%" nên match với content — nếu là yield change, dùng "-bp" notation thay vì "%".

## Hướng Dẫn Cho AI Report-Generator

1. **LUÔN tìm RTY futures trên CME Group website** (cmegroup.com/markets/equities/russell2000.html) nếu MarketWatch search không trả về — vì RTY có symbol khác (RT) không phải (RTY).
2. **KHÔNG BAO GIỜ dùng estimated value (~) cho futures table** — nếu không có giá, bỏ row đó ra. Futures table yêu cầu giá tuyệt đối.
3. **KHI viết yield/rate table** thì cột "%" nên ghi "-bp" hoặc "-pp" thay vì "—" để tránh hiểu nhầm và đúng convention.
4. **LUÔN verify BTC price từ Google Finance hoặc CoinGecko** — không dùng source MarketWatch cho crypto vì MarketWatch không có page crypto riêng cho BTC.
5. **CHECKLIST cho quick update overnight:** ES, NQ, YM đều có trên MarketWatch futures page; RTY cần source riêng (CME). Gold/Oil/DXY có trên Yahoo Finance hoặc MarketWatch.

## Rules Mới Đề Xuất

### RULE-016 — RTY futures phải tìm từ CME Group
- **Severity:** MAJOR
- **Detection:** Regex tìm "~" prefix trong bảng Futures
- **Anti-pattern:** "RTY ~2,903" trong bảng Futures
- **Fix template:** Khi cần RTY futures → search "RTY futures CME" hoặc truy cập cmegroup.com → không dùng estimated value
- **Learned from:** 2026-05-06, quick_update_2300.md (RTY futures không có giá tuyệt đối)

## Checklist Cho Lần Report Tiếp Theo

- [ ] Tìm RTY futures từ CME Group website (không từ MarketWatch)
- [ ] Verify tất cả futures có giá tuyệt đối (không ~ prefix)
- [ ] Format yield change column: dùng "-bp" thay vì "—" hoặc "%"
- [ ] Verify BTC price từ Google Finance hoặc CoinGecko
- [ ] Check column headers match data format (VIX = raw numbers, không %)
- [ ] Cross-check gold daily change between consecutive reports (consistency)
