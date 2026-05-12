#!/usr/bin/env python3
"""Generate evolution curve visualizations for novel fingerprint data."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import numpy as np

# Try to find Chinese font
chinese_fonts = [f for f in fm.findSystemFonts() if any(k in f.lower() for k in ['cjk', 'noto', 'wqy', 'simhei', 'simsun', 'heiti', 'songti', 'fang'])]
if chinese_fonts:
    plt.rcParams['font.family'] = fm.FontProperties(fname=chinese_fonts[0]).get_name()
else:
    # Fallback: use sans-serif
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']

plt.rcParams['axes.unicode_minus'] = False

OUT = '/root/.openclaw/workspace/novel-corpus-analysis/charts'
os.makedirs(OUT, exist_ok=True)

with open('/root/.openclaw/workspace/novel-txts/fingerprint-results.json') as f:
    data = json.load(f)

novels = {r['name']: r for r in data}

# === Evolution lines ===
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

def plot_evolution(author, names, metrics, filename):
    """Plot evolution curves for one author."""
    valid = [(n, novels[n]) for n in names if n in novels]
    if len(valid) < 2:
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'{author} Evolution Curves', fontsize=16, fontweight='bold')
    
    x_labels = [n for n, _ in valid]
    x = range(len(valid))
    
    metric_info = [
        ('ek', 'Exclamation /1000 chars', '#e74c3c'),
        ('pk', 'Period /1000 chars', '#3498db'),
        ('ck', 'Comma /1000 chars', '#2ecc71'),
        ('lk', 'Ellipsis /1000 chars', '#9b59b6'),
    ]
    
    for idx, (key, title, color) in enumerate(metric_info):
        ax = axes[idx // 2][idx % 2]
        values = [r[key] for _, r in valid]
        ax.plot(x, values, 'o-', color=color, linewidth=2, markersize=8)
        ax.set_title(title, fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=9)
        ax.grid(True, alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(values):
            ax.annotate(f'{v:.1f}', (i, v), textcoords="offset points", 
                       xytext=(0, 10), ha='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(f'{OUT}/{filename}', dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  Saved {filename}')

def plot_all_authors_evolution():
    """Generate evolution curves for all authors with complete lines."""
    print('Generating evolution curves...')
    for author, names in evolutions.items():
        safe_name = author.replace(' ', '_')
        plot_evolution(author, names, ['ek', 'pk', 'ck', 'lk'], f'evolution-{safe_name}.png')

def plot_heatmap():
    """Generate a heatmap of all novels' fingerprint metrics."""
    print('Generating heatmap...')
    
    # Sort by author then name
    sorted_novels = sorted(data, key=lambda r: (r.get('author', ''), r['name']))
    
    # Take top 100 by chars for readability
    sorted_novels = sorted(sorted_novels, key=lambda r: r['chars'], reverse=True)[:100]
    
    names = [r['name'][:6] for r in sorted_novels]
    metrics = ['ck', 'pk', 'ek', 'lk', 'qk', 'avg_sent', 'long30', 'emotion_density', 'cov']
    metric_labels = ['Comma', 'Period', 'Excl', 'Ellipsis', 'Quest', 'AvgSent', 'Long30%', 'Emotion', 'CoV']
    
    matrix = []
    for m in metrics:
        row = [r.get(m, 0) for r in sorted_novels]
        matrix.append(row)
    
    matrix = np.array(matrix, dtype=float)
    
    # Normalize each row to 0-1 for better color mapping
    norm_matrix = np.zeros_like(matrix)
    for i in range(len(metrics)):
        row = matrix[i]
        rmin, rmax = row.min(), row.max()
        if rmax > rmin:
            norm_matrix[i] = (row - rmin) / (rmax - rmin)
        else:
            norm_matrix[i] = 0.5
    
    fig, ax = plt.subplots(figsize=(20, 8))
    im = ax.imshow(norm_matrix, aspect='auto', cmap='YlOrRd', interpolation='nearest')
    
    ax.set_yticks(range(len(metrics)))
    ax.set_yticklabels(metric_labels, fontsize=10)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=90, fontsize=6)
    ax.set_title('Top 100 Novels - Fingerprint Heatmap (row-normalized)', fontsize=14)
    
    plt.colorbar(im, ax=ax, label='Normalized Value')
    plt.tight_layout()
    plt.savefig(f'{OUT}/heatmap-top100.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('  Saved heatmap-top100.png')

def plot_distribution():
    """Generate distribution plots for key metrics."""
    print('Generating distributions...')
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Full Library Distribution (286 novels)', fontsize=16, fontweight='bold')
    
    dist_metrics = [
        ('ek', 'Exclamation /1000', '#e74c3c', 30),
        ('pk', 'Period /1000', '#3498db', 50),
        ('ck', 'Comma /1000', '#2ecc71', 100),
        ('lk', 'Ellipsis /1000', '#9b59b6', 15),
        ('avg_sent', 'Avg Sentence Length', '#e67e22', 80),
        ('emotion_density', 'Emotion Density', '#1abc9c', 50),
    ]
    
    for idx, (key, title, color, xmax) in enumerate(dist_metrics):
        ax = axes[idx // 3][idx % 3]
        values = [r.get(key, 0) for r in data if key in r]
        ax.hist(values, bins=30, color=color, alpha=0.7, edgecolor='white')
        ax.set_title(title, fontsize=12)
        ax.set_xlim(0, xmax)
        ax.axvline(np.median(values), color='black', linestyle='--', linewidth=1, label=f'Median: {np.median(values):.1f}')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUT}/distributions.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('  Saved distributions.png')

# Run all
plot_all_authors_evolution()
plot_heatmap()
plot_distribution()
print('\nDone! All charts saved to', OUT)
