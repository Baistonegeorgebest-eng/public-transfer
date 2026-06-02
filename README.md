# novel-corpus-analysis

网文叙事深度分析 · 小说语料库研究项目

## 当前规模

| 项目 | 数量 |
|------|------|
| 小说原文 | **474 本**（`novel-txts/`，按作者归类，207个作者目录） |
| 分析报告 | **999 份**（`analysis-*.md`） |
| ≥10KB 分析 | **237 份**（✅ 高质量） |
| ≥15KB 分析 | **60 份**（🔵 顶级） |
| ≥25KB 分析 | **23 份**（🏆 现象级） |
| 分析脚本 | **28 个**（`scripts/`） |
| 协议版本 | **v5.0**（`docs/human-protocol-v5.0.md`） |

## 四路全覆盖（2026-06-02 完成）

| 路 | 定义 | 总数 | ✅≥10KB | 🏆≥25KB | 覆盖率 |
|---|---|---|---|---|---|
| 路1 | 知名作者 | 194 | 194 | 25 | **100%** |
| 路2 | 品类经典 | 50 | 48 | 12 | **100%** |
| 路3 | 数据异常 | 15 | 15 | 0 | **100%** |
| 路4 | 译本 | 29 | 28 | 0 | **100%** |
| **合计** | | **288** | **285** | **37** | **100%** |

## 目录结构

```
novel-corpus-analysis/
├── analysis/                    # 999份分析报告
│   ├── analysis-*.md            #   常规分析（10KB+）
│   ├── analysis-*-deep.md       #   深度统计分析（3KB，标点/感官/句式）
│   └── analysis-*-进化*.md      #   作者进化线
├── scripts/                   # 28个分析脚本
│   ├── analyze*.py            #   标点分析/深度提取
│   ├── extract*.py            #   感官/福利/句式提取
│   ├── download*.py           #   小说下载
│   └── visualize*.py          #   可视化
├── docs/                      # 项目文档
│   ├── STATUS.md              #   ⭐ 唯一进度源
│   ├── HANDOFF.md             #   ⭐ 唯一交接文件
│   ├── human-protocol-v5.0.md #   人味注入协议 v5.0
│   ├── 翻译文学分析方法论-v1.0.md  # 路4译本分析方法论
│   ├── 感官库-v2.0.md         #   感官库
│   ├── 福利感官库-v2.0.md     #   福利感官库
│   └── archive/               #   旧文件归档
├── reference/                 # 参考数据
│   ├── fingerprint-table-v4.*.md    # 指纹表
│   └── human-flavor-protocol-v3~4.*.md  # 人味协议历史版本
└── data-tables/               # 数据表格
```

## 分支说明

| 分支 | 内容 | 本地路径 |
|------|------|---------|
| **master** | 小说原文（474本txt，按作者归类）+ 分析报告 + 指纹表 | `public-transfer-master-git/` |
| **main** | 分析报告 + 脚本 + 协议（无txt） | `public-transfer-main-git/` |

## 操作规范

### 推送铁律
1. **永远不要 `git push --force`**
2. **推送前先 pull**：`git pull origin main --rebase`
3. **推送前 `git status` 确认**

### SSH 推送命令
```bash
GIT_SSH_COMMAND="ssh -i ~/.ssh/.github_miclaw -o StrictHostKeyChecking=no -o ConnectTimeout=60 -o ServerAliveInterval=30" git push origin main
```

### 交接协议

**核心规则：只维护两个文件。**

| 文件 | 用途 | 更新时机 |
|------|------|---------|
| `docs/STATUS.md` | 覆盖率+作者完成表+待做队列 | 有新作者完成时 |
| `docs/HANDOFF.md` | 上次完成+下次任务+已知问题 | 每次session结束时 |

---

_Last updated: 2026-06-02 GMT+8_
