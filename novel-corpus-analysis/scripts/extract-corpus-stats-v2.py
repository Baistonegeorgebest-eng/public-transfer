#!/usr/bin/env python3
"""从 analysis-*.md 报告中批量提取标点指纹数据 - v2 修正版"""

import os, re, json, glob
from collections import defaultdict

REPORT_DIR = os.path.expanduser("~/.openclaw/workspace/novel-corpus-analysis-tmp")

def parse_report(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    basename = os.path.basename(filepath)
    
    # 跳过 deep 对比分析（多本书合在一起）
    if '-deep' in basename or '对比' in basename or '进化' in basename:
        return None
    
    # 提取书名
    title_match = re.search(r'# [《「](.+?)[》」]', content)
    title = title_match.group(1) if title_match else basename.replace('analysis-', '').replace('.md', '')
    
    # 提取作者 - 多种格式
    author = "未知"
    for pattern in [
        r'作者[：:]\s*([^\s|]+)',  # 作者：xxx |
        r'\*\*作者\*\*[：:]\s*([^\s|]+)',  # **作者**：xxx
    ]:
        m = re.search(pattern, content)
        if m:
            author = m.group(1).strip()
            # 清理多余标点
            author = author.rstrip('，。、')
            break
    
    # 提取字数
    wordcount_wan = None
    m = re.search(r'全书约?([\d.]+)\s*万字', content)
    if m:
        wordcount_wan = float(m.group(1))
    
    # 提取章数
    chapters = None
    m = re.search(r'(\d+)\s*章', content)
    if m:
        chapters = int(m.group(1))
    
    data = {}
    
    # 标点数据 - 从表格行提取更可靠
    # 匹配 "| 感叹号密度 | X.XX/千字 |" 格式
    for field, patterns in [
        ('exclaim', [r'\|\s*感叹号密度\s*\|\s*([\d.]+)', r'感叹号密度[：:]\s*([\d.]+)']),
        ('period', [r'\|\s*句号密度\s*\|\s*([\d.]+)', r'句号密度[：:]\s*([\d.]+)']),
        ('ellipsis', [r'\|\s*省略号密度\s*\|\s*([\d.]+)', r'省略号密度[：:]\s*([\d.]+)']),
        ('question', [r'\|\s*问号密度\s*\|\s*([\d.]+)', r'问号密度[：:]\s*([\d.]+)']),
        ('comma', [r'\|\s*逗号密度\s*\|\s*([\d.]+)', r'逗号密度[：:]\s*([\d.]+)']),
        ('avg_sentence_len', [r'\|\s*均句长\s*\|\s*(\d+)', r'均句长[：:]\s*(\d+)']),
        ('long_sentence_pct', [r'\|\s*长句\(?>30字\)\s*\|\s*([\d.]+)']),
        ('avg_para_len', [r'\|\s*段均长度\s*\|\s*(\d+)']),
    ]:
        for pat in patterns:
            m = re.search(pat, content)
            if m:
                val = float(m.group(1))
                # 过滤明显异常值
                if field == 'avg_sentence_len' and val > 200:
                    continue
                if field == 'avg_para_len' and val > 1000:
                    continue
                data[field] = val
                break
    
    # 对话比例
    m = re.search(r'对话比例[：:]\s*([\d.]+)%', content)
    if m:
        data['dialogue_pct'] = float(m.group(1))
    else:
        m = re.search(r'对话[^\d]*?(\d+\.?\d*)%', content)
        if m:
            val = float(m.group(1))
            if val < 100:  # 过滤异常
                data['dialogue_pct'] = val
    
    return {
        'title': title, 'author': author,
        'wordcount_wan': wordcount_wan, 'chapters': chapters,
        'file': basename, **data
    }

def compute_stats(values):
    if not values:
        return None
    values = sorted(values)
    n = len(values)
    mean = sum(values) / n
    median = values[n // 2] if n % 2 == 1 else (values[n//2 - 1] + values[n//2]) / 2
    return {
        'n': n, 'mean': round(mean, 2), 'median': round(median, 2),
        'min': round(values[0], 2), 'max': round(values[-1], 2),
        'p25': round(values[n // 4], 2), 'p75': round(values[3 * n // 4], 2),
    }

def main():
    files = sorted(glob.glob(os.path.join(REPORT_DIR, 'analysis-*.md')))
    print(f"找到 {len(files)} 份报告文件\n")
    
    records = []
    skipped = 0
    for f in files:
        r = parse_report(f)
        if r is None:
            skipped += 1
            continue
        records.append(r)
    
    print(f"有效报告: {len(records)} 份 (跳过 {skipped} 份 deep/对比/进化)")
    
    with_punct = [r for r in records if 'exclaim' in r]
    print(f"含感叹号数据: {len(with_punct)} 份")
    with_comma = [r for r in records if 'comma' in r]
    print(f"含逗号数据: {len(with_comma)} 份\n")
    
    # === 全库统计 ===
    print("=" * 60)
    print("全库标点指纹统计 (更新自 422 份报告)")
    print("=" * 60)
    
    for field, label in [
        ('exclaim', '感叹号密度/千字'),
        ('comma', '逗号密度/千字'),
        ('period', '句号密度/千字'),
        ('ellipsis', '省略号密度/千字'),
        ('question', '问号密度/千字'),
        ('avg_sentence_len', '均句长(字)'),
        ('long_sentence_pct', '长句>30字占比(%)'),
        ('avg_para_len', '段均长度(字)'),
    ]:
        vals = [r[field] for r in records if field in r]
        stats = compute_stats(vals)
        if stats:
            print(f"\n{label} (N={stats['n']}):")
            print(f"  均值={stats['mean']} | 中位={stats['median']} | "
                  f"min={stats['min']} | max={stats['max']} | P25={stats['p25']} | P75={stats['p75']}")
    
    # === 感叹号分布 ===
    print("\n" + "=" * 60)
    print("感叹号密度分布")
    print("=" * 60)
    exclaim_vals = [r['exclaim'] for r in with_punct]
    brackets = [(0, 1), (1, 2), (2, 3), (3, 5), (5, 8), (8, 12), (12, 20)]
    for lo, hi in brackets:
        count = sum(1 for v in exclaim_vals if lo <= v < hi)
        pct = count / len(exclaim_vals) * 100
        bar = "█" * int(pct / 2)
        print(f"  [{lo:>2}-{hi:>2}]: {count:3d} ({pct:5.1f}%) {bar}")
    
    # === 多产作者 ===
    print("\n" + "=" * 60)
    print("已知作者统计（按本数排序）")
    print("=" * 60)
    
    author_books = defaultdict(list)
    for r in with_punct:
        if r['author'] != '未知':
            author_books[r['author']].append(r)
    
    for author, books in sorted(author_books.items(), key=lambda x: -len(x[1])):
        if len(books) < 2:
            continue
        ex = [b['exclaim'] for b in books]
        avg_ex = sum(ex) / len(ex)
        print(f"\n{author} ({len(books)}本): 感叹均值={avg_ex:.2f}")
        for b in sorted(books, key=lambda x: x.get('exclaim', 0)):
            print(f"  - {b['title']}: {b.get('exclaim', '?')}/千字")
    
    # === 极端值 ===
    print("\n" + "=" * 60)
    print("感叹号密度 TOP/BOTTOM 10")
    print("=" * 60)
    
    by_exclaim = sorted(with_punct, key=lambda x: x.get('exclaim', 0), reverse=True)
    print("\nTOP 10 最高:")
    for i, r in enumerate(by_exclaim[:10], 1):
        print(f"  {i}. {r['title']}({r['author']}): {r['exclaim']}/千字")
    
    print("\nTOP 10 最低:")
    for i, r in enumerate(by_exclaim[-10:], 1):
        print(f"  {i}. {r['title']}({r['author']}): {r['exclaim']}/千字")
    
    # 省略号
    by_ellipsis = sorted([r for r in with_punct if 'ellipsis' in r], 
                         key=lambda x: x['ellipsis'], reverse=True)
    print("\n省略号密度 TOP 10:")
    for i, r in enumerate(by_ellipsis[:10], 1):
        print(f"  {i}. {r['title']}({r['author']}): {r['ellipsis']}/千字")
    
    # 均句长（过滤异常）
    valid_sentlen = [r for r in with_punct if 'avg_sentence_len' in r and r['avg_sentence_len'] < 100]
    by_sentlen = sorted(valid_sentlen, key=lambda x: x['avg_sentence_len'], reverse=True)
    print("\n均句长 TOP 10 (过滤>100异常):")
    for i, r in enumerate(by_sentlen[:10], 1):
        print(f"  {i}. {r['title']}({r['author']}): {r['avg_sentence_len']}字")
    
    # === 对话比例 ===
    with_dialogue = [r for r in records if 'dialogue_pct' in r]
    if with_dialogue:
        print("\n" + "=" * 60)
        print(f"对话比例统计 (N={len(with_dialogue)})")
        print("=" * 60)
        vals = [r['dialogue_pct'] for r in with_dialogue]
        stats = compute_stats(vals)
        if stats:
            print(f"  均值={stats['mean']}% | 中位={stats['median']}% | min={stats['min']}% | max={stats['max']}%")
        # 分布
        brackets = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 65)]
        for lo, hi in brackets:
            count = sum(1 for v in vals if lo <= v < hi)
            pct = count / len(vals) * 100
            bar = "█" * int(pct / 2)
            print(f"  [{lo:>2}-{hi:>2}%]: {count:3d} ({pct:5.1f}%) {bar}")
    
    # === 保存 JSON ===
    output_path = os.path.join(REPORT_DIR, 'corpus-stats-v2.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'total_reports': len(records),
            'with_exclaim': len(with_punct),
            'with_comma': len(with_comma),
            'with_dialogue': len(with_dialogue),
            'skipped_deep': skipped,
            'records': records,
        }, f, ensure_ascii=False, indent=2)
    print(f"\n数据已保存: {output_path}")

if __name__ == '__main__':
    main()
