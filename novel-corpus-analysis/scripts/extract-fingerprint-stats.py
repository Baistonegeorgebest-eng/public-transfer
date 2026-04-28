#!/usr/bin/env python3
"""从指纹表 v4.4 提取全库标点统计"""

import os, re, json

FPT_PATH = os.path.expanduser("~/.openclaw/workspace/novel-corpus-analysis-tmp/fingerprint-table-v4.4.md")

with open(FPT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 解析表格行: | # | 作者 | 小说 | 字数 | 逗号 | 句号 | 感叹 | 省略 | 问号 | 均句 | 长句% | ...
rows = []
for line in content.split('\n'):
    line = line.strip()
    if not line.startswith('|'):
        continue
    cells = [c.strip() for c in line.split('|')]
    if len(cells) < 11:
        continue
    # 跳过表头
    if cells[1] == '#' or cells[1] == '---' or '作者' in cells[1]:
        continue
    try:
        idx = cells[1]
        author = cells[2]
        title = cells[3]
        wordcount = cells[4]
        comma = float(cells[5]) if cells[5] and cells[5] != '—' else None
        period = float(cells[6]) if cells[6] and cells[6] != '—' else None
        exclaim = float(cells[7]) if cells[7] and cells[7] != '—' else None
        ellipsis = float(cells[8]) if cells[8] and cells[8] != '—' else None
        question = float(cells[9]) if cells[9] and cells[9] != '—' else None
        avg_sent = float(cells[10]) if cells[10] and cells[10] != '—' else None
        long_pct = float(cells[11]) if len(cells) > 11 and cells[11] and cells[11] != '—' else None
        
        rows.append({
            'idx': idx, 'author': author, 'title': title, 'wordcount': wordcount,
            'comma': comma, 'period': period, 'exclaim': exclaim,
            'ellipsis': ellipsis, 'question': question,
            'avg_sent': avg_sent, 'long_pct': long_pct,
        })
    except (ValueError, IndexError):
        continue

print(f"解析到 {len(rows)} 本书\n")

def stats(values, label):
    vals = [v for v in values if v is not None and v > 0]
    if not vals:
        print(f"{label}: 无数据")
        return
    vals.sort()
    n = len(vals)
    mean = sum(vals) / n
    median = vals[n//2] if n%2 else (vals[n//2-1]+vals[n//2])/2
    print(f"{label} (N={n}):")
    print(f"  均值={mean:.2f} | 中位={median:.2f} | min={vals[0]:.2f} | max={vals[-1]:.2f} | P25={vals[n//4]:.2f} | P75={vals[3*n//4]:.2f}")
    return {'n': n, 'mean': round(mean,2), 'median': round(median,2)}

print("=" * 60)
print("全库标点指纹统计（来源：指纹表 v4.4）")
print("=" * 60)

results = {}
for field, label in [
    ('comma', '逗号密度/千字'),
    ('period', '句号密度/千字'),
    ('exclaim', '感叹号密度/千字'),
    ('ellipsis', '省略号密度/千字'),
    ('question', '问号密度/千字'),
    ('avg_sent', '均句长(字)'),
    ('long_pct', '长句>30字占比(%)'),
]:
    vals = [r[field] for r in rows]
    s = stats(vals, label)
    if s:
        results[field] = s

# 感叹号分布
print("\n" + "=" * 60)
print("感叹号密度分布")
print("=" * 60)
exclaim_vals = [r['exclaim'] for r in rows if r['exclaim'] is not None]
brackets = [(0, 1), (1, 2), (2, 3), (3, 5), (5, 8), (8, 12), (12, 20)]
for lo, hi in brackets:
    count = sum(1 for v in exclaim_vals if lo <= v < hi)
    pct = count / len(exclaim_vals) * 100
    bar = "█" * int(pct / 2)
    print(f"  [{lo:>2}-{hi:>2}]: {count:3d} ({pct:5.1f}%) {bar}")

# 多产作者
print("\n" + "=" * 60)
print("多产作者感叹号统计（3本+）")
print("=" * 60)
from collections import defaultdict
author_exclaim = defaultdict(list)
for r in rows:
    if r['exclaim'] is not None and r['author']:
        author_exclaim[r['author']].append((r['title'], r['exclaim']))

for author, books in sorted(author_exclaim.items(), key=lambda x: -len(x[1])):
    if len(books) < 3:
        continue
    vals = [b[1] for b in books]
    avg = sum(vals)/len(vals)
    print(f"\n{author} ({len(books)}本): 均值={avg:.2f}")
    for title, val in sorted(books, key=lambda x: x[1]):
        print(f"  - {title}: {val}/千字")

# 与协议旧数据对比
print("\n" + "=" * 60)
print("与协议 v4.4 旧数据对比")
print("=" * 60)
old_data = {
    'comma': {'n': 417, 'mean': 60.9, 'median': 59.7},
    'period': {'n': 417, 'mean': 22.2, 'median': 21.4},
    'exclaim': {'n': 417, 'mean': 5.1, 'median': 4.3},
    'ellipsis': {'n': 417, 'mean': 2.3, 'median': 1.4},
    'avg_sent': {'n': 417, 'mean': 40, 'median': 37},
}
for field in ['comma', 'period', 'exclaim', 'ellipsis', 'avg_sent']:
    if field in results:
        old = old_data.get(field, {})
        new = results[field]
        diff_mean = new['mean'] - old.get('mean', 0)
        sign = '+' if diff_mean > 0 else ''
        print(f"{field}: 旧(N={old.get('n','?')})均值={old.get('mean','?')} → 新(N={new['n']})均值={new['mean']} ({sign}{diff_mean:.2f})")
