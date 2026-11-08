# DT Learun Playbook

广州力软旧框架的团队开发手册、审查交接与架构演进记录。团队仓库名：`dt-learun-playbook`。

本仓库只保存文档、源码定位证据和文档生成工具；业务源码仍在每个人自己的广州平台仓库中。

## 从哪里开始

- [当前交接与下一步](docs/handoff/2026-11-08.md)
- [决策依据与待验证假设](docs/decisions/0001-workflow-baseline.md)
- [架构改进推进表](docs/architecture/roadmap.md)
- [Agent 开发工作流](力软开发模式工作流-2026-11-08/AGENT_力软开发工作流.md)
- [IT HTML 手册](力软开发模式工作流-2026-11-08/IT_力软开发模式工作流.html)（下载后用浏览器打开）
- [第一轮框架审查 HTML](广州平台审查-2026-11-08/广州平台框架审查与AI开发基线.html)

文档中的旧路径和日期属于首次审查快照，不代表同事必须使用相同盘符。证据清单的 `path` 是相对于广州源码根目录的路径。

## 同事首次使用

需要 Git、Python 3 和一份合法取得的广州源码。本仓库不包含业务源码、数据库或 ponytail 技能安装包。

```powershell
git clone https://github.com/trevortsui007-explorer/dt-learun-playbook.git dt-learun-playbook
cd dt-learun-playbook
Copy-Item config/local.example.json config/local.json
```

把 `config/local.json` 中的 `guangzhou_source_root` 改成自己的广州源码路径。JSON 路径使用 `/`，例如 `E:/work/com.delton.serve-release`。该文件已被 Git 忽略，不会影响同事。

```powershell
python scripts/check_evidence.py
```

检查返回差异说明本地代码与审查快照不同，应重新追踪对应调用链；不得只更新哈希掩盖差异。阅读文档不要求安装 Python，也不要求本地有源码。

给 Agent 的任务示例：

> 先读取本仓库 AGENTS.md、config/local.json、docs/handoff/2026-11-08.md 和 Agent 工作流。根据本机广州源码重新核对目标模块的证据；本次完成……，报告修改、验证及未验证项。业务代码遵循业务仓库的 AGENTS.md。

## 团队如何继续完善

1. 在本仓库建立 `docs/<主题>` 分支，例如 `docs/si-contracts`；业务改动在业务仓库单独建分支。
2. 修改手册正文 `workflow_guide_source.md`，记录接口、过程签名、flag、参数、返回结构与权限来源。不要提交凭据或真实业务数据。
3. 新决策参考 [决策模板](docs/templates/decision.md)；结束一次任务参考 [交接模板](docs/templates/handoff.md)。保存结论、选择依据和验收证据，不复制聊天流水账。
4. 正文更新后运行 `python build_workflow_guide.py`。它使用个人配置读取源码，更新当前两份工作流文档与证据。阅读源文件采用 UTF-8 或 GB18030，只有标准库依赖。
5. 检查 `git diff`。如果源码版本已变化，新的报告应建立新的日期快照并更新生成脚本的 OUT/日期，避免无意覆盖历史。第一轮报告生成器 `build_guangzhou_audit.py` 保留用于追溯，不必每次运行。
6. 运行证据检查；业务变更另行构建、测试和 review。提交文档 PR，注明关联业务提交、验证结果、兼容影响和回退方法。

## 远程共享

远程仓库：[dt-learun-playbook](https://github.com/trevortsui007-explorer/dt-learun-playbook)。维护者首次连接远程并推送使用下列命令；普通同事使用上面的 clone 命令即可：

```powershell
git remote add origin https://github.com/trevortsui007-explorer/dt-learun-playbook.git
git push -u origin main
```

也可先把 `dist/dt-learun-playbook.bundle` 发给同事：`git clone <bundle文件路径> dt-learun-playbook`。bundle 仅包含已提交历史；后续持续协作仍应连接统一远程仓库。更新 bundle 使用 `git bundle create dist/dt-learun-playbook.bundle main`。

静态审查不能替代线上数据库、权限、IIS 配置、性能或业务验收。东莞平台尚未对照。
