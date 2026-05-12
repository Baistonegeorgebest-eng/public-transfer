#!/usr/bin/env python3
"""
Update fingerprint-results.json with corrected author info from doubao list.
- Fill missing author fields (127 entries)
- Correct existing wrong author fields (32 entries)
"""
import json
import re

# Parse the corrected author list
def parse_author_list(path):
    """Parse 《书名》——作者：（作者名） [字数] format"""
    authors = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Match: 《书名》——作者：（作者名） [字数]
            m = re.match(r'《(.+?)》——作者：（(.+?)）\s*\[', line)
            if m:
                name = m.group(1)
                author = m.group(2)
                authors[name] = author
            else:
                print(f"  [WARN] Could not parse: {line}")
    return authors

# Load data
with open('novel-txts/fingerprint-results.json', encoding='utf-8') as f:
    data = json.load(f)

corrections = parse_author_list('全部小说清单校正版-doubao.md')
print(f"Parsed {len(corrections)} author entries from corrected full list")

# Build name->index lookup
name_to_idx = {}
for i, entry in enumerate(data):
    name_to_idx[entry['name']] = i

# Apply updates
added = 0
corrected = 0
unchanged = 0
not_found = []

for novel_name, author in corrections.items():
    if novel_name not in name_to_idx:
        not_found.append(novel_name)
        continue
    
    idx = name_to_idx[novel_name]
    entry = data[idx]
    old_author = entry.get('author', '')
    
    if not old_author or old_author.strip() in ('', '未知'):
        # Missing author - add it
        entry['author'] = author
        added += 1
        print(f"  [ADD] 《{novel_name}》 -> {author}")
    elif old_author != author:
        # Wrong author - correct it
        entry['author'] = author
        corrected += 1
        print(f"  [FIX] 《{novel_name}》: {old_author} -> {author}")
    else:
        unchanged += 1

# Save updated JSON
with open('novel-txts/fingerprint-results.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n=== Summary ===")
print(f"Total in doubao list: {len(corrections)}")
print(f"Authors added (was missing): {added}")
print(f"Authors corrected (was wrong): {corrected}")
print(f"Already correct: {unchanged}")
print(f"Not found in JSON: {len(not_found)}")
if not_found:
    print(f"  Missing novels: {', '.join(not_found[:10])}")

# Final stats
has_author = sum(1 for d in data if d.get('author') and d['author'].strip())
no_author = sum(1 for d in data if not d.get('author') or d['author'].strip() in ('', '未知'))
print(f"\nFinal: {has_author} with author, {no_author} without (total {len(data)})")
