#!/usr/bin/env python3
"""Analyze new novels and add to fingerprint JSON."""
import json, re, os

def analyze_novel(filepath, name, author):
    """Run basic fingerprint analysis on a novel file."""
    # Read with encoding detection
    for enc in ['utf-8', 'gbk', 'gb18030', 'gb2312']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                text = f.read()
            break
        except:
            text = None
    if text is None:
        with open(filepath, 'rb') as f:
            raw = f.read()
        text = raw.decode('gbk', errors='replace')
    
    # Clean text
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Character count (exclude whitespace)
    chars = len(re.sub(r'\s', '', text))
    
    # Count punctuation
    comma_count = text.count('，')
    period_count = text.count('。')
    excl_count = text.count('！')
    ellipsis_count = text.count('……')
    question_count = text.count('？')
    
    # Per-1000-char rates
    ck = comma_count / chars * 1000 if chars else 0
    pk = period_count / chars * 1000 if chars else 0
    ek = excl_count / chars * 1000 if chars else 0
    lk = ellipsis_count / chars * 1000 if chars else 0
    qk = question_count / chars * 1000 if chars else 0
    
    # Sentence analysis
    sentences = re.split(r'[。！？]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 2]
    if sentences:
        sent_lengths = [len(re.sub(r'\s', '', s)) for s in sentences]
        avg_sent = sum(sent_lengths) / len(sent_lengths)
        med_sent = sorted(sent_lengths)[len(sent_lengths)//2]
        long30 = sum(1 for l in sent_lengths if l > 30) / len(sent_lengths) * 100
        short10 = sum(1 for l in sent_lengths if l < 10) / len(sent_lengths) * 100
    else:
        avg_sent = med_sent = long30 = short10 = 0
    
    # Paragraph analysis
    paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 10]
    if paragraphs:
        para_lengths = [len(re.sub(r'\s', '', p)) for p in paragraphs]
        avg_para = sum(para_lengths) / len(para_lengths)
    else:
        avg_para = 0
    
    # Chapter count (approximate)
    chapters = len(re.findall(r'第[一二三四五六七八九十百千\d]+章', text))
    
    # Sentence length CoV
    if len(sent_lengths) > 1:
        mean_sl = avg_sent
        variance = sum((x - mean_sl)**2 for x in sent_lengths) / len(sent_lengths)
        cov = (variance ** 0.5) / mean_sl if mean_sl else 0
    else:
        cov = 0
    
    # Emotion density (exclamation + question + ellipsis per paragraph)
    emotion_density = (excl_count + question_count + ellipsis_count) / max(len(paragraphs), 1) * 1000
    
    return {
        'name': name,
        'chars': chars,
        'chapters': chapters,
        'ck': round(ck, 1),
        'pk': round(pk, 1),
        'ek': round(ek, 2),
        'lk': round(lk, 2),
        'qk': round(qk, 1),
        'avg_sent': round(avg_sent, 1),
        'med_sent': round(med_sent, 1),
        'cov': round(cov, 3),
        'long30': round(long30, 1),
        'short10': round(short10, 1),
        'avg_para': round(avg_para, 1),
        'emotion_density': round(emotion_density, 1),
        'author': author,
    }

# Load existing data
with open('novel-txts/fingerprint-results.json') as f:
    data = json.load(f)

existing_names = {d['name'] for d in data}

# New novels to add
new_novels = [
    ('格兰自然科学院-utf8.txt', '格兰自然科学院', '一行白鹭上青天'),
    ('超级浮空城.txt-utf8.txt', '超级浮空城', '诸生浮屠'),
    ('超维度玩家.txt-utf8.txt', '超维度玩家', '诸生浮屠'),
    ('深渊主宰-新-utf8.txt', '深渊主宰', '诸生浮屠'),  # duplicate check
]

for filename, name, author in new_novels:
    filepath = f'novel-txts/{filename}'
    if not os.path.exists(filepath):
        print(f"  [SKIP] {filepath} not found")
        continue
    if name in existing_names:
        print(f"  [SKIP] {name} already in JSON (author: {[d.get('author') for d in data if d['name']==name]})")
        continue
    result = analyze_novel(filepath, name, author)
    data.append(result)
    existing_names.add(name)
    print(f"  [ADD] {name}: chars={result['chars']}, ck={result['ck']}, pk={result['pk']}, ek={result['ek']}, lk={result['lk']}, author={result['author']}")

# Save
with open('novel-txts/fingerprint-results.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal entries: {len(data)}")
