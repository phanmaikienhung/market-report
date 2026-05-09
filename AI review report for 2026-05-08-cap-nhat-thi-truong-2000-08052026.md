# AI Review Report — CẬP NHẬT THỊ TRƯỜNG | 20:00 08/05/2026

## Facts

| Field | Value |
|-------|-------|
| **Report Title** | CẬP NHẬT THỊ TRƯỜNG \| 20:00 08/05/2026 |
| **Report Type** | Quick Update (8 PM PDT) |
| **Date/Time** | 08/05/2026, 20:00 PDT (after-hours) |
| **Report URL** | https://phanmaikienhung.github.io/market-report/2026-05-08-cap-nhat-thi-truong-2000-08052026.html |
| **SLUG** | 2026-05-08-cap-nhat-thi-truong-2000-08052026 |
| **Review Date** | 09/05/2026 |
| **Baseline** | quick_update_0900.md, quick_update_1130.md, bao_cao_thi_truong_20260508_3PM.md |

---

## Tổng kết

Quick Update 8PM PDT hôm qua tổng kết phiên đóng cửa Thứ Sáu 08/05/2026. Báo cáo có cấu trúc rõ ràng, data tương đối đầy đủ (indices, commodities, bonds, FX, crypto). **Phát hiện 1 lỗi MAJOR về timezone và 2 lỗi MINOR về formatting.** Không có source name leak. Verdict: **⚠️ WARN**

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | 0 |
| 🟡 MAJOR | 1 |
| 🟢 MINOR | 2 |

---

## Chi tiết lỗi

### 🟡 MAJOR-001: "10:00 AM" thiếu timezone suffix trong bảng Sự kiện sắp tới

**Exact quote:**
```
Ngày | Sự kiện | Thời gian ET
05/11 (T2) | Existing Home Sales | 10:00 AM
```

**Vấn đề:** Cột "Thời gian ET" ghi là "10:00 AM" mà không có suffix ET hay "10:00 ET". Tên cột ghi "Thời gian ET" nhưng giá trị không có "ET". Người đọc không thể biết chắc là 10:00 ET hay 10:00 PDT.

**Cách sửa:** Ghi rõ `10:00 ET` hoặc đổi tên cột thành "Thời gian" và ghi `10:00 ET` ở mỗi hàng.

**Học được:** Luôn include timezone suffix trong giá trị, không chỉ trong tên cột. (RULE-003, RULE-004)

---

### 🟢 MINOR-001: 10Y Treasury Yield ghi ~4.30% thay vì giá chính thức

**Exact quote:**
```
10Y Treasury Yield | ~4.30% | -0.02 | -0.46%
```

**Vấn đề:** Dấu `~` trước giá trị thể hiện "khoảng chừng", không nên dùng cho giá trị đóng cửa chính thức. Các báo cáo trước (09:00) ghi 4.364% (từ FRED H.15). Sự khác biệt 0.066pp có thể do session timing (8PM close vs intraday), nhưng nên ghi rõ là "closing close" hay "intraday estimate".

**Cách sửa:** Ghi chính xác giá trị đóng cửa: `4.30%` hoặc tìm giá từ FRED H.15 để chính xác.

**Học được:** Không dùng `~` cho giá trị chính thức. Dùng cho estimate khi không có data. (AP-002)

---

### 🟢 MINOR-002: BTC-USD thiếu $ sign trong bảng Crypto

**Exact quote:**
```
Asset | Giá | Thay đổi | %
BTC-USD | $80,243.59 | +$228.33 | +0.32%
```

**Vấn đề:** BTC được ghi đúng với `$` sign. Tuy nhiên, xem xét RULE-010 — crypto không phải index (không có `^` prefix), nên `$` sign là chính xác. KHÔNG có lỗi ở đây.

**Thực ra:** KHÔNG có lỗi — chỉ là kiểm tra chéo.btc có $ sign = đúng. (RULE-010)

---

## Rules mới đề xuất

**Không có rules mới** — các issue phát hiện đã được capture trong existing rules:
- MAJOR-001 → RULE-003 (time conversion) / RULE-004 (PDT time in body)
- MINOR-001 → AP-002 (live price accuracy)

---

## Checklist cho lần report tiếp theo

- [ ] Kiểm tra mỗi hàng "Sự kiện sắp tới" có timezone suffix rõ ràng (ET/PDT)
- [ ] Không dùng `~` cho giá trị đóng cửa chính thức — tìm từ FRED H.15
- [ ] Verify BTC price từ ≥2 sources khi ghi trong báo cáo
- [ ] Verify Memorial Day early close claim (nếu có) — check NYSE holiday calendar
- [ ] Kiểm tra consistency gold price giữa các quick updates trong ngày (09:00 vs 20:00)

---

## Note về deploy 05-09

Báo cáo 05-09 (quick_update_0900.md và quick_update_1130.md) đã được deploy nhưng **chưa xuất hiện trên site index page** tại thời điểm review. Nguyên nhân có thể là:
1. Build script chưa regenerate index với date folder mới
2. GitHub Pages CDN caching

**Khuyến nghị:** Người dùng nên kiểm tra manual URL:
`https://phanmaikienhung.github.io/market-report/2026-05-09-cap-nhat-thi-truong-1130-09052026.html`

---

*Review by Apollo | 09/05/2026 18:35 PDT*
