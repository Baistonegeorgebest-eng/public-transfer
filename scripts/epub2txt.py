#!/usr/bin/env python3
"""
EPUB → TXT 转换脚本
用法: python3 epub2txt.py 输入.epub [输出.txt]
      python3 epub2txt.py *.epub (批量)
"""
import zipfile, html, os, sys, re
from xml.etree import ElementTree as ET

def epub_to_text(epub_path):
    with zipfile.ZipFile(epub_path) as z:
        opf_files = [f for f in z.namelist() if f.endswith('.opf')]
        if not opf_files:
            raise ValueError('未找到 OPF 文件')
        
        opf = ET.parse(z.open(opf_files[0]))
        ns = {'opf': 'http://www.idpf.org/2007/opf'}
        
        manifest = {}
        for item in opf.findall('.//opf:item', ns):
            item_id = item.get('id')
            href = item.get('href')
            if item_id and href:
                manifest[item_id] = href
        
        spine_order = []
        for itemref in opf.findall('.//opf:itemref', ns):
            idref = itemref.get('idref')
            if idref and idref in manifest:
                spine_order.append(manifest[idref])
        
        opf_dir = os.path.dirname(opf_files[0])
        
        texts = []
        for rel_path in spine_order:
            full_path = os.path.join(opf_dir, rel_path) if opf_dir else rel_path
            if full_path not in z.namelist():
                full_path = rel_path
                if full_path not in z.namelist():
                    continue
            content = z.read(full_path).decode('utf-8', errors='replace')
            text = re.sub(r'<[^>]+>', ' ', content)
            text = html.unescape(text)
            text = re.sub(r'\s+', ' ', text).strip()
            # 过滤过短页面（封面、版权页等）
            if len(text) > 50:
                texts.append(text)
        
        return '\n\n'.join(texts)

def main():
    files = [a for a in sys.argv[1:] if a.endswith('.epub')]
    if not files:
        print('用法: python3 epub2txt.py 输入.epub [输出.txt]')
        sys.exit(1)
    
    for epub_path in files:
        out_path = epub_path.replace('.epub', '.txt')
        # 如果第二个参数指定了输出文件名，只对第一个文件生效
        if files.index(epub_path) == 0 and len(sys.argv) > 2 and not sys.argv[2].endswith('.epub'):
            out_path = sys.argv[2]
        
        print(f'🔄 {os.path.basename(epub_path)} → {os.path.basename(out_path)} ...', end=' ')
        try:
            text = epub_to_text(epub_path)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(text)
            kb = os.path.getsize(out_path) / 1024
            print(f'✅ {kb:.0f}KB')
        except Exception as e:
            print(f'❌ {e}')

if __name__ == '__main__':
    main()
