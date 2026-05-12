import re

with open('/root/.openclaw/workspace/novel-corpus/明克街13号.txt', 'r', encoding='gbk', errors='replace') as f:
    text = f.read()

chapters = [(m.start(), m.group()) for m in re.finditer(r'(第[一二三四五六七八九十百零\d]+章\s*\S+)', text)]
ch1_pos = text.find('第一章 床底')

# Categorize ALL quoted content in Ch1-20
ch21_pos = None
for pos, name in chapters:
    if '第二十一' in name and ch21_pos is None:
        ch21_pos = pos

ch20 = text[ch1_pos:ch21_pos]
all_quoted = re.findall(r'\u201c([^\u201d]+)\u201d', ch20)

# Categorize
sounds = []  # pure onomatopoeia
single_words = []  # single word emphasis
thoughts = []  # inner monologue (no speaker attribution near)
dialogue = []  # actual dialogue between characters
broadcast = []  # radio/TV broadcast
unknown = []

# Simple categorization heuristic
for q in all_quoted:
    clean = q.strip()
    # Pure sounds
    if re.match(r'^[\u561b\u549c\u54af\u556a\u53ee\u5413\u54c6\u5475\u5543\u5486\u549f\u5534\u5561\u5486\u55b7\u5578\u568e\u542c\u53f2\u54c0\u5543\u5486\u556a\u5495\u5475\u5634\u54af\u5480\u549f\u5534\u5486\u5534\u5486\u5475\u5578\u5534\u54c0\u5634\u5534\u5486\u5543\u54c0\u561b\u549f\u5534\u5561\u5486\u5486\u55b7\u5543\u54c0\u5634\u5561\u5480\u54c0\u5543\u5486\u561b\u5543\u5486\u556a\u5495\u5475\u5634\u54af\u5480\u549f\u5534\u5486\u5534\u5486\u5475\u5578\u5534\u54c0\u5634\u5534\u5486\u5543\u54c0\u561b\u549f\u5534\u5561\u5486\u5486\u55b7\u5543\u54c0\u5634\u5561\u5480\u54c0\u5543\u5486\u561b\u5543\u5486\u556a\u5495\u5475\u5634\u54af\u5480\u549f\u5534\u5486\u5534\u5486\u5475\u5578\u5534\u54c0\u5634\u5534\u5486\u5543\u54c0\u561b\u549f\u5534\u5561\u5486\u5486\u55b7\u5543\u54c0\u5634\u5561\u5480\u54c0\u5543\u5486\u561b]+', clean):
        sounds.append(clean)
        continue
    # Sounds with dots/dashes
    if re.match(r'^[\u561b\u549c\u54af\u556a\u53ee\u5413\u54c6\u5475\u5543\u5486\u549f\u5534\u5561\u5486\u55b7\u5578\u568e\u542c\u53f2\u54c0\u5543\u5486\u556a\u5495\u5475\u5634\u54af\u5480\u549f\u5534\u5486\u5534\u5486\u5475\u5578\u5534\u54c0\u5634\u5534\u5486\u5543\u54c0\u561b\u549f\u5534\u5561\u5486\u5486\u55b7\u5543\u54c0\u5634\u5561\u5480\u54c0\u5543\u5486\u561b\u5543\u5486\u556a\u5495\u5475\u5634\u54af\u5480\u549f\u5534\u5486\u5534\u5486\u5475\u5578\u5534\u54c0\u5634\u5534\u5486\u5543\u54c0\u561b\u549f\u5534\u5561\u5486\u5486\u55b7\u5543\u54c0\u5634\u5561\u5480\u54c0\u5543\u5486\u561b\u5543\u5486\u556a\u5495\u5475\u5634\u54af\u5480\u549f\u5534\u5486\u5534\u5486\u5475\u5578\u5534\u54c0\u5634\u5534\u5486\u5543\u54c0\u561b\u549f\u5534\u5561\u5486\u5486\u55b7\u5543\u54c0\u5634\u5561\u5480\u54c0\u5543\u5486\u561b\u2026\uff01\u2014\uff0c\u3002\uff1f]+', clean):
        sounds.append(clean)
        continue

print(f'Total quoted segments in Ch1-20: {len(all_quoted)}')

# Let me just do simple stats on quote lengths
lengths = [len(q) for q in all_quoted]
print(f'Avg quote length: {sum(lengths)/len(lengths):.1f} chars')
short = [q for q in all_quoted if len(q) <= 5]
medium = [q for q in all_quoted if 5 < len(q) <= 30]
long_q = [q for q in all_quoted if len(q) > 30]
print(f'Very short (<=5 chars): {len(short)} ({len(short)/len(all_quoted)*100:.1f}%)')
print(f'Medium (6-30 chars): {len(medium)} ({len(medium)/len(all_quoted)*100:.1f}%)')
print(f'Long (>30 chars): {len(long_q)} ({len(long_q)/len(all_quoted)*100:.1f}%)')

# Most common short quotes
from collections import Counter
short_counter = Counter(short)
print('\nMost common short quotes:')
for q, cnt in short_counter.most_common(20):
    print(f'  "{q}" x{cnt}')

# Also check Ch1 only
ch1_text = text[ch1_pos:chapters[1][0]] if len(chapters) > 1 else text[ch1_pos:ch1_pos+10000]
ch1_quoted = re.findall(r'\u201c([^\u201d]+)\u201d', ch1_text)
ch1_short = [q for q in ch1_quoted if len(q) <= 5]
ch1_medium = [q for q in ch1_quoted if 5 < len(q) <= 30]
ch1_long = [q for q in ch1_quoted if len(q) > 30]
print(f'\nCh1 quoted segments: {len(ch1_quoted)}')
print(f'  Short (<=5): {len(ch1_short)} = {len(ch1_short)/len(ch1_quoted)*100:.0f}%')
print(f'  Medium (6-30): {len(ch1_medium)} = {len(ch1_medium)/len(ch1_quoted)*100:.0f}%')
print(f'  Long (>30): {len(ch1_long)} = {len(ch1_long)/len(ch1_quoted)*100:.0f}%')

# Sample short and medium from Ch1
print('\nCh1 short quotes:')
for q in ch1_short[:15]:
    print(f'  "{q}"')

print('\nCh1 medium quotes:')
for q in ch1_medium[:10]:
    print(f'  "{q}"')

# Check Ch 30-35 for later serious/urban sections
ch30_start = None
ch36_start = None
for pos, name in chapters:
    if '第三十' in name and '三十' in name and '第三十章' in name and ch30_start is None:
        ch30_start = pos
    if '第三十六' in name and ch30_start and pos > ch30_start:
        ch36_start = pos
        break

if ch30_start and ch36_start:
    ch30_35 = text[ch30_start:ch36_start]
    ch30_35_quoted = re.findall(r'\u201c([^\u201d]+)\u201d', ch30_35)
    ch30_35_short = [q for q in ch30_35_quoted if len(q) <= 5]
    print(f'\nCh30-35: {len(ch30_35_quoted)} quotes, {len(ch30_35_short)} short ({len(ch30_35_short)/max(len(ch30_35_quoted),1)*100:.0f}%)')

# Check Ch100+ for mature content
ch100_start = None
ch105_start = None
for pos, name in chapters:
    if '第一百章' in name and '一百' in name and ch100_start is None:
        ch100_start = pos
    if '第一百零五' in name and ch100_start and pos > ch100_start:
        ch105_start = pos
        break

if ch100_start and ch105_start:
    ch100_104 = text[ch100_start:ch105_start]
    ch100_quoted = re.findall(r'\u201c([^\u201d]+)\u201d', ch100_104)
    ch100_short = [q for q in ch100_quoted if len(q) <= 5]
    print(f'\nCh100-104: {len(ch100_quoted)} quotes, {len(ch100_short)} short ({len(ch100_short)/max(len(ch100_quoted),1)*100:.0f}%)')
