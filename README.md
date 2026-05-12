# novel-corpus-analysis

网文叙事深度分析 · 小说语料库研究项目

## 当前规模

| 项目 | 数量 |
|------|------|
| 小说原文 | **473 本**（`novel-txts/*.txt`，master 分支） |
| 指纹表 | **362 本**（`reference/fingerprint-table-v4.4.md`） |
| 分析报告 | **983 份**（`analysis-*.md`） |
| 深度分析（>10KB） | **50 份** |
| 深度分析（>20KB） | **15 份** |
| 作者进化线 | **20+ 条** |
| 协议版本 | **v5.0**（`docs/human-protocol-v5.0.md`） |

## 目录结构

```
novel-corpus-analysis/
├── analysis-*.md              # 983份深度分析报告（纯分析）
├── scripts/                   # 31个分析脚本
│   ├── analyze*.py            #   标点分析/深度提取
│   ├── extract*.py            #   感官/福利/句式提取
│   ├── download*.py           #   小说下载
│   ├── visualize*.py          #   可视化
│   └── generate-docx*.js      #   DOCX生成
├── docs/                      # 31个项目文档
│   ├── HANDOFF-*.md           #   交接文件
│   ├── NARRATIVE-STATUS-*.md  #   叙事分析状态总览
│   ├── human-protocol-v5.0.md #   人味注入协议 v5.0
│   ├── 感官库-v2.0.md         #   感官库
│   └── 福利感官库-v2.0.md     #   福利感官库
├── reference/                 # 25个参考数据
│   ├── fingerprint-table-v4.*.md    # 指纹表
│   ├── human-flavor-protocol-v3~4.*.md  # 人味协议历史版本
│   ├── sensory-extraction-*.md      # 各题材感官提取
│   └── 感官库*.md / 福利*.md        # 感官/福利参考
└── data-tables/               # 数据表格
    └── §12.5-151novels-table.md
```

## 深度分析覆盖

### 作者进化线（已全量重做）
- **皇甫奇**（6本）：飞升之后/大周皇族/人皇纪/帝御山河/神座/无上真魔
- **zhttty**（6本）：无限恐怖/无限曙光/无限未来/大宇宙时代/死亡开端/魔法世纪
- **唐家三少**（11本）：斗罗系列/神印王座/天珠变/琴帝/狂神等
- **风凌天下**（7本）：傲世九重天/异世邪君/天域苍穹等
- **滚开**（8本）：十方武圣/隐秘死角/极道天魔等
- **文抄公**（10本）：苟在妖武/神秀之主/香火成神道等
- 天蚕土豆/辰东/耳根/血红/梦入神机/烽火戏诸侯/猫腻 等

### 单本深度分析（>15KB）
- 斗破苍穹（31KB）· 仙侠双壁-遮天仙逆对比（28KB）· 道诡异仙（23KB）
- 全职高手（22KB）· 惊悚乐园（21KB）· 邪龙道三部曲（21KB）
- 唐砖（20KB）· 冒牌大英雄（16KB）· 苟在妖武（15KB）等

### 品类分析
- 游戏文/体育文/霍格沃茨系列/小样本作者

## 分支说明

| 分支 | 内容 | 本地路径 |
|------|------|---------|
| **master** | 小说原文（473本txt）+ 分析报告 + 指纹表 | `public-transfer-master-git/` |
| **main** | 分析报告 + 脚本 + 协议（无txt） | `public-transfer-main-git/` |

## 操作规范

### 推送铁律
1. **永远不要 `git push --force`**
2. **只推送新增/修改的文件**，不要 `git add -A`
3. **推送前先 pull**：`git pull origin master --rebase`
4. **推送前 `git status` 确认**

### SSH 推送命令
```bash
GIT_SSH_COMMAND="ssh -i ~/.ssh/.github_miclaw -o StrictHostKeyChecking=no -o ConnectTimeout=60 -o ServerAliveInterval=30" git push origin <branch>
```

### SSH 密钥
- 路径：`~/.ssh/.github_miclaw`
- Git config：`bot@openclaw.ai` / `OpenClaw Bot`

## 教训记录

1. **永远不要把整个 workspace 文件夹推到 git** — 只推送项目文件
2. **workspace 文件不入仓库** — AGENTS.md、SOUL.md 等是本地工作文件
3. **新 session 先 pull 再操作** — 确认远程最新状态
4. **SSH push 大仓库容易超时** — 设置 `ConnectTimeout=60 + ServerAliveInterval=30`
5. **GBK 编码小说需 iconv 转 UTF-8** — 部分小说原文是 GBK 编码，统计前需转换

---

_Last updated: 2026-05-12 19:30 GMT+8_
