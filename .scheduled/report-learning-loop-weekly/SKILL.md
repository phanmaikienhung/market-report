---
name: report-learning-loop-weekly
description: Weekly rollup Chủ nhật 7 PM: promote provisional cases, escalate confirmed → reviewer anti_patterns, generate weekly summary.
---

Chạy weekly rollup của report-learning-loop skill.

## MÔI TRƯỜNG
Cowork Linux sandbox, Python stdlib only. Không cần wrapper Windows MCP.

## Task

```bash
cd /sessions/peaceful-pensive-babbage/mnt/PhanTichChungKhoan
python3 report-learning-loop/scripts/weekly_rollup.py
```

Script sẽ tự động:
1. Scan 7 ngày gần nhất trong `learning/daily/` để build weekly metrics summary
2. Promote provisional cases có occurrence_count ≥ 2 → status=CONFIRMED, trust=1.0
3. Retire minor cases có `last_seen > 7 ngày` + occurrence=1 → status=ARCHIVED
4. Escalate newly CONFIRMED cases → append vào `report-reviewer/references/anti_patterns.md` với format AP-NNN
5. Write `learning/weekly/YYYY-Www_rollup.md` với summary metrics + promotions + retirements

## Sau khi script chạy xong

1. Đọc `learning/weekly/<week_label>_rollup.md` để xem kết quả
2. Nếu có promoted cases → đọc từng case file trong `learning/cases/case_NNN.md` và verify chất lượng
3. Nếu có escalated cases → verify `report-reviewer/references/anti_patterns.md` đã được append đúng format
4. Gửi tóm tắt vào chat: số cases promoted, số cases retired, số cases escalated, link đến weekly rollup md file

## Failure handling

- Nếu không có metrics trong 7 ngày → write note "no data to rollup", không fail
- Nếu script lỗi → log error + stop, báo anh qua chat

Ngôn ngữ: Tiếng Việt.