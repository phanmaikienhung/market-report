# Review Report: QUICK 11:30 AM PDT RE-V2 (2026-05-05)
- **Report URL (reviewed):** https://phanmaikienhung.github.io/market-report/2026-05-05-cap-nhat-thi-truong-1130-05052026.html
- **Report Date:** 2026-05-05
- **Review Date:** 2026-05-05
- **Reviewer:** AI Post-Deploy Reviewer (task: review-deployed-report, RE-V2 iteration)
- **Verdict:** WARN

## Tổng Kết
Report RE-V2 (deployed lần thứ 2) có chất lượng tốt hơn rất nhiều so với bản đầu tiên. Đã sửa được hầu hết các lỗi CRITICAL và MAJOR từ bản trước: không còn Chinese chars, không có source name leak, không dùng `~` prefix cho giá, table columns đầy đủ, format commodity nhất quán, có Gold data, economic data được ghi rõ tháng công bố. Tuy nhiên vẫn còn 2 lỗi MAJOR: (1) VIX change column ghi -0.91 nhưng % change -4.98% là không khớp (inconsistent baseline), (2) Yield change column dùng % thay vì bp/pp. Không có lỗi CRITICAL nào.

- 🔴 Critical: 0
- 🟡 Major: 2
- 🟢 Minor: 2

## Chi Tiết Lỗi

### 🟡 MAJOR — VIX Change column: absolute change không khớp với % change
- **Category:** 4.2 Data Accuracy
- **Rule:** RULE-002 (Live price must match session timing)
- **Vị trí:** Bảng Commodities & Yields, row VIX
- **Quote:** `VIX | 17.38 | -0.91 | -4.98%`
- **Vấn đề:** Absolute change (-0.91) và % change (-4.98%) dùng baseline khác nhau. 
  - Nếu prev close = 16.99 (Friday) → change = +0.39 (+2.3%) — KHÔNG KHỚP -0.91/-4.98%
  - Nếu từ 17.95 (mở cửa) → change = -0.57 (-3.2%) — KHÔNG KHỚP
  - Nếu -4.98% đúng → prev = 18.29, change = -0.91. Nhưng giá nào tại 17:95-18:29?
  - Trong narrative ghi "Giảm mạnh từ 16.99 → 17.38" → đây là tăng +2.3%, nhưng % change table là -4.98%. Mâu thuẫn.
- **Cách sửa:** Dùng cùng baseline cho cả absolute và % change. Nếu so với Friday close (16.99): ghi `+0.39 | +2.3%`. Nếu so với intraday high (~17.95): ghi `-0.57 | -3.2%`. Không mix baselines.
- **Học được:** RULE đề xuất: Cùng một row trong bảng phải dùng cùng prev close baseline cho cả Change và % Change.

### 🟡 MAJOR — Yield change column dùng % thay vì bp/pp (RULE-011)
- **Category:** 4.3 Arithmetic & Units
- **Rule:** RULE-011
- **Vị trí:** Bảng Commodities & Yields, rows 10Y và 30Y Treasury
- **Quote:** `10Y Treasury Yield (^TNX) | 4.4160% | -0.0300 | -0.67%` và `30Y Treasury Yield (^TYX) | 4.9840% | -0.0410 | -0.82%`
- **Vấn đề:** % column ghi -0.67% và -0.82% — đây là % change của yield value, nhưng quy tắc RULE-011 yêu cầu dùng bp/pp để tránh nhầm lẫn magnitude. Đúng phải là:
  - 10Y: `-0.0300pp` (hay `-3.0bp`) thay vì `-0.67%`
  - 30Y: `-0.0410pp` (hay `-4.1bp`) thay vì `-0.82%`
- **Cách sửa:** Auto-convert yield change từ pp sang bp: `change_bp = |yield - prev_yield| * 10000`
- **Học được:** Đã được đề xuất trong RE-V1 review (RULE-011). Cần enforce trong template generator.

### 🟢 MINOR — DXY missing absolute change value
- **Category:** 4.2 Data Accuracy
- **Vị trí:** Bảng Commodities & Yields, row DXY
- **Quote:** `DXY (Dollar Index) | 98.48 | +0.11 | +0.11%`
- **Vấn đề:** Không còn trống `—` như bản trước (đã được sửa!). Tuy nhiên giá +0.11 có vẻ là % change lẫn với absolute change. Từ browser data, DXY prev close ~98.37 → change ≈ +0.11 points, và +0.11% cũng khớp. Không có lỗi dữ liệu nhưng dễ gây nhầm lẫn vì value giống nhau.
- **Cách sửa:** Làm rõ: ghi absolute change là `+0.11` và % change là `+0.11%` — hai giá trị khác nhau nhưng trùng chữ số. Có thể thêm đơn vị: `+0.11 pts | +0.11%`
- **Học được:** Khi absolute và % change có cùng giá trị số → thêm label để phân biệt.

### 🟢 MINOR — "15:00 PM PDT" format inconsistency
- **Category:** 4.4 Format & Language
- **Vị trí:** Footer — "Cập nhật tiếp theo: 15:00 PM PDT"
- **Quote:** `Cập nhật tiếp theo: 15:00 PM PDT (market-report-full)`
- **Vấn đề:** "15:00 PM" — 15:00 là 24-hour format, "PM" là 12-hour suffix. Lặp lại redundant. Đúng: "3:00 PM PDT" hoặc "15:00 PDT"
- **Cách sửa:** Dùng consistent format: "3:00 PM PDT"
- **Học được:** Không mix 24h và 12h notation.

## Positive Notes (bản RE-V2 đã sửa được từ RE-V1)

✅ **Không còn Chinese characters** — RULE-012 satisfied
✅ **Không còn source name leak** — RULE-005 satisfied
✅ **Không dùng `~` prefix cho giá** — format nhất quán
✅ **DXY change column không còn trống `—`**
✅ **Có Gold price** trong bảng Commodities
✅ **Economic data ghi rõ tháng + release date**
✅ **Yield change column không còn trống**
✅ **Russell 2000 không còn 52w High < Current Price**
✅ **No CJK characters anywhere in report**
✅ **Tiếng Việt toàn bộ content**

## Hướng Dẫn Cho AI Report-Generator

1. **VIX: Dùng cùng baseline cho cả Change và % Change** — cùng row trong bảng phải so với cùng prev close. Không mix intraday vs daily baseline.
2. **Yield change phải dùng bp/pp** — RULE-011: `-3.0bp` hoặc `-0.030pp`, không dùng `-0.67%`.
3. **DXY: Làm rõ absolute vs % change** — khi cả hai có cùng value số, thêm label `pts` cho absolute.
4. **Time format phải nhất quán** — không mix 24h và 12h: "15:00 PDT" HOẶC "3:00 PM PDT", không phải "15:00 PM PDT".
5. **Tiếp tục duy trì:** Không Chinese chars, không source leaks, đầy đủ table columns, format commodity nhất quán.

## Rules Mới Đề Xuất

### RULE-014 — VIX Change baseline consistency
- **Severity:** MAJOR
- **Detection:** Trong cùng row, kiểm tra `change = current - prev_close` và `% = (current - prev_close) / prev_close * 100`. Nếu cả hai không cùng reference → FAIL.
- **Anti-pattern:** `VIX | 17.38 | -0.91 | -4.98%` (change từ intraday high, % từ Friday close)
- **Fix template:** Tính cả absolute và % change từ cùng prev_close (Friday close cho daily report).
- **Learned from:** 2026-05-05, RE-V2 of quick_update_1130

## Checklist Cho Lần Report Tiếp Theo
- [ ] VIX: tính Change và % từ cùng prev close
- [ ] Yield: dùng bp/pp cho change (RULE-011)
- [ ] Time format: consistent 24h HOẶC 12h
- [ ] DXY: thêm label pts nếu cần phân biệt
- [ ] Duy trì: no CJK, no source leaks, full tables
