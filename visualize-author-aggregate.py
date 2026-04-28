#!/usr/bin/env python3
"""Generate author-aggregated evolution curves: all authors on same axes for comparison."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import numpy as np

# Chinese font setup
chinese_fonts = [f for f in fm.findSystemFonts() if any(k in f.lower() for k in ['cjk', 'noto', 'wqy', 'simhei', 'simsun', 'heiti', 'songti', 'fang'])]
if chinese_fonts:
    prop = fm.FontProperties(fname=chinese_fonts[0])
    plt.rcParams['font.family'] = prop.get_name()
    FONT = chinese_fonts[0]
else:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
    FONT = None

plt.rcParams['axes.unicode_minus'] = False

OUT = '/root/.openclaw/workspace/novel-corpus-analysis/charts'
os.makedirs(OUT, exist_ok=True)

with open('/root/.openclaw/workspace/novel-txts/fingerprint-results.json') as f:
    data = json.load(f)

novels = {r['name']: r for r in data}

evolutions = {
    '远瞳': ['希灵帝国', '异常生物见闻录', '黎明之剑', '深海余烬'],
    '会说话的肘子': ['英雄联盟之灾变时代', '大王饶命', '夜的命名术'],
    '皇甫奇': ['人皇纪', '帝御山河', '飞升之后', '大周皇族', '神座', '无上真魔'],
    '梦入神机': ['星峰传说', '佛本是道', '龙蛇演义', '圣王', '星河大帝', '拳镇山河', '点道为止'],
    '天蚕土豆': ['魔兽剑圣异界纵横', '斗破苍穹', '武动乾坤', '大主宰', '元尊'],
    '猫腻': ['朱雀记', '间客', '庆余年', '将夜', '择天记', '大道朝天'],
    '血红': ['升龙道', '邪龙道', '逆龙道', '偷天', '光明纪元', '三界血歌', '开天录'],
    '烽火戏诸侯': ['极品公子', '陈二狗的妖孽人生', '剑来'],
    '耳根': ['仙逆', '求魔', '我欲封天', '一念永恒', '三寸人间'],
}

# Also add more authors from the fingerprint data
more_authors = {}
for r in data:
    author = r.get('author', '')
    if author and author != '—' and author not in evolutions and author != '？':
        if author not in more_authors:
            more_authors[author] = []
        more_authors[author].append(r['name'])

# Keep only authors with 3+ novels
more_authors = {k: v for k, v in more_authors.items() if len(v) >= 3}

colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#e67e22', '#1abc9c', 
          '#f1c40f', '#e84393', '#00cec9', '#6c5ce7', '#fd79a8', '#55a3e8',
          '#a29bfe', '#fab1a0', '#81ecec', '#ffeaa7']

def plot_aggregated(metric_key, metric_label, filename):
    """Plot all authors on same chart for one metric."""
    fig, ax = plt.subplots(figsize=(16, 10))
    
    all_valid = [(auth, names) for auth, names in evolutions.items() 
                 if sum(1 for n in names if n in novels) >= 2]
    
    for idx, (author, names) in enumerate(all_valid):
        valid = [(n, novels[n]) for n in names if n in novels]
        if len(valid) < 2:
            continue
        x = range(len(valid))
        values = [r[metric_key] for _, r in valid]
        color = colors[idx % len(colors)]
        
        ax.plot(x, values, 'o-', color=color, linewidth=2, markersize=7, label=author, alpha=0.85)
        
        # Label last point
        ax.annotate(author, (len(valid)-1, values[-1]), 
                   textcoords="offset points", xytext=(8, 0),
                   fontsize=9, color=color, fontweight='bold')
    
    ax.set_title(f'Author Aggregated Evolution: {metric_label}', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Novel Index (chronological)', fontsize=12)
    ax.set_ylabel(metric_label, fontsize=12)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUT}/{filename}', dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  Saved {filename}')

def plot_all_4metrics_grid():
    """Single figure with 4 subplots, each showing all authors for one metric."""
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('Author Evolution Comparison (9 Authors × 4 Metrics)', fontsize=18, fontweight='bold')
    
    metrics = [
        ('ek', 'Exclamation /1000 chars'),
        ('pk', 'Period /1000 chars'),
        ('ck', 'Comma /1000 chars'),
        ('lk', 'Ellipsis /1000 chars'),
    ]
    
    all_valid = [(auth, names) for auth, names in evolutions.items() 
                 if sum(1 for n in names if n in novels) >= 2]
    
    for midx, (key, label) in enumerate(metrics):
        ax = axes[midx // 2][midx % 2]
        
        for idx, (author, names) in enumerate(all_valid):
            valid = [(n, novels[n]) for n in names if n in novels]
            if len(valid) < 2:
                continue
            x = range(len(valid))
            values = [r[key] for _, r in valid]
            color = colors[idx % len(colors)]
            ax.plot(x, values, 'o-', color=color, linewidth=1.5, markersize=5, label=author, alpha=0.8)
        
        ax.set_title(label, fontsize=13, fontweight='bold')
        ax.legend(fontsize=7, loc='best', ncol=2)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUT}/aggregated-4metrics-grid.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('  Saved aggregated-4metrics-grid.png')

def plot_more_authors():
    """Plot additional authors with 3+ novels."""
    more_keys = sorted(more_authors.keys())
    if not more_keys:
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('Additional Authors Evolution (3+ novels)', fontsize=18, fontweight='bold')
    
    metrics = [
        ('ek', 'Exclamation /1000 chars'),
        ('pk', 'Period /1000 chars'),
        ('ck', 'Comma /1000 chars'),
        ('lk', 'Ellipsis /1000 chars'),
    ]
    
    for midx, (key, label) in enumerate(metrics):
        ax = axes[midx // 2][midx % 2]
        
        for idx, author in enumerate(more_keys[:15]):
            names = more_authors[author]
            valid = [(n, novels[n]) for n in names if n in novels]
            if len(valid) < 2:
                continue
            x = range(len(valid))
            values = [r[key] for _, r in valid]
            color = colors[idx % len(colors)]
            ax.plot(x, values, 'o-', color=color, linewidth=1.5, markersize=5, label=author, alpha=0.8)
        
        ax.set_title(label, fontsize=13, fontweight='bold')
        ax.legend(fontsize=7, loc='best', ncol=2)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUT}/aggregated-additional-authors.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('  Saved aggregated-additional-authors.png')

print('Generating aggregated charts...')
plot_aggregated('ek', 'Exclamation /1000 chars', 'aggregated-exclamation.png')
plot_aggregated('pk', 'Period /1000 chars', 'aggregated-period.png')
plot_aggregated('ck', 'Comma /1000 chars', 'aggregated-comma.png')
plot_aggregated('lk', 'Ellipsis /1000 chars', 'aggregated-ellipsis.png')
plot_all_4metrics_grid()
plot_more_authors()
print('Done!')
