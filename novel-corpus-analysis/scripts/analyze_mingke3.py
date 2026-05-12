import re

with open('/root/.openclaw/workspace/novel-corpus/明克街13号.txt', 'r', encoding='gbk', errors='replace') as f:
    text = f.read()

chapters = [(m.start(), m.group()) for m in re.finditer(r'(第[一二三四五六七八九十百零\d]+章\s*\S+)', text)]

ch1_pos = text.find('第一章 床底')
ch2_pos = None
for pos, name in chapters:
    if '第二章' in name and pos > ch1_pos:
        ch2_pos = pos
        break

ch1 = text[ch1_pos:ch2_pos]

# Line structure analysis
lines = ch1.split('\n')
non_empty = [l.strip() for l in lines if l.strip()]
print(f'Total non-empty lines in Ch1: {len(non_empty)}')

dialogue_line_count = sum(1 for l in non_empty if '\u201c' in l or '\u201d' in l)
print(f'Lines with quotation marks: {dialogue_line_count}')
print(f'Dialogue line ratio: {dialogue_line_count/len(non_empty)*100:.1f}%')

# Show line-by-line first 60
print('\n=== Ch1 line samples ===')
for i, l in enumerate(non_empty[:60]):
    has_q = '\u201c' in l or '\u201d' in l
    marker = '>>>' if has_q else '   '
    print(f'{marker} [{i+1}] {l[:90]}')

# Check Ch9 for special format
ch9_start = None
ch10_start = None
for pos, name in chapters:
    if '第九' in name and pos > ch1_pos:
        ch9_start = pos
    if '第十章' in name and ch9_start and pos > ch9_start:
        ch10_start = pos
        break

if ch9_start and ch10_start:
    ch9 = text[ch9_start:ch10_start]
    ch9_lines = [l.strip() for l in ch9.split('\n') if l.strip()]
    ch9_dial = sum(1 for l in ch9_lines if '\u201c' in l or '\u201d' in l)
    print(f'\nCh9: {len(ch9_lines)} lines, {ch9_dial} dialogue lines, ratio={ch9_dial/len(ch9_lines)*100:.1f}%')
    print('\nCh9 first 40 lines:')
    for i, l in enumerate(ch9_lines[:40]):
        has_q = '\u201c' in l or '\u201d' in l
        marker = '>>>' if has_q else '   '
        print(f'{marker} [{i+1}] {l[:90]}')

# Also look at Ch13 (犯罪心理) - 47.7% dialogue
ch13_start = None
ch14_start = None
for pos, name in chapters:
    if '第十三' in name and pos > ch1_pos:
        ch13_start = pos
    if '第十四' in name and ch13_start and pos > ch13_start:
        ch14_start = pos
        break

if ch13_start and ch14_start:
    ch13 = text[ch13_start:ch14_start]
    ch13_lines = [l.strip() for l in ch13.split('\n') if l.strip()]
    ch13_dial = sum(1 for l in ch13_lines if '\u201c' in l or '\u201d' in l)
    print(f'\nCh13: {len(ch13_lines)} lines, {ch13_dial} dialogue lines, ratio={ch13_dial/len(ch13_lines)*100:.1f}%')
    print('\nCh13 first 40 lines:')
    for i, l in enumerate(ch13_lines[:40]):
        has_q = '\u201c' in l or '\u201d' in l
        marker = '>>>' if has_q else '   '
        print(f'{marker} [{i+1}] {l[:90]}')
