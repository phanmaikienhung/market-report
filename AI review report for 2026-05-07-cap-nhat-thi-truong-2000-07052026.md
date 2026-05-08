# AI Review Report for 2026-05-07-cap-nhat-thi-truong-2000-07052026
- **Report URL:** https://phanmaikienhung.github.io/market-report/2026-05-07-cap-nhat-thi-truong-2000-07052026.html
- **Report Date:** 2026-05-07
- **Review Date:** 2026-05-08
- **Reviewer:** AI Post-Deploy Reviewer (skill: review-deployed-report)
- **Verdict:** ⚠️ WARN

## Tổng Kết
Report After-Hours 20:00 hôm nay chất lượng tốt — dữ liệu giá indices/commodities/XF đa số chính xác, cấu trúc nhanh gọn dễ đọc, source citation hợp lý. Tuy nhiên có **2 lỗi arithmetic** ở bảng Commodities (WTI % change sai 0.10pp, Brent round 3.87% → 3.88%) và **lỗi format yield** dùng % thay vì bp (RULE-011). Tổng thể cần fix arithmetic trước khi deploy.
- 🔴 Critical: 0
- 🟡 Major: 3
- 🟢 Minor: 2

## Chi Tiết Lỗi

### 🟡 MAJOR — WTI Crude Oil % change arithmetic error (RULE-007 / AP-005)
- **Category:** 4.3 Arithmetic & Units
- **Rule:** RULE-007 (Arithmetic must be verified)
- **Vị trí:** `"WTI Crude (Jun) | $95.45 | +$1.59 | +1.59% | Từ $93.86 close"`
- **Vấn đề:** Dollar change $1.59 được copy nhầm thành percentage. Actual: `(95.45 - 93.86) / 93.86 × 100 = 1.694% ≈ 1.69%`, không phải 1.59%. Lỗi này xuất hiện vì reporter lấy ngay số dollar change (`$1.59`) và gắn luôn dấu `%` → `1.59%`. Delta 0.10pp có vẻ nhỏ nhưng trong oil market ($95/barrel), 0.10pp = $0.095/barrel — có thể ảnh hưởng decision-making.
- **Cách sửa:** Tính % change độc lập: `round((AH_close - close) / close * 100, 1)`. Đừng copy dollar value làm % value.
- **Học được:** Dollar change và percentage change là 2 số khác nhau — KHÔNG bao giờ lấy số dollar rồi gắn % vào.

### 🟡 MAJOR — Brent Crude % change rounding error (RULE-007 / AP-005)
- **Category:** 4.3 Arithmetic & Units
- **Rule:** RULE-007
- **Vị trí:** `"Brent Crude (Jul) | $101.44 | +$3.78 | +3.88% | ⚡ Vượt mốc $100!"`
- **Vấn đề:** `(101.44 - 97.66) / 97.66 × 100 = 3.8705%` → đúng phải là **3.87%** (làm tròn 1 decimal). Report ghi 3.88% — sai 0.01pp. Lỗi này có thể do làm tròn intermediate values trước khi tính.
- **Cách sửa:** Dùng giá trị chính xác từ 2 nguồn (3PM close + AH price), tính delta, round 1 decimal. Không làm tròn intermediate.
- **Học được:** Tính `% = delta/old_value` với full precision, chỉ round ở bước cuối cùng.

### 🟡 MAJOR — Treasury yield changes dùng % thay vì bp (RULE-011)
- **Category:** 4.3 Arithmetic & Units
- **Rule:** RULE-011 (Yield/rate change phải ghi bp hoặc pp, không dùng %)
- **Vị trí:** `"US 2Y | 3.9090% | +~3bp | +~0.08%"` và `"US 10Y | 4.3860% | +~6bp | +~0.14%"` và `"US 30Y | 4.9660% | +~10bp | +~0.20%"`
- **Vấn đề:** Theo RULE-011, yield changes không được có `%` vì gây nhầm lẫn magnitude (25x). `+~0.08%` cho 2Y yield có thể hiểu nhầm là +8bp thay vì +0.08pp. Nên bỏ cột % hoặc đổi sang pp/bp.
- **Cách sửa:** Cột "Thay đổi" của Treasuries dùng bp (basis points). Bỏ cột % hoàn toàn cho Treasuries section.
- **Học được:** Yield = percentage, nên yield CHANGE phải dùng bp (1bp = 0.01%) hoặc pp (1pp = 1%). Không dùng % cho yield change.

### 🟢 MINOR — Redundant "20:00 PM" notation
- **Category:** 4.4 Format & Language
- **Rule:** General formatting guideline
- **Vị trí:** `"Từ 3PM Full Report → 20:00 PM After-Hours:"`
- **Vấn đề:** "20:00 PM" là redundant notation — 20:00 đã là 24h format, không cần "PM" phía sau. Nên dùng "20:00" hoặc "8:00 PM" (không trộn lẫn).
- **Cách sửa:** Dùng nhất quán 1 định dạng thời gian — hoặc 24h (`20:00`) hoặc 12h với AM/PM (`8:00 PM`).
- **Học được:** Không trộn lẫn 24h và 12h format trong cùng biểu tượng thời gian.

### 🟢 MINOR — ~ markers trên Silver/Copper thay vì estimated value
- **Category:** 4.4 Format & Language
- **Rule:** General data quality
- **Vị trí:** `"Silver | $80-82 | ~+~$3 | ~+~3.8%"`
- **Vấn đề:** Các giá trị `~+~$3` và `~+~3.8%` khó đọc và không follow convention `~+3.8%`. `~+~$3` đặc biệt confusing.
- **Cách sửa:** Dùng format `~$80-82 | ~+$3 | ~+3.8%` (dấu ~ đứng trước giá trị, không xen giữa).
- **Học được:** Format `~value` — dấu ~ luôn đứng TRƯỚC số, không xen giữa dấu +/- và số.

## Hướng Dẫn Cho AI Report-Generator

1. **LUÔN tính % change từ công thức `(new - old) / old × 100`** — đừng copy dollar change rồi gắn dấu % vào. Đây là lỗi AP-005 kinh điển.
2. **LUÔN dùng basis points (bp) cho yield changes** — không bao giờ dùng % cho yield change. 1bp = 0.01pp. Format: `+3bp` hoặc `-5bp`.
3. **KHÔNG BAO GIỜ làm tròn intermediate values** — tính delta và % với full precision, chỉ round ở bước cuối cùng (1 decimal place).
4. **KHI viết commodities section** — kiểm tra cả 3 column: dollar change, %, và ghi chú. Đảm bảo % = dollar_delta / old_close × 100.
5. **KHI dùng ~ (approximate) marker** — đặt ~ TRƯỚC cả giá trị: `~$80-82`, `~+$3`, `~+3.8%`. Không dùng `~+~$3`.

## Rules Mới Đề Xuất

### RULE-016 — % change KHÔNG được bằng dollar change
- **Severity:** MAJOR
- **Detection:** Regex `\$\d+\.?\d*\s*\|\s*~?[\+\-]~?(\d+\.?\d*)\s*\|\s*~?[\+\-]~?\1%` — nếu % value = dollar value → FAIL
- **Anti-pattern:** `"WTI | $95.45 | +$1.59 | +1.59%"` — dollar và % giống hệt nhau (chỉ khác dấu %)
- **Fix template:** Sau khi viết report, chạy check: `abs(pct - abs(dollar_change) * close / 100) < 0.1` → flagged
- **Learned from:** 2026-05-07, quick_update_2000.md (WTI 1.59% = $1.59 dollar change)

## Checklist Cho Lần Report Tiếp Theo
- [ ] **Compute every % change independently** — `(new-old)/old*100`, not copy from dollar change
- [ ] **Verify Brent/WTI gold/oil % against close price** — use 3PM close as old value
- [ ] **Use bp (not %) for yield changes** — `+3bp` not `+0.03%`
- [ ] **Check ~ markers format** — `~+3.8%` not `~+~3.8%`
- [ ] **Consistent time notation** — `20:00` or `8:00 PM`, never `20:00 PM`
- [ ] **Smoke-test: pick 3 key % changes and recompute** before deploying
