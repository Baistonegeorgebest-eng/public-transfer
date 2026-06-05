#!/usr/bin/env python3
"""
生成知识库摘要文件：
- author-dna.md（多本作者进化曲线）
- anomaly-cases.md（数据异常案例）
- top30-analysis.md（现象级分析摘要）
"""

import json
from pathlib import Path
from collections import defaultdict

EXTRACT = Path(__file__).resolve().parent.parent / "extract"
KB_SUMMARIES = Path(__file__).resolve().parent.parent.parent / "novel-corpus-knowledge-base" / "summaries"
KB_EXAMPLES = Path(__file__).resolve().parent.parent.parent / "novel-corpus-knowledge-base" / "examples"

with open(EXTRACT / "fingerprint-all.json", encoding="utf-8") as f:
    data = json.load(f)

books = [r for r in data if any(k.startswith("punct_") for k in r)]

# ═══════════════════════════════════════════════════
# 1. author-dna.md
# ═══════════════════════════════════════════════════
print("📝 生成 author-dna.md...")

author_books = defaultdict(list)
for r in books:
    author = r.get("author", "")
    if author and author != "—":
        author_books[author].append(r)

# 只保留2本以上的作者
multi = {a: bs for a, bs in author_books.items() if len(bs) >= 2}

lines = []
lines.append("# 作者风格DNA（Author DNA）")
lines.append("")
lines.append(f"> 基于 {len(multi)} 位多本作者的进化曲线数据")
lines.append(f"> 全量数据见 data/fingerprint-all.json")
lines.append("")

# 按作品数降序排列
for author in sorted(multi.keys(), key=lambda a: len(multi[a]), reverse=True):
    bs = sorted(multi[author], key=lambda r: r.get("title", ""))
    lines.append(f"## {author}（{len(bs)}本）")
    lines.append("")
    lines.append("| 作品 | 感叹 | 省略 | 逗号 | 句号 | 均句长 | 对话率 | 风格 |")
    lines.append("|------|------|------|------|------|--------|--------|------|")
    for r in bs:
        ex = r.get("punct_感叹", 0)
        ell = r.get("punct_省略", 0)
        com = r.get("punct_逗号", 0)
        per = r.get("punct_句号", 0)
        sent = r.get("punct_均句", 0)
        dlg = r.get("punct_对话占比", 0)
        # 风格标签
        if ex >= 10:
            tag = "极致外放"
        elif ex >= 6:
            tag = "高感叹"
        elif ex >= 3:
            tag = "中感叹"
        elif ex < 1:
            tag = "零感叹"
        else:
            tag = "低感叹"
        dlg_str = f"{dlg:.0f}%" if dlg > 0 else "—"
        lines.append("| {} | {:.2f} | {:.2f} | {:.1f} | {:.1f} | {:.0f}字 | {} | {} |".format(
            r.get("title", "?"), ex, ell, com, per, sent, dlg_str, tag))
    lines.append("")

    # 进化趋势
    if len(bs) >= 3:
        ex_vals = [r.get("punct_感叹", 0) for r in bs]
        if ex_vals[-1] < ex_vals[0] * 0.5:
            lines.append(f"**进化趋势**：感叹号从{ex_vals[0]:.1f}降至{ex_vals[-1]:.1f}，趋向内收")
        elif ex_vals[-1] > ex_vals[0] * 1.5:
            lines.append(f"**进化趋势**：感叹号从{ex_vals[0]:.1f}升至{ex_vals[-1]:.1f}，趋向外放")
        else:
            lines.append(f"**进化趋势**：感叹号稳定在{min(ex_vals):.1f}-{max(ex_vals):.1f}区间")
        lines.append("")

text = "\n".join(lines)
out = KB_SUMMARIES / "author-dna.md"
out.write_text(text, encoding="utf-8")
print(f"  💾 {out} ({out.stat().st_size/1024:.0f}KB)")

# ═══════════════════════════════════════════════════
# 2. anomaly-cases.md
# ═══════════════════════════════════════════════════
print("📝 生成 anomaly-cases.md...")

lines = []
lines.append("# 数据异常案例（Anomaly Cases）")
lines.append("")
lines.append("> 标点指纹极端值或违反品类规律的作品")
lines.append("> 这些案例对理解标点光谱的边界极有价值")
lines.append("")

# 极端感叹号
lines.append("## 一、感叹号极端值")
lines.append("")
ex_sorted = sorted(books, key=lambda r: r.get("punct_感叹", 0), reverse=True)
lines.append("### TOP10 最高感叹")
lines.append("")
lines.append("| 作品 | 作者 | 感叹/千字 | 品类 | 说明 |")
lines.append("|------|------|----------|------|------|")
for r in ex_sorted[:10]:
    lines.append("| {} | {} | {:.2f} | {} | — |".format(
        r.get("title", "?"), r.get("author", "—"),
        r.get("punct_感叹", 0), r.get("genre", "—")))
lines.append("")

lines.append("### TOP10 最低感叹（非译本）")
lines.append("")
native_low = [r for r in books if not r.get("is_translated")]
native_low.sort(key=lambda r: r.get("punct_感叹", 0))
lines.append("| 作品 | 作者 | 感叹/千字 | 品类 | 说明 |")
lines.append("|------|------|----------|------|------|")
for r in native_low[:10]:
    lines.append("| {} | {} | {:.2f} | {} | — |".format(
        r.get("title", "?"), r.get("author", "—"),
        r.get("punct_感叹", 0), r.get("genre", "—")))
lines.append("")

# 极端省略号
lines.append("## 二、省略号极端值")
lines.append("")
ell_sorted = sorted(books, key=lambda r: r.get("punct_省略", 0), reverse=True)
lines.append("### TOP10 最高省略")
lines.append("")
lines.append("| 作品 | 作者 | 省略/千字 | 感叹/千字 | 说明 |")
lines.append("|------|------|----------|----------|------|")
for r in ell_sorted[:10]:
    lines.append("| {} | {} | {:.2f} | {:.2f} | — |".format(
        r.get("title", "?"), r.get("author", "—"),
        r.get("punct_省略", 0), r.get("punct_感叹", 0)))
lines.append("")

# 极端均句长
lines.append("## 三、均句长极端值")
lines.append("")
sent_sorted = sorted(books, key=lambda r: r.get("punct_均句", 0), reverse=True)
lines.append("### TOP10 最长句子")
lines.append("")
lines.append("| 作品 | 作者 | 均句长 | 长句率 | 说明 |")
lines.append("|------|------|--------|--------|------|")
for r in sent_sorted[:10]:
    lines.append("| {} | {} | {:.0f}字 | {:.0f}% | — |".format(
        r.get("title", "?"), r.get("author", "—"),
        r.get("punct_均句", 0), r.get("punct_长句(>30字)%", 0)))
lines.append("")

# 感官异常
sensory_books = [r for r in data if "sensory" in r]
if sensory_books:
    lines.append("## 四、感官描写异常")
    lines.append("")
    # 触觉最高
    touch_top = sorted(sensory_books, key=lambda r: r.get("sensory", {}).get("触觉", {}).get("per_10k", 0), reverse=True)[:5]
    lines.append("### 触觉密度TOP5")
    lines.append("")
    lines.append("| 作品 | 作者 | 触觉/万字 | 说明 |")
    lines.append("|------|------|----------|------|")
    for r in touch_top:
        lines.append("| {} | {} | {:.1f} | — |".format(
            r.get("title", "?"), r.get("author", "—"),
            r.get("sensory", {}).get("触觉", {}).get("per_10k", 0)))
    lines.append("")

    # 嗅觉最高
    smell_top = sorted(sensory_books, key=lambda r: r.get("sensory", {}).get("嗅觉", {}).get("per_10k", 0), reverse=True)[:5]
    lines.append("### 嗅觉密度TOP5")
    lines.append("")
    lines.append("| 作品 | 作者 | 嗅觉/万字 | 说明 |")
    lines.append("|------|------|----------|------|")
    for r in smell_top:
        lines.append("| {} | {} | {:.1f} | — |".format(
            r.get("title", "?"), r.get("author", "—"),
            r.get("sensory", {}).get("嗅觉", {}).get("per_10k", 0)))
    lines.append("")

text = "\n".join(lines)
out = KB_SUMMARIES / "anomaly-cases.md"
out.write_text(text, encoding="utf-8")
print(f"  💾 {out} ({out.stat().st_size/1024:.0f}KB)")

# ═══════════════════════════════════════════════════
# 3. top30-analysis.md
# ═══════════════════════════════════════════════════
print("📝 生成 top30-analysis.md...")

# 找最大的30个分析文件
top30 = sorted(data, key=lambda r: r.get("file_size_kb", 0), reverse=True)[:30]

lines = []
lines.append("# 现象级分析摘要（Top 30）")
lines.append("")
lines.append(f"> 按分析文件大小排序，取前30份最大/最详细的分析")
lines.append("> 完整分析见原始 analysis/ 目录")
lines.append("")

lines.append("| # | 作品 | 作者 | 文件大小 | 深度 | 感叹 | 省略 | 均句长 |")
lines.append("|---|------|------|---------|------|------|------|--------|")
for i, r in enumerate(top30, 1):
    deep = "✅" if r.get("is_deep") else "—"
    ex = r.get("punct_感叹", 0)
    ell = r.get("punct_省略", 0)
    sent = r.get("punct_均句", 0)
    lines.append("| {} | {} | {} | {:.0f}KB | {} | {:.2f} | {:.2f} | {:.0f}字 |".format(
        i, r.get("title", "?"), r.get("author", "—"),
        r.get("file_size_kb", 0), deep, ex, ell, sent))
lines.append("")

text = "\n".join(lines)
out = KB_EXAMPLES / "top30-analysis.md"
out.write_text(text, encoding="utf-8")
print(f"  💾 {out} ({out.stat().st_size/1024:.0f}KB)")

print("\n✅ 完成")
