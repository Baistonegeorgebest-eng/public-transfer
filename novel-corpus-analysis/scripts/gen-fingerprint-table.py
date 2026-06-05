#!/usr/bin/env python3
"""
从 extract/fingerprint-all.json 生成：
1. 更新后的 fingerprint-table.md §12.5 段落（全量标点指纹表）
2. 品类指纹库 genre-fingerprints.md
3. 扩充的 style-reference-extended.md（现象级+高数据作者分析）
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

EXTRACT = Path(__file__).resolve().parent.parent / "extract"
MICLAW = Path.home() / ".openclaw" / "workspace" / "Miclaw-sessison"

# ── 加载数据 ──
with open(EXTRACT / "fingerprint-all.json", encoding="utf-8") as f:
    all_data = json.load(f)

# 过滤有标点数据的
books = [r for r in all_data if any(k.startswith("punct_") for k in r)]
print(f"📊 有标点数据的书籍: {len(books)}")

# ── 品类映射 ──
GENRE_MAP = {
    "仙侠": ["仙侠", "修真", "修仙", "武侠"],
    "玄幻": ["玄幻", "异界", "异世"],
    "西幻": ["西幻", "奇幻", "魔法"],
    "都市": ["都市", "现实", "现代"],
    "科幻": ["科幻", "末世", "星际", "未来"],
    "历史": ["历史", "架空", "古代", "穿越历史"],
    "恐怖": ["恐怖", "灵异", "悬疑", "惊悚"],
    "竞技": ["竞技", "网游", "电竞", "游戏"],
    "无限": ["无限", "综穿", "综漫"],
    "体育": ["体育", "足球", "篮球"],
    "言情": ["言情", "古言", "现言"],
}

def classify_genre(genre_str, title=""):
    if genre_str:
        for cat, keywords in GENRE_MAP.items():
            for kw in keywords:
                if kw in genre_str:
                    return cat
    # 从标题猜测
    for cat, keywords in GENRE_MAP.items():
        for kw in keywords:
            if kw in title:
                return cat
    return "未分类"


def style_tag(r):
    """根据数据生成风格标签"""
    tags = []
    ex = r.get("punct_感叹", 0)
    ell = r.get("punct_省略", 0)
    com = r.get("punct_逗号", 0)
    sent = r.get("punct_均句", 30)
    dlg = r.get("punct_对话占比", 0)

    if ex >= 10:
        tags.append("极致外放")
    elif ex >= 6:
        tags.append("高感叹")
    elif ex >= 3:
        tags.append("中感叹")
    elif ex < 1:
        tags.append("零感叹")
    else:
        tags.append("低感叹")

    if ell >= 5:
        tags.append("高省略")
    elif ell >= 3:
        tags.append("中省略")
    elif ell < 0.5:
        tags.append("极低省略")

    if com >= 75:
        tags.append("超高逗号")
    elif com >= 65:
        tags.append("高逗号")

    if sent >= 50:
        tags.append("超长句")
    elif sent >= 40:
        tags.append("长句型")
    elif sent < 20:
        tags.append("短句型")

    if dlg >= 40:
        tags.append("高对话")
    elif dlg < 10:
        tags.append("低对话")

    return " + ".join(tags) if tags else "—"


# ═══════════════════════════════════════════════════
# 1. 生成 §12.5 标点指纹表
# ═══════════════════════════════════════════════════
print("\n📝 生成 §12.5 标点指纹表...")

# 按感叹号密度降序排列
sorted_books = sorted(books, key=lambda r: r.get("punct_感叹", 0), reverse=True)

lines = []
lines.append("### 12.5 标点指纹（v6.0更新 — {}本全量实测）".format(len(books)))
lines.append("**规则：不同严肃度对应不同标点组合，不是所有场景用同一套标点。**")
lines.append("**全量数据（{}本小说实测，逗号/句号/感叹/省略 均为每千字频率）：**".format(len(books)))
lines.append("")

# 严肃度分档
tier1 = [r for r in books if r.get("punct_感叹", 0) >= 8]
tier2 = [r for r in books if 4 <= r.get("punct_感叹", 0) < 8]
tier3 = [r for r in books if 2 <= r.get("punct_感叹", 0) < 4]
tier4 = [r for r in books if r.get("punct_感叹", 0) < 2]
lines.append("- **全库严肃度分档（{}本实测）：**".format(len(books)))
lines.append("  - T1 极致外放（感叹≥8）：{}本".format(len(tier1)))
lines.append("  - T2 高感叹（感叹4-8）：{}本".format(len(tier2)))
lines.append("  - T3 中等（感叹2-4）：{}本".format(len(tier3)))
lines.append("  - T4 克制（感叹<2）：{}本".format(len(tier4)))
lines.append("")

# 主表
lines.append("| # | 作品 | 作者 | 逗号 | 句号 | 感叹 | 省略 | 均句长 | 风格标签 |")
lines.append("|---|------|------|------|------|------|------|--------|----------|")
for i, r in enumerate(sorted_books, 1):
    title = r.get("title", "?")
    author = r.get("author", "—")
    com = r.get("punct_逗号", 0)
    per = r.get("punct_句号", 0)
    ex = r.get("punct_感叹", 0)
    ell = r.get("punct_省略", 0)
    sent = r.get("punct_均句", 0)
    tag = style_tag(r)
    lines.append("| {} | {} | {} | {:.1f} | {:.1f} | {:.2f} | {:.2f} | {:.0f}字 | {} |".format(
        i, title, author, com, per, ex, ell, sent, tag))

fingerprint_section = "\n".join(lines)
print(f"  生成 {len(sorted_books)} 行数据")

# ═══════════════════════════════════════════════════
# 2. 生成品类指纹库
# ═══════════════════════════════════════════════════
print("\n📝 生成品类指纹库...")

genre_data = defaultdict(list)
for r in books:
    genre = r.get("genre", "")
    title = r.get("title", "")
    cat = classify_genre(genre, title)
    genre_data[cat].append(r)

genre_lines = []
genre_lines.append("# 品类指纹库（v6.0·{}本实测）".format(len(books)))
genre_lines.append("")
genre_lines.append("> 来源：public-transfer/novel-corpus-analysis/extract/ 全量数据")
genre_lines.append("> 本文件按品类聚合标点指纹数据，每品类标注中位值±标准差")
genre_lines.append("")
genre_lines.append("## 品类标点指纹矩阵")
genre_lines.append("")
genre_lines.append("| 品类 | 样本 | 逗号 | 句号 | 感叹 | 省略 | 问号 | 均句长 | 对话率 |")
genre_lines.append("|------|------|------|------|------|------|------|--------|--------|")

import statistics

def median_or_zero(vals):
    vals = [v for v in vals if v > 0]
    return statistics.median(vals) if vals else 0

def stdev_or_zero(vals):
    vals = [v for v in vals if v > 0]
    return statistics.stdev(vals) if len(vals) >= 2 else 0

for cat in ["仙侠", "玄幻", "西幻", "都市", "科幻", "历史", "恐怖", "竞技", "无限", "体育", "言情", "未分类"]:
    if cat not in genre_data:
        continue
    rs = genre_data[cat]
    n = len(rs)
    com_vals = [r.get("punct_逗号", 0) for r in rs if r.get("punct_逗号", 0) > 0]
    per_vals = [r.get("punct_句号", 0) for r in rs if r.get("punct_句号", 0) > 0]
    ex_vals = [r.get("punct_感叹", 0) for r in rs if r.get("punct_感叹", 0) > 0]
    ell_vals = [r.get("punct_省略", 0) for r in rs if r.get("punct_省略", 0) > 0]
    que_vals = [r.get("punct_问号", 0) for r in rs if r.get("punct_问号", 0) > 0]
    sent_vals = [r.get("punct_均句", 0) for r in rs if r.get("punct_均句", 0) > 0]
    dlg_vals = [r.get("punct_对话占比", 0) for r in rs if r.get("punct_对话占比", 0) > 0]

    com_m = median_or_zero(com_vals)
    per_m = median_or_zero(per_vals)
    ex_m = median_or_zero(ex_vals)
    ell_m = median_or_zero(ell_vals)
    que_m = median_or_zero(que_vals)
    sent_m = median_or_zero(sent_vals)
    dlg_m = median_or_zero(dlg_vals)

    dlg_str = f"{dlg_m:.0f}%" if dlg_m > 0 else "—"
    genre_lines.append("| **{}** | {}本 | {:.1f} | {:.1f} | {:.1f} | {:.1f} | {:.1f} | {:.0f} | {} |".format(
        cat, n, com_m, per_m, ex_m, ell_m, que_m, sent_m, dlg_str))

genre_lines.append("")

# 品类内详细数据
for cat in ["仙侠", "玄幻", "西幻", "都市", "科幻", "历史", "恐怖", "竞技", "无限", "体育", "言情", "未分类"]:
    if cat not in genre_data:
        continue
    rs = sorted(genre_data[cat], key=lambda r: r.get("punct_感叹", 0), reverse=True)
    genre_lines.append(f"### {cat}（{len(rs)}本）")
    genre_lines.append("")
    genre_lines.append("| 作品 | 作者 | 逗号 | 句号 | 感叹 | 省略 | 均句长 |")
    genre_lines.append("|------|------|------|------|------|------|--------|")
    for r in rs:
        title = r.get("title", "?")
        author = r.get("author", "—")
        com = r.get("punct_逗号", 0)
        per = r.get("punct_句号", 0)
        ex = r.get("punct_感叹", 0)
        ell = r.get("punct_省略", 0)
        sent = r.get("punct_均句", 0)
        genre_lines.append("| {} | {} | {:.1f} | {:.1f} | {:.2f} | {:.2f} | {:.0f}字 |".format(
            title, author, com, per, ex, ell, sent))
    genre_lines.append("")

genre_text = "\n".join(genre_lines)
print(f"  生成 {len(genre_data)} 个品类")

# ═══════════════════════════════════════════════════
# 3. 输出文件
# ═══════════════════════════════════════════════════

# §12.5 段落
out1 = EXTRACT / "fingerprint-section-12.5.md"
out1.write_text(fingerprint_section, encoding="utf-8")
print(f"\n💾 §12.5: {out1} ({out1.stat().st_size/1024:.0f}KB)")

# 品类指纹库
genre_dir = MICLAW / "novel-skills" / "expert-genre-contract" / "references"
genre_dir.mkdir(parents=True, exist_ok=True)
out2 = genre_dir / "genre-fingerprints.md"
out2.write_text(genre_text, encoding="utf-8")
print(f"💾 品类指纹库: {out2} ({out2.stat().st_size/1024:.0f}KB)")

# 同时保存到 extract/
out2b = EXTRACT / "genre-fingerprints.md"
out2b.write_text(genre_text, encoding="utf-8")

print("\n✅ 完成")
