#!/usr/bin/env python3
"""Generate evolution charts for newly discovered authors + updated ones."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

# Font setup
chinese_fonts = [f for f in fm.findSystemFonts() if any(k in f.lower() for k in ['cjk', 'noto', 'wqy', 'simhei', 'simsun', 'heiti', 'songti', 'fang'])]
if chinese_fonts:
    plt.rcParams['font.family'] = fm.FontProperties(fname=chinese_fonts[0]).get_name()
else:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

with open('novel-txts/fingerprint-results.json', encoding='utf-8') as f:
    data = json.load(f)

os.makedirs('novel-corpus-analysis/charts', exist_ok=True)

def plot_evolution(author, novels_ordered, metrics, title_suffix=''):
    """Generate a 2x2 evolution chart for an author."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'{author} 进化线{title_suffix}', fontsize=16, fontweight='bold')
    
    metric_info = {
        'ek': ('感叹/千', '#e74c3c'),
        'ck': ('逗号/千', '#3498db'),
        'pk': ('句号/千', '#2ecc71'),
        'lk': ('省略/千', '#f39c12'),
        'avg_sent': ('均句(字)', '#9b59b6'),
        'avg_para': ('段均(字)', '#1abc9c'),
        'long30': ('长30%(%)', '#e67e22'),
        'short10': ('短10%(%)', '#34495e'),
    }
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx // 2][idx % 2]
        label, color = metric_info.get(metric, (metric, '#333'))
        values = [n.get(metric, 0) for n in novels_ordered]
        names = [n['name'][:6] for n in novels_ordered]
        x = range(len(values))
        
        ax.plot(x, values, 'o-', color=color, linewidth=2, markersize=8)
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=30, ha='right', fontsize=9)
        ax.set_ylabel(label, fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Annotate values
        for i, v in enumerate(values):
            ax.annotate(f'{v:.1f}', (i, v), textcoords='offset points', xytext=(0, 10), ha='center', fontsize=9)
    
    plt.tight_layout()
    path = f'novel-corpus-analysis/charts/evolution-{author}.png'
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {path}')

def get_novels_by_author(author):
    novels = [d for d in data if d.get('author') == author]
    return sorted(novels, key=lambda x: x.get('chars', 0))

# Generate charts
authors_to_plot = {
    '百里玺': ['ek', 'ck', 'pk', 'avg_sent'],
    '猪头七': ['ek', 'ck', 'avg_sent', 'long30'],
    '风凌天下': ['ek', 'ck', 'lk', 'avg_sent'],
    '文抄公': ['ek', 'ck', 'lk', 'avg_sent'],
    '余云飞': ['ek', 'ck', 'pk', 'avg_sent'],
    '诸生浮屠': ['ek', 'ck', 'pk', 'avg_sent'],
    '迪巴拉爵士': ['ek', 'ck', 'avg_sent', 'long30'],
}

for author, metrics in authors_to_plot.items():
    novels = get_novels_by_author(author)
    if len(novels) >= 2:
        plot_evolution(author, novels, metrics)

print('\nDone!')
