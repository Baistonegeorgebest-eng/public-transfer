import re

with open('/root/.openclaw/workspace/novel-corpus/明克街13号.txt', 'r', encoding='gbk', errors='replace') as f:
    text = f.read()

# Check a wider sample for dialogue format patterns
chapters = [(m.start(), m.group()) for m in re.finditer(r'(第[一二三四五六七八九十百零\d]+章\s*\S+)', text)]

# Get Ch1 content raw for format analysis
ch1_pos = text.find('第一章 床底')
ch2_pos = None
for pos, name in chapters:
    if '第二章' in name and pos > ch1_pos:
        ch2_pos = pos
        break

ch1 = text[ch1_pos:ch2_pos]

# Categorize dialogue lines
dialogue_lines = re.findall(r'\u201c([^\u201d]+)\u201d', ch1)

# Categorize each
sound_effects = []
inner_thoughts = []
actual_dialogue = []
emphasis_words = []

for dl in dialogue_lines:
    # Sound effects: mostly onomatopoeia with dashes
    if re.match(r'^[\u549c\u54af\u55b7\u5403\u54ee\u53eb\u5305\u54e5\u5403\u568e\u5578\u5634\u5486\u5389\u54c0\u54e5\u5415\u5480\u556a\u53ee\u5543\u5403\u54bd\u5475\u53f9\u54c6\u5410\u547c\u5634\u5438\u5471\u5527\u5543\u5486\u548c\u556d\u5543\u53eb\u53f9\u5475\u5634\u53f7\u556a\u5413\u542c\u54ac\u5403\u542c\u55b7\u542c\u5440\u5566\u5434\u54cd\u5443\u54af\u542c\u53f2\u5578\u5486\u55b7\u5534\u5561\u561b\u5561\u54c0\u5543\u53d6\u54ac\u5475\u5471\u5480\u5438\u5543\u54c0\u5561\u561b\u54c0\u5543\u5495\u568e\u5471\u5561\u5486\u55b7\u5543\u54c0\u5634\u5561\u5480\u54c0\u5543\u5486\u561b\u5543\u5486\u556a\u5495\u5475\u5634\u54af\u5480\u549f\u5534\u5486\u5534\u5486\u5475\u5634\u54c0\u549f\u5534\u5486\u5486\u5475\u5578\u5534\u54c0\u5634\u5534\u5486\u5543\u54c0\u561b\u549f\u5534\u5561\u5486\u5486\u55b7\u5543\u54c0\u5634\u5561\u5480\u54c0\u5543\u5486\u561b\u5543\u5486\u556a\u5495\u5475\u5634\u54af\u5480\u549f\u5534\u5486\u5534\u5486\u5475\u5578\u5534\u54c0\u5634\u5534\u5486\u5543\u54c0\u561b\u549f\u5534\u5561\u5486\u5486\u55b7\u5543\u54c0\u5634\u5561\u5480\u54c0\u5543\u5486\u561b]', dl):
        sound_effects.append(dl)
    elif len(dl) <= 3 and ('…' in dl or '！' in dl or '。' in dl):
        sound_effects.append(dl)
    elif len(dl) <= 3:
        emphasis_words.append(dl)
    elif dl in ['……']:
        sound_effects.append(dl)

print(f'Ch1 dialogue lines: {len(dialogue_lines)}')
print(f'  Sound effects: {len(sound_effects)}')
print(f'  Emphasis words: {len(emphasis_words)}')

# Actually let me take a different approach - just look at the format
# Key question: WHY is dialogue ratio 109%? 
# Possible: dialogue lines count / total narration lines, where dialogue takes more lines
# Let me count lines
print('\n=== Line structure analysis ===')
lines = ch1.split('\n')
non_empty = [l.strip() for l in lines if l.strip()]
print(f'Total non-empty lines in Ch1: {len(non_empty)}')

# Count lines that contain dialogue markers
dialogue_line_count = sum(1 for l in non_empty if '\u201c' in l or '\u201d' in l)
print(f'Lines with quotation marks: {dialogue_line_count}')
print(f'Dialogue line ratio: {dialogue_line_count/len(non_empty)*100:.1f}%')

# Check if the 109% might mean (dialogue chars + dialogue attribution) / narration chars 
# Or dialogue lines / total lines * multi-line factor
# Let me check line-by-line more carefully
print('\n=== Ch1 line samples (first 60 lines) ===')
for i, l in enumerate(non_empty[:60]):
    has_q = '\u201c' in l or '\u201d' in l
    marker = '>>>' if has_q else '   '
    print(f'{marker} [{i+1}] {l[:80]}')

# Also check the "收音机" (radio) narrative device which might explain high dialogue
print('\n=== Radio device analysis ===')
radio_count = text[ch1_pos:ch2_pos].count('收音机')
print(f'Radio mentions in Ch1: {radio_count}')

# Check Ch 9 (这章很精彩) - dialogue 29.3% - might have special format
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
    ch9_dial_lines = sum(1 for l in ch9_lines if '\u201c' in l or '\u201d' in l)
    print(f'\nCh9: {len(ch9_lines)} lines, {ch9_dial_lines} dialogue lines, ratio={ch9_dial_lines/len(ch9_lines)*100:.1f}%')
    
    # Show first 30 lines of Ch9
    print('\nCh9 first 30 lines:')
    for i, l in enumerate(ch9_lines[:30]):
        has_q = '\u201c' in l or '\u201d' in l
        marker = '>>>' if has_q else '   '
        print(f'{marker} [{i+1}] {l[:90]}')
