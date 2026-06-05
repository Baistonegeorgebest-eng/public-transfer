#!/usr/bin/env python3
"""
从 extract/ 数据生成 style-reference-extended.md
包含：感官数据TOP作者 + 福利数据TOP + 进化曲线作者
"""

import json
from pathlib import Path
from collections import defaultdict

EXTRACT = Path(__file__).resolve().parent.parent / "extract"
MICLAW = Path.home() / ".openclaw" / "workspace" / "Miclaw-sessison"

with open(EXTRACT / "fingerprint-all.json", encoding="utf-8") as f:
    data = json.load(f)

books = [r for r in data if any(k.startswith("punct_") for k in r)]
deep = [r for r in data if r.get("is_deep")]

lines = []
lines.append("# 风格参照库扩展（v6.0·424本深度数据）")
lines.append("")
lines.append("> 来源：public-transfer/novel-corpus-analysis/extract/ 深度分析数据")
lines.append("> 本文件补充 style-reference.md 中未覆盖的感官/福利/进化数据")
lines.append("")

# ── 感官描写密度TOP ──
lines.append("## 一、感官描写密度TOP（424本深度分析）")
lines.append("")

sensory_books = [r for r in deep if "sensory" in r]
for sense_name, sense_key in [("视觉", "视觉"), ("听觉", "听觉"), ("触觉", "触觉"), ("嗅觉", "嗅觉"), ("味觉", "味觉")]:
    top = sorted(sensory_books, key=lambda r: r.get("sensory", {}).get(sense_key, {}).get("per_10k", 0), reverse=True)[:10]
    lines.append(f"### {sense_name}密度TOP10")
    lines.append("")
    lines.append("| 作品 | 作者 | 密度/万字 | 命中数 |")
    lines.append("|------|------|----------|--------|")
    for r in top:
        s = r.get("sensory", {}).get(sense_key, {})
        lines.append(f"| {r.get('title','?')} | {r.get('author','—')} | {s.get('per_10k',0):.1f} | {s.get('count',0)} |")
    lines.append("")

# ── 福利密度TOP ──
lines.append("## 二、福利内容密度TOP（424本深度分析）")
lines.append("")

welfare_books = [r for r in deep if "welfare" in r]
top_welfare = sorted(welfare_books, key=lambda r: r.get("welfare", {}).get("total", {}).get("per_10k", 0), reverse=True)[:20]
lines.append("| 作品 | 作者 | 总密度/万字 | L1身体 | L2服饰 | L3亲密 | L4暧昧 | L5氛围 |")
lines.append("|------|------|-----------|--------|--------|--------|--------|--------|")
for r in top_welfare:
    w = r.get("welfare", {})
    total = w.get("total", {}).get("per_10k", 0)
    l1 = w.get("L1", {}).get("per_10k", 0)
    l2 = w.get("L2", {}).get("per_10k", 0)
    l3 = w.get("L3", {}).get("per_10k", 0)
    l4 = w.get("L4", {}).get("per_10k", 0)
    l5 = w.get("L5", {}).get("per_10k", 0)
    lines.append(f"| {r.get('title','?')} | {r.get('author','—')} | {total:.1f} | {l1:.1f} | {l2:.1f} | {l3:.1f} | {l4:.1f} | {l5:.1f} |")
lines.append("")

# ── 作者进化曲线（按作者聚合）──
lines.append("## 三、作者进化曲线速查（多本作者）")
lines.append("")

author_books = defaultdict(list)
for r in books:
    author = r.get("author", "")
    if author and author != "—":
        author_books[author].append(r)

# 只保留有多本作品的作者
multi_authors = {a: bs for a, bs in author_books.items() if len(bs) >= 3}
for author in sorted(multi_authors.keys()):
    bs = sorted(multi_authors[author], key=lambda r: r.get("punct_感叹", 0))
    lines.append(f"### {author}（{len(bs)}本）")
    lines.append("")
    lines.append("| 作品 | 感叹 | 省略 | 逗号 | 句号 | 均句长 |")
    lines.append("|------|------|------|------|------|--------|")
    for r in bs:
        lines.append("| {} | {:.2f} | {:.2f} | {:.1f} | {:.1f} | {:.0f}字 |".format(
            r.get("title", "?"),
            r.get("punct_感叹", 0),
            r.get("punct_省略", 0),
            r.get("punct_逗号", 0),
            r.get("punct_句号", 0),
            r.get("punct_均句", 0)))
    lines.append("")

# ── 输出 ──
text = "\n".join(lines)
out = MICLAW / "novel-skills" / "expert-human-flavor" / "references" / "style-reference-extended.md"
out.write_text(text, encoding="utf-8")
print(f"💾 风格参照扩展: {out} ({out.stat().st_size/1024:.0f}KB)")

# 也保存到 extract/
out2 = EXTRACT / "style-reference-extended.md"
out2.write_text(text, encoding="utf-8")
print("✅ 完成")
