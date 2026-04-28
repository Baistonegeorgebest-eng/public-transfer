const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, ImageRun, HeadingLevel, 
        AlignmentType, PageBreak, Header, Footer, PageNumber } = require('docx');

const CHARTS = '/root/.openclaw/workspace/novel-corpus-analysis/charts';
const OUT = '/root/.openclaw/workspace/novel-corpus-analysis/人味协议-可视化报告.docx';

function img(filename, w = 520, h = 360) {
    const data = fs.readFileSync(path.join(CHARTS, filename));
    return new Paragraph({
        children: [new ImageRun({ type: 'png', data, transformation: { width: w, height: h },
            altText: { title: filename, description: filename, name: filename } })],
        alignment: AlignmentType.CENTER, spacing: { after: 160 }
    });
}

function h1(text) { return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text, bold: true, font: 'Arial', size: 32 })],
    spacing: { before: 360, after: 200 }
}); }

function h2(text) { return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text, bold: true, font: 'Arial', size: 28 })],
    spacing: { before: 240, after: 160 }
}); }

function p(text, opts = {}) { return new Paragraph({
    children: [new TextRun({ text, font: 'Arial', size: 22, ...opts })],
    spacing: { after: 120 }
}); }

function pb() { return new Paragraph({ children: [new PageBreak()] }); }

const doc = new Document({
    styles: {
        default: { document: { run: { font: 'Arial', size: 22 } } },
        paragraphStyles: [
            { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
              run: { size: 32, bold: true, font: 'Arial' },
              paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
            { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
              run: { size: 28, bold: true, font: 'Arial' },
              paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 } },
        ]
    },
    sections: [{
        properties: {
            page: {
                size: { width: 12240, height: 15840 },
                margin: { top: 1440, right: 1200, bottom: 1440, left: 1200 }
            }
        },
        headers: { default: new Header({ children: [new Paragraph({
            children: [new TextRun({ text: 'Human Flavor Protocol v4.0 — Visualization Report', font: 'Arial', size: 18, color: '888888' })],
            alignment: AlignmentType.RIGHT
        })] }) },
        footers: { default: new Footer({ children: [new Paragraph({
            children: [new TextRun({ text: 'Page ', font: 'Arial', size: 18 }), new TextRun({ children: [PageNumber.CURRENT], font: 'Arial', size: 18 })],
            alignment: AlignmentType.CENTER
        })] }) },
        children: [
            // ========== TITLE PAGE ==========
            new Paragraph({ spacing: { before: 3000 } }),
            new Paragraph({ children: [new TextRun({ text: 'Human Flavor Protocol', font: 'Arial', size: 56, bold: true })], alignment: AlignmentType.CENTER }),
            new Paragraph({ children: [new TextRun({ text: 'Full Visualization Report', font: 'Arial', size: 40, color: '666666' })], alignment: AlignmentType.CENTER }),
            new Paragraph({ spacing: { before: 600 } }),
            new Paragraph({ children: [new TextRun({ text: '286 Novels · 194 Analyses · 32 Deep Analyses · 9 Author Evolution Lines', font: 'Arial', size: 22, color: '888888' })], alignment: AlignmentType.CENTER }),
            new Paragraph({ children: [new TextRun({ text: 'v4.0 · 2026-04-22', font: 'Arial', size: 22, color: '888888' })], alignment: AlignmentType.CENTER }),
            pb(),

            // ========== PART 1: DISTRIBUTIONS ==========
            h1('Part 1: Full Library Distributions'),
            p('Histograms of 6 key metrics across all 286 novels. Dashed line = median.'),
            img('distributions.png', 600, 330),
            p('Key observations:', { bold: true }),
            p('  • Exclamation: heavily right-skewed, median ~4, long tail to 44 (射门)'),
            p('  • Period: bimodal distribution, peaks at ~15 and ~28'),
            p('  • Comma: near-normal, centered around 55-65'),
            p('  • Ellipsis: extreme right-skew, most novels < 3, outliers up to 14'),
            p('  • Avg sentence length: normal-ish, median ~35 chars'),
            p('  • Emotion density: right-skewed, median ~10'),
            pb(),

            // ========== PART 2: HEATMAP ==========
            h1('Part 2: Fingerprint Heatmap (Top 100)'),
            p('Row-normalized heatmap of 9 metrics across top 100 novels by word count.'),
            p('Brighter = higher relative value within that metric row.'),
            img('heatmap-top100.png', 620, 290),
            pb(),

            // ========== PART 3: INDIVIDUAL EVOLUTION ==========
            h1('Part 3: Individual Author Evolution Curves'),
            p('Each author tracked through 4 punctuation metrics across their career novels.'),

            h2('3.1 Yuantong (4 novels: Xiling -> YCBJWL -> LMZJ -> SHYJ)'),
            p('Comma extremely low (40-48, lowest in library). Period: drops then recovers. Exclamation: steady decline 2.2 -> 1.7. Ellipsis: rising trend 3.4 -> 4.7.'),
            img('evolution-远瞳.png', 560, 390),
            pb(),

            h2('3.2 Zhouzi (3 novels: LOL -> DWLM -> YDMS)'),
            p('Dramatic exclamation cliff: 10.62 -> 5.17 -> 3.48 (-67%). Period transformation: stable 13-14 then jumps to 23.8 (+68%).'),
            img('evolution-会说话的肘子.png', 560, 390),
            pb(),

            h2('3.3 Huangfuqi (6 novels)'),
            p('Exclamation stable 5.77-7.65. Period swings 149% (14.5-36.1) — genre-driven oscillation. Comma rising trend 50.5 -> 67.0.'),
            img('evolution-皇甫奇.png', 560, 390),
            pb(),

            h2('3.4 Mengru Shenji (7 novels)'),
            p('Most extreme linear convergence in library: exclamation 10.49 -> 0.52 (95% decline). Comma peak at 佛本是道 (84.6, #3 in library).'),
            img('evolution-梦入神机.png', 560, 390),
            pb(),

            h2('3.5 Tian Can Tu Dou (5 novels)'),
            p('Ellipsis collapse: 6+ -> ~0 (near-zero, most extreme in library). Period doubles: 12 -> 26.'),
            img('evolution-天蚕土豆.png', 560, 390),
            pb(),

            h2('3.6 Mao Ni (6 novels)'),
            p('U-curve pattern: period 22 -> 16 -> 28. Exclamation always below 1.6 (extreme cold). Comma stable.'),
            img('evolution-猫腻.png', 560, 390),
            pb(),

            h2('3.7 Xue Hong (7 novels)'),
            p('Turning point at 开天录. Comma diverges: 63 -> 47 -> 60. Exclamation variable by genre.'),
            img('evolution-血红.png', 560, 390),
            pb(),

            h2('3.8 Fenghuo Xizhu Hou (3 novels)'),
            p('Ultra-long sentences (68.1 avg in 陈二狗, highest original Chinese). Exclamation near-zero throughout.'),
            img('evolution-烽火戏诸侯.png', 560, 390),
            pb(),

            h2('3.9 Er Gen (5 novels)'),
            p('Period stable high (27-29 range). Comma varies. Consistent "serious" fingerprint across career.'),
            img('evolution-耳根.png', 560, 390),
            pb(),

            // ========== PART 4: AGGREGATED ==========
            h1('Part 4: Author Aggregated Comparisons'),
            p('All 9 main authors plotted on the same axes for direct comparison.'),

            h2('4.1 Exclamation Comparison'),
            p('Clear separation between "hot-blooded" authors (Zhouzi, Huangfuqi) and "cold" authors (Mao Ni, Fenghuo, Yuantong).'),
            img('aggregated-exclamation.png', 580, 380),
            pb(),

            h2('4.2 Period (Breathing) Comparison'),
            p('Huangfuqi shows widest period range. Mengru Shenji has lowest periods. Er Gen most stable.'),
            img('aggregated-period.png', 580, 380),
            pb(),

            h2('4.3 Comma Comparison'),
            p('Mengru Shenji highest (84.6 peak). Yuantong lowest (40-48 range). Most authors cluster 50-70.'),
            img('aggregated-comma.png', 580, 380),
            pb(),

            h2('4.4 Ellipsis Comparison'),
            p('Tian Can Tu Dou collapses to zero. Huangfuqi consistently low. Zhouzi moderate.'),
            img('aggregated-ellipsis.png', 580, 380),
            pb(),

            h2('4.5 Four-Metric Grid Overview'),
            p('Side-by-side view of all 4 metrics for quick pattern recognition.'),
            img('aggregated-4metrics-grid.png', 620, 490),
            pb(),

            h2('4.6 Additional Authors (3+ novels)'),
            p('Extended comparison including authors with 3+ novels in the library.'),
            img('aggregated-additional-authors.png', 620, 490),
            pb(),

            // ========== PART 5: KEY FINDINGS ==========
            h1('Part 5: Key Findings Summary'),
            
            h2('5.1 Seriousness Distribution (286 novels)'),
            p('  • Extreme Hot-blooded (ek>=10): 20 novels (7%)'),
            p('  • Hot-blooded (ek 6-10): 59 novels (21%)'),
            p('  • Medium (ek 3-6): 99 novels (35%)'),
            p('  • Cold Pen (ek 1.5-3): 56 novels (20%)'),
            p('  • Extreme Cold (ek<1.5): 46 novels (16%)'),
            p('  • Finding: bimodal — hot-blooded (28%) vs cold+extreme-cold (36%)'),

            h2('5.2 Breathing Pattern Distribution'),
            p('  • Very Slow (pk<12): 23 novels (8%)'),
            p('  • Slow (pk 12-18): 69 novels (24%)'),
            p('  • Normal (pk 18-28): 128 novels (45%)'),
            p('  • Fast (pk 28-40): 52 novels (18%)'),
            p('  • Very Fast (pk>40): 8 novels (2%)'),

            h2('5.3 Notable Evolution Patterns'),
            p('  • Linear Convergence: Mengru Shenji (ek 10.49->0.52, 95%)'),
            p('  • Exclamation Cliff: Zhouzi (10.62->3.48, -67%), Warehouse Author (8.33->2.25)'),
            p('  • Breathing Transformation: Zhouzi period 13->24 (near double)'),
            p('  • U-Curve: Mao Ni period 22->16->28'),
            p('  • Genre-Driven Oscillation: Huangfuqi period swings 149%'),
            p('  • Ellipsis Collapse: Tian Can Tu Dou (6+ -> ~0)'),
            p('  • Ultra-Constant: Wang Yu (period 27-29), Fang Xiang (stable core)'),

            h2('5.4 Library Records'),
            p('  • Highest exclamation: 射门 44.01/1000'),
            p('  • Highest comma: 我欲封天 94.7/1000'),
            p('  • Highest ellipsis: 惊悚乐园 14.44/1000'),
            p('  • Lowest exclamation: 点道为止 0.52/1000'),
            p('  • Longest avg sentence (original): 陈二狗 68.1 chars'),
            p('  • Longest avg paragraph: 宰执天下 109.5 chars'),
            p('  • Highest emotion density: 射门 48.2/1000'),
        ]
    }]
});

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(OUT, buffer);
    console.log('Done! Saved to', OUT);
    console.log('Size:', (buffer.length / 1024 / 1024).toFixed(1), 'MB');
});
