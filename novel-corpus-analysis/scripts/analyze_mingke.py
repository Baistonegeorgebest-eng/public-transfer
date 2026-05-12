import re

with open('/root/.openclaw/workspace/novel-corpus/明克街13号.txt', 'r', encoding='gbk', errors='replace') as f:
    text = f.read()

# Get chapter positions
chapters = [(m.start(), m.group()) for m in re.finditer(r'(第[一二三四五六七八九十百零\d]+章\s*\S+)', text)]

ch1_pos = text.find('第一章 床底')
ch6_pos = None
ch21_pos = None

for pos, name in chapters:
    if '第六' in name and ch6_pos is None:
        ch6_pos = pos
    if '第二十一' in name and ch21_pos is None:
        ch21_pos = pos

print(f'Total chars: {len(text)}')
print(f'Total chapters: {len(chapters)}')

# Ch1-20 content
ch20_text = text[ch1_pos:ch21_pos]

# Count various punctuation
left_q = ch20_text.count('\u201c')
right_q = ch20_text.count('\u201d')
excl = ch20_text.count('\uff01') + ch20_text.count('!')
ellipsis = ch20_text.count('\u2026\u2026')
qmark = ch20_text.count('\uff1f') + ch20_text.count('?')

print(f'\n=== Ch1-20 Overview ===')
print(f'Total chars: {len(ch20_text)}')
print(f'Left/Right quotes: {left_q}/{right_q}')
print(f'Exclamation marks: {excl}')
print(f'Ellipsis: {ellipsis}')
print(f'Question marks: {qmark}')

# Dialogue ratio
quoted = re.findall(r'\u201c[^\u201d]*\u201d', ch20_text)
dialogue_chars = sum(len(q) for q in quoted)
print(f'Dialogue chars: {dialogue_chars}')
print(f'Dialogue ratio: {dialogue_chars/len(ch20_text)*100:.1f}%')

# Per-chapter analysis
print('\n=== Per-chapter analysis (Ch1-20) ===')
ch_starts = [(pos, name) for pos, name in chapters if pos >= ch1_pos and pos < ch21_pos]

for i in range(min(len(ch_starts), 20)):
    start = ch_starts[i][0]
    end = ch_starts[i+1][0] if i+1 < len(ch_starts) else ch21_pos
    name = ch_starts[i][1]
    ch_text = text[start:end]
    ch_len = len(ch_text)
    excl_count = ch_text.count('\uff01') + ch_text.count('!')
    excl_rate = excl_count / (ch_len / 1000)
    ellipsis_count = ch_text.count('\u2026\u2026')
    ch_quoted = re.findall(r'\u201c[^\u201d]*\u201d', ch_text)
    ch_dial_chars = sum(len(q) for q in ch_quoted)
    ch_dial_ratio = ch_dial_chars / ch_len * 100 if ch_len > 0 else 0
    print(f'{name}: len={ch_len} | excl={excl_count}/{excl_rate:.2f}/千字 | ellipsis={ellipsis_count} | dialogue={ch_dial_ratio:.1f}%')

# Ch1-5 content
print('\n=== Ch1-5 Opening ===')
ch15 = text[ch1_pos:ch6_pos]
print(f'Ch1-5 chars: {len(ch15)}')

keywords = ['\u602a', '\u9b3c', '\u6b7b', '\u6740', '\u8840', '\u6697', '\u9ed1', '\u6050', '\u60e7', '\u9b54', '\u5f02', '\u7075', '\u90aa', '\u6076', '\u5f71', '\u6028', '\u9b42']
kw_names = ['怪','鬼','死','杀','血','暗','黑','恐','惧','魔','异','灵','邪','恶','影','怨','魂']
print('Horror keywords in Ch1-5:')
for kw, kwn in zip(keywords, kw_names):
    count = ch15.count(kw)
    if count > 0:
        print(f'  {kwn}: {count}')

# Dialogue samples from Ch1
ch1 = text[ch1_pos:ch6_pos]
dialogue_lines = re.findall(r'\u201c[^\u201d]+\u201d', ch1)
print(f'\nDialogue lines in Ch1: {len(dialogue_lines)}')
for i, dl in enumerate(dialogue_lines[:15]):
    clean = dl.strip('\u201c\u201d')
    print(f'  {i+1}. [{len(clean)}chars] {dl[:100]}')

# Short dialogue fragments
print('\nShort dialogue fragments (<=5 chars):')
for dl in dialogue_lines:
    clean = dl.strip('\u201c\u201d')
    if len(clean) <= 5:
        print(f'  "{clean}"')

# Check self-talk / inner monologue patterns
# Lines with ... at start or short lines alone on their own line
single_line_dialogues = [dl for dl in dialogue_lines if len(dl.strip('\u201c\u201d')) <= 3]
print(f'\nVery short dialogue (<=3 chars): {len(single_line_dialogues)}')
for dl in single_line_dialogues[:20]:
    print(f'  {dl}')
