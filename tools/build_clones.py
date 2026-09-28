# -*- coding: utf-8 -*-
"""
克隆开源许可(Apache-2.0 / MIT)的 skill，并做本地化微调：
  1. 复制整个 skill 目录（保留脚本、参考文件、LICENSE）
  2. 改写 frontmatter 的 name 为本地命名
  3. 在 description 末尾追加中文触发词，提升中文场景命中率
  4. 在正文标题后插入「中文导读」区块（一句话 / 何时触发 / 来源与改动声明）
"""
import os, re, shutil, sys

SRC = os.path.dirname(os.path.abspath(__file__))
ANTH = os.path.join(SRC, "anth", "skills")
SP = os.path.join(SRC, "sp", "skills")
OUT = sys.argv[1]

# (源目录, 目标名, 来源仓库, 来源路径, 许可, 一句话, 何时触发, 中文触发词)
M = [
    # ---- anthropics/skills (Apache-2.0) ----
    ("skill-creator", "meta-skill-creator", "anthropics/skills", "skills/skill-creator", "Apache-2.0",
     "从零创建、迭代改进、跑评测优化一个 skill——造 skill 的 skill。",
     "想新建 skill、改已有 skill、给 skill 跑评测、优化 description 的触发准确率。",
     "造 skill、新建技能、写 SKILL.md、评测技能、优化触发"),
    ("frontend-design", "design-frontend", "anthropics/skills", "skills/frontend-design", "Apache-2.0",
     "做 UI 时给出有辨识度的视觉方向，避开一眼模板化的默认审美。",
     "新建界面、重做现有 UI、需要排版 / 配色 / 字体的方向性决策。",
     "前端设计、UI 设计、界面美化、配色、字体、视觉方向"),
    ("canvas-design", "design-canvas", "anthropics/skills", "skills/canvas-design", "Apache-2.0",
     "用代码渲染海报级平面设计作品（版面、层级、留白）。",
     "做海报、封面、宣传图、版面设计。",
     "海报、封面、宣传图、版面设计、平面设计"),
    ("theme-factory", "design-theme-factory", "anthropics/skills", "skills/theme-factory", "Apache-2.0",
     "成批生成彼此协调的配色与字体主题，保证多页面观感统一。",
     "需要一套统一主题、给多个页面 / 幻灯片配色。",
     "主题、配色方案、色板、多页统一风格"),
    ("brand-guidelines", "design-brand-guidelines", "anthropics/skills", "skills/brand-guidelines", "Apache-2.0",
     "把品牌规范（色彩、字体、语气）落进具体产出物。",
     "产出物需要符合某个品牌 / 机构规范。",
     "品牌规范、VI、机构模板、规范落地"),
    ("algorithmic-art", "design-algorithmic-art", "anthropics/skills", "skills/algorithmic-art", "Apache-2.0",
     "生成式艺术：用算法与参数化方式做视觉作品。",
     "生成艺术、参数化图形、创意编码。",
     "生成艺术、参数化、创意编码、算法艺术"),
    ("webapp-testing", "dev-webapp-testing", "anthropics/skills", "skills/webapp-testing", "Apache-2.0",
     "用浏览器自动化测 Web 应用：点击、填表、截图、断言。",
     "测网页、跑端到端流程、抓截图、复现前端 bug。",
     "网页测试、端到端测试、浏览器自动化、截图、复现 bug"),
    ("web-artifacts-builder", "dev-web-artifacts-builder", "anthropics/skills", "skills/web-artifacts-builder", "Apache-2.0",
     "把网页做成可交互的单文件产物，便于分享与嵌入。",
     "做可交互 HTML 小应用、演示件、单文件网页工具。",
     "可交互网页、单文件 HTML、artifact、小工具"),
    ("mcp-builder", "dev-mcp-builder", "anthropics/skills", "skills/mcp-builder", "Apache-2.0",
     "从零写一个 MCP server，把自己的工具或数据源暴露给 agent。",
     "接 MCP、暴露自建工具、写 connector、配置 mcp.json。",
     "MCP、mcp server、连接器、connector、工具接入"),
    ("claude-api", "dev-claude-api", "anthropics/skills", "skills/claude-api", "Apache-2.0",
     "Anthropic API 用法速查：模型选择、tool use、提示缓存、流式。",
     "调 Claude API、选模型、写 tool use、做缓存与流式。",
     "Claude API、Anthropic API、tool use、提示缓存、流式输出"),
    ("internal-comms", "writing-internal-comms", "anthropics/skills", "skills/internal-comms", "Apache-2.0",
     "写内部沟通件：周报、公告、复盘、状态同步。",
     "写周报 / 月报、团队公告、项目状态更新、复盘。",
     "周报、月报、公告、状态同步、复盘、内部沟通"),
    ("academy-guide", "writing-academy-guide", "anthropics/skills", "skills/academy-guide", "Apache-2.0",
     "教学与课程材料的结构化写法。",
     "写教程、课程、教学大纲、讲解材料。",
     "教程、课程、教学大纲、讲解、培训材料"),
    ("discernment-nudge", "thinking-discernment", "anthropics/skills", "skills/discernment-nudge", "Apache-2.0",
     "在信息不足或提问带预设时，先辨别再回答，不顺着错误前提走。",
     "问题含未验证的预设、信息不全、需要判断可信度。",
     "辨别、质疑前提、信息不足、可信度、反问"),
    ("slack-gif-creator", "design-slack-gif", "anthropics/skills", "skills/slack-gif-creator", "Apache-2.0",
     "制作聊天场景用的 GIF 动图。",
     "做 GIF、表情动图、聊天贴图。",
     "GIF、动图、表情包"),
    # ---- obra/superpowers (MIT) ----
    ("using-superpowers", "meta-using-skills", "obra/superpowers", "skills/using-superpowers", "MIT",
     "skill 体系的入口：先判断该调哪个 skill，再动手。",
     "会话开始、任务类型不明、不确定该用哪个 skill。",
     "该用哪个 skill、技能路由、入口、方法论总纲"),
    ("writing-skills", "meta-writing-skills", "obra/superpowers", "skills/writing-skills", "MIT",
     "把可复用的工作流沉淀成 skill（结构、触发词、组织方式）。",
     "把流程写成 skill、重构已有 skill。",
     "写 skill、沉淀流程、技能结构、触发词设计"),
    ("brainstorming", "dev-brainstorming", "obra/superpowers", "skills/brainstorming", "MIT",
     "动手前先把意图、需求、设计聊透，避免做错方向。",
     "要开新功能 / 新组件、需求还模糊、方案未定。",
     "头脑风暴、需求梳理、方案讨论、动手前对齐"),
    ("writing-plans", "dev-writing-plans", "obra/superpowers", "skills/writing-plans", "MIT",
     "把设计落成可执行、可验证的分步计划。",
     "设计已定、要拆步骤、要写实施计划。",
     "写计划、拆任务、实施步骤、方案拆解"),
    ("executing-plans", "dev-executing-plans", "obra/superpowers", "skills/executing-plans", "MIT",
     "按计划一步步执行，每步落地后逐项验证。",
     "已有计划要落地执行。",
     "执行计划、按步骤实施、逐步落地"),
    ("systematic-debugging", "dev-systematic-debugging", "obra/superpowers", "skills/systematic-debugging", "MIT",
     "系统化排障：先稳定复现，再定位根因，最后才改。",
     "有 bug、行为不符预期、报错排查、性能异常。",
     "调试、排障、bug、复现、根因分析、报错"),
    ("test-driven-development", "dev-tdd", "obra/superpowers", "skills/test-driven-development", "MIT",
     "红-绿-重构：先写失败的测试，再写实现。",
     "写新功能 / 修 bug 并希望用 TDD 推进。",
     "TDD、测试驱动、单元测试、红绿重构"),
    ("verification-before-completion", "dev-verification", "obra/superpowers", "skills/verification-before-completion", "MIT",
     "在声称「做完了」之前，必须先拿出验证证据。",
     "准备宣布完成、提交前自检、交付前确认。",
     "验证、自检、完成前检查、交付确认"),
    ("requesting-code-review", "dev-requesting-review", "obra/superpowers", "skills/requesting-code-review", "MIT",
     "发起代码评审，把上下文和关注点交代清楚。",
     "要请人 review、开 PR、请求评审。",
     "代码评审、review、PR、请人看代码"),
    ("receiving-code-review", "dev-receiving-review", "obra/superpowers", "skills/receiving-code-review", "MIT",
     "接到评审意见后怎么处理才不跑偏、不盲从。",
     "收到 review 意见、要按意见改代码。",
     "处理评审意见、改 review、代码修改"),
    ("subagent-driven-development", "dev-subagent-driven", "obra/superpowers", "skills/subagent-driven-development", "MIT",
     "用子代理驱动开发，主代理只做编排与验收。",
     "任务可拆分派给子代理、需要并行推进。",
     "子代理、subagent、任务编排、并行开发"),
    ("dispatching-parallel-agents", "dev-dispatching-parallel", "obra/superpowers", "skills/dispatching-parallel-agents", "MIT",
     "把互不依赖的任务并行派发给多个代理，省墙钟时间。",
     "多个彼此独立的调研 / 改造任务可同时跑。",
     "并行代理、并行任务、同时调研"),
    ("using-git-worktrees", "dev-git-worktrees", "obra/superpowers", "skills/using-git-worktrees", "MIT",
     "用 git worktree 隔离并行分支，不污染当前工作区。",
     "要并行开多条分支、需要干净的工作区。",
     "git worktree、并行分支、工作区隔离"),
    ("finishing-a-development-branch", "dev-finishing-branch", "obra/superpowers", "skills/finishing-a-development-branch", "MIT",
     "开发分支收尾：自检、清理、合并、删分支。",
     "分支开发完成，要收口合并。",
     "分支收尾、合并、清理分支、开发完成"),
    ("diagnosing-superpowers", "dev-diagnosing", "obra/superpowers", "skills/diagnosing-superpowers", "MIT",
     "排查 skill 体系自身的问题：没触发、行为异常、体系混乱。",
     "skill 不生效、触发错误、技能体系需要体检。",
     "skill 不生效、排查技能、体系体检"),
]


def split_fm(text):
    """返回 (frontmatter_str, body_str)。没有 frontmatter 则 fm 为 None。"""
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def set_fm_field(fm, key, value):
    """在 frontmatter 文本里替换或追加一个字段。value 会被安全地加引号。"""
    esc = value.replace('"', "'")
    line = '%s: "%s"' % (key, esc)
    pat = re.compile(r"^%s:.*$" % re.escape(key), re.M)
    if pat.search(fm):
        return pat.sub(lambda _: line, fm, count=1)
    return fm.rstrip("\n") + "\n" + line


def get_fm_field(fm, key):
    m = re.search(r"^%s:\s*(.*)$" % re.escape(key), fm, re.M)
    if not m:
        return ""
    v = m.group(1).strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v


def build():
    ok, fail = [], []
    for src_name, dst_name, repo, path, lic, oneliner, when, triggers in M:
        base = ANTH if repo.startswith("anthropics") else SP
        src = os.path.join(base, src_name)
        dst = os.path.join(OUT, dst_name)
        if not os.path.isdir(src):
            fail.append((dst_name, "源目录不存在: " + src))
            continue
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

        md = os.path.join(dst, "SKILL.md")
        if not os.path.isfile(md):
            fail.append((dst_name, "缺少 SKILL.md"))
            continue
        with open(md, "r", encoding="utf-8") as f:
            text = f.read()

        fm, body = split_fm(text)
        if fm is None:
            fail.append((dst_name, "无 frontmatter"))
            continue

        old_desc = get_fm_field(fm, "description")
        new_desc = (old_desc + " 中文触发词：" + triggers + "。").strip() if old_desc else triggers
        fm = set_fm_field(fm, "name", dst_name)
        fm = set_fm_field(fm, "description", new_desc)

        # 中文导读区块
        guide = (
            "\n> **📖 中文导读**（本地化补充，原版正文未改动）\n>\n"
            "> - **一句话**：%s\n"
            "> - **何时触发**：%s\n"
            "> - **来源**：`%s` → `%s`，许可 **%s**，已克隆并加注本导读。\n"
            "\n---\n" % (oneliner, when, repo, path, lic)
        )

        # 插到第一个 H1 之后；没有 H1 就放正文最前
        m = re.search(r"^#\s+.*$", body, re.M)
        if m:
            body = body[:m.end()] + "\n" + guide + body[m.end():]
        else:
            body = guide + body

        with open(md, "w", encoding="utf-8") as f:
            f.write("---\n" + fm.strip("\n") + "\n---\n" + body)

        # MIT 要求再分发时保留版权声明与许可文本。
        # obra/superpowers 的 LICENSE 在仓库根目录，不在单个 skill 目录里，
        # 必须显式复制进来，否则单独拷一个 skill 出去就违反 MIT。
        if not repo.startswith("anthropics"):
            root_lic = os.path.join(base, os.pardir, "LICENSE")
            if os.path.isfile(root_lic):
                shutil.copyfile(root_lic, os.path.join(dst, "LICENSE.txt"))
            else:
                fail.append((dst_name, "找不到仓库根 LICENSE，无法满足 MIT 署名要求"))

        ok.append(dst_name)

    print("克隆成功 %d 个：" % len(ok))
    for n in ok:
        print("  +", n)
    if fail:
        print("失败 %d 个：" % len(fail))
        for n, why in fail:
            print("  !", n, why)


if __name__ == "__main__":
    build()
