#!/usr/bin/env python3
"""Apply merge guard to fetch-steve-le-daily SKILL.md"""
from pathlib import Path

skill_path = Path(r'C:\Users\Hung Phan\.openclaw\workspace-main\data\PhanTichChungKhoan\.scheduled\fetch-steve-le-daily\SKILL.md')

text = skill_path.read_text(encoding="utf-8")

if "_merge_guard" in text:
    print("SKIP: Already has guard")
else:
    # Insertion 1: After Step 6 heading
    anchor1 = "### Step 6 — Smart Merge into Knowledge Base (Bước 7 of knowledge-distillation-agent SKILL.md)"
    block1 = '''

> **⚠️ BẮT BUỘC dùng `knowledge_base/_merge_guard.py`** để tránh mojibake + JSON-escape leftover:
> - **Pre-merge**: text mới (distill content) phải đi qua `python knowledge_base/_merge_guard.py --sanitize-stdin` TRƯỚC khi edit vào KB
> - **Post-merge**: cuối cùng chạy `--lint knowledge_base/knowledge_base_steve_le.md`, fail → revert + fix
'''
    
    if anchor1 in text:
        text = text.replace(anchor1, anchor1 + block1)
        print(f"✓ Inserted guard warning after Step 6")
    else:
        print(f"WARN: Anchor 1 not found")
    
    # Insertion 2: After Step 7 heading, before the bullet list
    anchor2 = "### Step 7 — Verify and report"
    block2 = '''

> **⚠️ BẮT BUỘC chạy guard lint trước khi báo cáo:**
> ```bash
> python knowledge_base/_merge_guard.py --lint knowledge_base/knowledge_base_steve_le.md
> ```
> - Exit 0 + `✓ LINT PASS` → proceed to report
> - Exit 1 + `✗ LINT FAIL` → revert KB, fix source distill bằng `--sanitize-file`, retry

'''
    
    if anchor2 in text:
        text = text.replace(anchor2, anchor2 + block2)
        print(f"✓ Inserted guard lint step after Step 7 heading")
    else:
        print(f"WARN: Anchor 2 not found")
    
    skill_path.write_text(text, encoding="utf-8")
    print(f"✓ Saved. Verifying...")
    
    # Verify
    verify_text = skill_path.read_text(encoding="utf-8")
    count = verify_text.count("_merge_guard")
    print(f"✓ Total _merge_guard references: {count}")

print("Done!")
