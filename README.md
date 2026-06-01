# 新道蓝谷.skill

> 金帝·新道蓝谷生命科学园 / 团队 / 个人 的项目、工具、技能合集

新道蓝谷不只是一个园区，也是我们这群人的代号。这里放跟新道蓝谷相关的所有项目，每个项目独立发展。

---

## 我们在做什么

围绕"新道蓝谷"这个 IP，我们有：

- **园区招商** — 跟企业打交道（入驻、租赁、政策、合规）
- **内部工具** — 让团队 / 园区办公更高效
- **个人 / 团队知识管理** — 不让经验流失
- **Skill 化** — 把日常工作流做成 AI 可执行的 Skill

具体项目见 [`projects/`](projects/)。

---

## 项目列表

| 项目 | 说明 | 状态 |
|------|------|------|
| [**xiaoyuan-vault**](projects/xiaoyuan-vault/) | 免费的本地知识库（开源版）<br/>支持 Markdown / 知识图谱 / 搜索 / 多 vault / Skill.md 插件 | ✅ v1.3.0-free |
| [**skill-x-valley**](projects/skill-x-valley/) | 金帝·新道蓝谷生命科学园招商助手<br/>园区入驻、政策、环评合规智能问答 | ✅ v1.0 |

## 项目添加流程

我们鼓励所有新道蓝谷相关的项目都聚合到这里。

**要求**：
- 独立仓库（不与合集混编）
- MIT 兼容 License
- 至少 1 个明确维护者
- 有 README 和入门指南

**步骤**：
1. 在 GitHub 上创建新仓库
2. 在本合集里加 submodule：
   ```bash
   git submodule add <repo-url> projects/<name>
   ```
3. 在本 README 表格里加一行
4. 提交 push

详见 [`docs/PROJECTS.md`](docs/PROJECTS.md)。

---

## 如何使用这个合集

### 完整克隆（含子项目）

```bash
git clone --recurse-submodules https://github.com/wj89093/X-valley.skill.git
```

如果忘了 `--recurse-submodules`：

```bash
cd X-valley.skill
git submodule update --init --recursive
```

### 同步所有子项目到最新

```bash
git submodule update --remote
```

### 只更新某个子项目

```bash
git submodule update --remote projects/xiaoyuan-vault
```

---

## 维护

- 顶层仓库**只做导航 + 索引**，不直接修改子项目代码
- 子项目各自独立发展，PR 提交到对应仓库
- 添加 / 移除项目请开 Issue 讨论

---

## License

MIT © 新道蓝谷团队

各子项目 License 见各自仓库。
