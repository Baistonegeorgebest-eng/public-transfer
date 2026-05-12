const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, ImageRun, HeadingLevel, 
        AlignmentType, PageBreak, BorderStyle, WidthType, Table, TableRow, TableCell,
        ShadingType, Header, Footer, PageNumber } = require('docx');

const CHARTS = '/root/.openclaw/workspace/novel-corpus-analysis/charts';
const OUT = '/root/.openclaw/workspace/novel-corpus-analysis/人味协议-可视化报告.docx';

// Helper: create image paragraph
function imgPara(filename, width = 500, height = 350) {
    const data = fs.readFileSync(path.join(CHARTS, filename));
    return new Paragraph({
        children: [new ImageRun({
            type: 'png',
            data: data,
            transformation: { width, height },
            altText: { title: filename, description: filename, name: filename }
        })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 }
    });
}

// Helper: heading
function h1(text) {
    return new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun({ text, bold: true, font: 'Arial', size: 32 })],
        spacing: { before: 360, after: 200 }
    });
}

function h2(text) {
    return new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun({ text, bold: true, font: 'Arial', size: 28 })],
        spacing: { before: 240, after: 160 }
    });
}

function p(text, opts = {}) {
    return new Paragraph({
        children: [new TextRun({ text, font: 'Arial', size: 22, ...opts })],
        spacing: { after: 120 }
    });
}

// Build document
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
        headers: {
            default: new Header({
                children: [new Paragraph({
                    children: [new TextRun({ text: 'Human Flavor Protocol v3.9 — Visualization Report', font: 'Arial', size: 18, color: '888888' })],
                    alignment: AlignmentType.RIGHT
                })]
            })
        },
        footers: {
            default: new Footer({
                children: [new Paragraph({
                    children: [new TextRun({ text: 'Page ', font: 'Arial', size: 18 }), new TextRun({ children: [PageNumber.CURRENT], font: 'Arial', size: 18 })],
                    alignment: AlignmentType.CENTER
                })]
            })
        },
        children: [
            // Title page
            new Paragraph({ spacing: { before: 3000 } }),
            new Paragraph({
                children: [new TextRun({ text: 'Human Flavor Protocol', font: 'Arial', size: 56, bold: true })],
                alignment: AlignmentType.CENTER
            }),
            new Paragraph({
                children: [new TextRun({ text: 'Visualization Report', font: 'Arial', size: 40, color: '666666' })],
                alignment: AlignmentType.CENTER
            }),
            new Paragraph({ spacing: { before: 600 } }),
            new Paragraph({
                children: [new TextRun({ text: '286 Novels · 194 Analysis Reports · 32 Deep Analyses', font: 'Arial', size: 24, color: '888888' })],
                alignment: AlignmentType.CENTER
            }),
            new Paragraph({
                children: [new TextRun({ text: 'Generated: 2026-04-22', font: 'Arial', size: 24, color: '888888' })],
                alignment: AlignmentType.CENTER
            }),
            new Paragraph({ children: [new PageBreak()] }),

            // Section 1: Full Library Distribution
            h1('1. Full Library Distribution (286 Novels)'),
            p('Distribution of 6 key metrics across all 286 novels. Median lines indicate central tendency.'),
            imgPara('distributions.png', 580, 320),

            new Paragraph({ children: [new PageBreak()] }),

            // Section 2: Heatmap
            h1('2. Fingerprint Heatmap (Top 100 Novels)'),
            p('Row-normalized heatmap showing relative patterns across 9 metrics for the top 100 novels by word count.'),
            imgPara('heatmap-top100.png', 600, 280),

            new Paragraph({ children: [new PageBreak()] }),

            // Section 3: Evolution Curves
            h1('3. Author Evolution Curves'),
            p('Each author\'s career trajectory tracked through 4 punctuation metrics: Exclamation, Period, Comma, and Ellipsis density (per 1000 characters).'),

            h2('3.1 Yuantong (4 novels)'),
            imgPara('evolution-远瞳.png', 550, 380),

            new Paragraph({ children: [new PageBreak()] }),

            h2('3.2 Hui Shuo Hua De Zhouzi (3 novels)'),
            imgPara('evolution-会说话的肘子.png', 550, 380),

            new Paragraph({ children: [new PageBreak()] }),

            h2('3.3 Huangfuqi (6 novels)'),
            imgPara('evolution-皇甫奇.png', 550, 380),

            new Paragraph({ children: [new PageBreak()] }),

            h2('3.4 Meng Ru Shen Ji (7 novels)'),
            imgPara('evolution-梦入神机.png', 550, 380),

            new Paragraph({ children: [new PageBreak()] }),

            h2('3.5 Tian Can Tu Dou (5 novels)'),
            imgPara('evolution-天蚕土豆.png', 550, 380),

            new Paragraph({ children: [new PageBreak()] }),

            h2('3.6 Mao Ni (6 novels)'),
            imgPara('evolution-猫腻.png', 550, 380),

            new Paragraph({ children: [new PageBreak()] }),

            h2('3.7 Xue Hong (7 novels)'),
            imgPara('evolution-血红.png', 550, 380),

            new Paragraph({ children: [new PageBreak()] }),

            h2('3.8 Feng Huo Xi Zhu Hou (3 novels)'),
            imgPara('evolution-烽火戏诸侯.png', 550, 380),

            new Paragraph({ children: [new PageBreak()] }),

            h2('3.9 Er Gen (5 novels)'),
            imgPara('evolution-耳根.png', 550, 380),

            new Paragraph({ children: [new PageBreak()] }),

            // Section 4: Key Findings
            h1('4. Key Findings'),
            
            p('Seriousness Distribution (286 novels):', { bold: true }),
            p('  - Extreme Hot-blooded (ek>=10): 20 novels (7%)'),
            p('  - Hot-blooded (ek 6-10): 59 novels (21%)'),
            p('  - Medium (ek 3-6): 99 novels (35%)'),
            p('  - Cold Pen (ek 1.5-3): 56 novels (20%)'),
            p('  - Extreme Cold (ek<1.5): 46 novels (16%)'),

            p('Breathing Pattern Distribution:', { bold: true }),
            p('  - Very Slow (pk<12): 23 novels (8%)'),
            p('  - Slow (pk 12-18): 69 novels (24%)'),
            p('  - Normal (pk 18-28): 128 novels (45%)'),
            p('  - Fast (pk 28-40): 52 novels (18%)'),
            p('  - Very Fast (pk>40): 8 novels (2%)'),

            p('Notable Evolution Patterns:', { bold: true }),
            p('  - Linear Convergence: Meng Ru Shen Ji (exclamation 10.49 -> 0.52, 95% decline)'),
            p('  - Exclamation Cliff: Zhouzi (10.62 -> 3.48, -67%)'),
            p('  - Breathing Transformation: Zhouzi period 13 -> 24 (near double)'),
            p('  - U-Curve: Mao Ni period 22 -> 16 -> 28'),
            p('  - Genre-Driven Oscillation: Huangfuqi period swings 149%'),
        ]
    }]
});

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(OUT, buffer);
    console.log('Done! Saved to', OUT);
    console.log('Size:', (buffer.length / 1024).toFixed(0), 'KB');
});
