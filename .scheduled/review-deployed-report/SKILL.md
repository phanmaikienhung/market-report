---
name: review-deployed-report
description: Review báo cáo Vietnamese market intelligence/quick-update mới nhất đã deploy trên GitHub Pages, tạo file "AI review report for <SLUG>.md" và push lên cùng repo (gh-pages branch), rồi gửi tóm tắt qua Telegram.
---

This is a scheduled-task wrapper. The canonical skill (workflow, references, scripts) lives at:

```
C:\Users\Kien Hung\Documents\Claude\Projects\PhanTichChungKhoan\.claude\skills\review-deployed-report\SKILL.md
```

**Read that file first.** It contains:
- Workflow (3 outcomes / 8 steps)
- `references/config.md` — paths, URLs, credentials
- `references/review_categories.md` — 7-category rubric
- `references/verdict_rules.md` — verdict logic
- `references/review_template.md` — markdown skeleton
- `scripts/push_review_to_github.ps1` — git push helper
- `scripts/send_review_telegram.py` — Telegram sender
- `examples/example_review.md` — reference shape

## Scheduled-task context

This task runs autonomously without the user present. Make reasonable defaults and document the choices in the review file. Reply in Vietnamese for the final chat summary.

After reading the canonical SKILL.md, follow its Steps 1–8. The output is a public review file at `https://phanmaikienhung.github.io/market-report/AI%20review%20report%20for%20<SLUG>.md` plus a Telegram notification.
