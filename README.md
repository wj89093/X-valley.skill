# 新道蓝谷.skill — 项目合集

> 个人 / 团队 / 园区的项目 + 工具 + 技能 聚合仓库

这里放新道蓝谷相关的所有项目和工具，按"项目（projects/）"组织，每个项目独立发展。

---

## 项目列表

| 项目 | 说明 | 状态 | 链接 |
|------|------|------|------|
| **xiaoyuan-vault** | 免费的本地知识库（开源版）<br/>支持 Markdown / 知识图谱 / 搜索 / 多 vault / Skill.md 插件 | ✅ v1.3.0-free | [查看](projects/xiaoyuan-vault/) |
| **skill-x-valley** | 金帝·新道蓝谷生命科学园招商助手<br/>解答园区入驻、政策、环评合规等问题 | ✅ v1.0 | [查看](projects/skill-x-valley/) |
| ... | (后续项目按需添加) | 📋 | - |

---

## 目录结构

```
.
├── projects/                ← 子项目目录
│   ├── xiaoyuan-vault/      ← git submodule 指向 wj89093/xiaoyuan-vault
│   └── skill-x-valley/      ← 当前 Skill 内容（SKILL.md + 数据）
├── docs/                    ← 顶层文档
└── README.md
```

---

## 快速开始

### 克隆整个合集（含所有子项目）

```bash
git clone --recurse-submodules https://github.com/wj89093/X-valley.skill.git
```

如果忘了 `--recurse-submodules`，补救：

```bash
cd X-valley.skill
git submodule update --init --recursive
```

### 只克隆顶层（不含子项目）

```bash
git clone https://github.com/wj89093/X-valley.skill.git
# 子项目目录会是空的
```

### 同步子项目到最新

```bash
git submodule update --remote
```

---

## 添加新项目

```bash
# 1. 在 GitHub 上创建新仓库
# 2. 加为 submodule
git submodule add https://github.com/wj89093/new-project.git projects/new-project
# 3. 提交
git add . && git commit -m "feat: add new-project submodule"
git push
```

---

## 贡献

- 顶层仓库**只做导航 + 索引**，不直接修改子项目代码
- 子项目各自独立发展，PR 提交到对应仓库
- 添加新项目请开 Issue 讨论

---

## License

MIT © 新道蓝谷团队

各子项目 License 见各自仓库。
