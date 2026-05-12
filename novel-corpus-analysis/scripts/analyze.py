#!/usr/bin/env python3
"""Punctuation fingerprint analysis for Chinese novels.
Outputs: comma, period, exclamation, ellipsis, question per 1000 chars + dialogue ratio + chapter stats."""
import os, re, sys
from collections import Counter

D = "/root/.openclaw/workspace/novel-corpus"

def analyze(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    
    # Basic counts
    total_chars = len(text.replace('\n', '').replace('\r', '').replace(' ', ''))
    if total_chars < 1000:
        return None
    
    # Punctuation counts
    comma = text.count('，') + text.count(',')
    period = text.count('。') + text.count('.')
    exclamation = text.count('！') + text.count('!')
    ellipsis = text.count('……') + text.count('...')  # Count pairs for Chinese ellipsis
    ellipsis_single = text.count('…')  # Also count single
    question = text.count('？') + text.count('?')
    
    # Per 1000 chars
    k = total_chars / 1000
    comma_k = comma / k
    period_k = period / k
    excl_k = exclamation / k
    ellipsis_k = ellipsis / k
    quest_k = question / k
    
    # Dialogue detection: text between 「」or "" or ""
    # Chinese novels use various quote styles
    dialogue_chars = 0
    for pattern in [r'「[^」]*」', r'""', r'""', r'「[^」]*」']:
        for m in re.finditer(pattern, text):
            dialogue_chars += len(m.group())
    dialogue_pct = (dialogue_chars / total_chars * 100) if total_chars > 0 else 0
    
    # Chapter count
    chapters = len(re.findall(r'第[一二三四五六七八九十百千\d]+[章回节]', text))
    if chapters == 0:
        chapters = len(re.findall(r'(?m)^chapter\s*\d+', text, re.IGNORECASE))
    if chapters == 0:
        # Rough estimate: every 3000 chars = 1 chapter
        chapters = max(1, total_chars // 3000)
    
    # Exclamation per chapter
    excl_per_ch = exclamation / max(chapters, 1)
    ellipsis_per_ch = ellipsis / max(chapters, 1)
    
    # Sentence length analysis
    sentences = re.split(r'[。！？…]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    if sentences:
        lengths = [len(s.replace(' ', '')) for s in sentences]
        avg_sent = sum(lengths) / len(lengths)
        long_pct = sum(1 for l in lengths if l > 30) / len(lengths) * 100
        median_sent = sorted(lengths)[len(lengths)//2]
    else:
        avg_sent = 0
        long_pct = 0
        median_sent = 0
    
    # "似乎" and "可能" frequency
    seem_freq = (text.count('似乎') + text.count('好像') + text.count('仿佛')) / (total_chars/10000)
    maybe_freq = (text.count('可能') + text.count('也许') + text.count('或许')) / (total_chars/10000)
    
    return {
        'chars': total_chars,
        'chapters': chapters,
        'comma_k': comma_k,
        'period_k': period_k,
        'excl_k': excl_k,
        'ellipsis_k': ellipsis_k,
        'quest_k': quest_k,
        'excl_per_ch': excl_per_ch,
        'ellipsis_per_ch': ellipsis_per_ch,
        'dialogue_pct': dialogue_pct,
        'avg_sent': avg_sent,
        'long_pct': long_pct,
        'median_sent': median_sent,
        'seem_freq': seem_freq,
        'maybe_freq': maybe_freq,
    }

# Run
results = {}
for f in sorted(os.listdir(D)):
    if f.endswith('.txt'):
        path = os.path.join(D, f)
        name = f.replace('.txt', '')
        r = analyze(path)
        if r:
            results[name] = r

# Output table
print(f"{'小说':<16} {'字数':>6} {'逗号':>6} {'句号':>6} {'感叹':>6} {'省略':>6} {'问号':>6} {'对白%':>6} {'均句长':>5} {'长句%':>5} {'感叹/章':>7} {'省略/章':>7} {'似乎':>5} {'可能':>5}")
print("-" * 130)
for name in sorted(results.keys(), key=lambda x: results[x]['chars'], reverse=True):
    r = results[name]
    chars_m = r['chars'] / 10000
    print(f"{name:<16} {chars_m:>5.0f}万 {r['comma_k']:>5.1f} {r['period_k']:>5.1f} {r['excl_k']:>5.2f} {r['ellipsis_k']:>5.1f} {r['quest_k']:>5.1f} {r['dialogue_pct']:>5.1f}% {r['avg_sent']:>4.0f} {r['long_pct']:>4.1f}% {r['excl_per_ch']:>6.1f} {r['ellipsis_per_ch']:>6.1f} {r['seem_freq']:>4.1f} {r['maybe_freq']:>4.1f}")

# Also output as data for protocol
print("\n\n=== DATA FOR PROTOCOL ===")
for name in sorted(results.keys(), key=lambda x: results[x]['chars'], reverse=True):
    r = results[name]
    print(f"| (待定作者)({name}) | {r['comma_k']:.1f} | {r['period_k']:.1f} | {r['excl_k']:.2f} | {r['ellipsis_k']:.2f} | {r['dialogue_pct']:.1f} | (待分析) |")
