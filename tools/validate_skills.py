# -*- coding: utf-8 -*-
"""
校验 skill 合集的完整性。

用法：
    python validate_skills.py [合集根目录]

默认检查当前目录下的 skills/ 子目录。

检查项：
    1. 每个 skill 目录都有 SKILL.md
    2. frontmatter 能被 YAML 正确解析（能抓出块标量改写事故）
    3. name 字段与目录名一致
    4. description 非空且含触发词
    5. 正文长度合理、含 H1 标题
"""
import os, re, sys

try:
    import yaml
except ImportError:
    print("需要 pyyaml：pip install pyyaml")
    sys.exit(2)

ROOT = sys.argv[1] if len(sys.argv) > 1 else "skills"
FM = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.S)

ok, bad = [], []
if not os.path.isdir(ROOT):
    print("目录不存在：%s" % ROOT)
    sys.exit(2)

for name in sorted(os.listdir(ROOT)):
    d = os.path.join(ROOT, name)
    if not os.path.isdir(d):
        continue
    f = os.path.join(d, "SKILL.md")
    if not os.path.isfile(f):
        bad.append((name, "缺 SKILL.md"))
        continue
    with open(f, encoding="utf-8") as fh:
        t = fh.read()
    m = FM.match(t)
    if not m:
        bad.append((name, "frontmatter 未闭合或缺失"))
        continue
    try:
        data = yaml.safe_load(m.group(1))
    except Exception as e:
        bad.append((name, "YAML 解析失败: %s" % str(e).splitlines()[0]))
        continue
    if not isinstance(data, dict):
        bad.append((name, "frontmatter 不是映射"))
        continue
    if data.get("name") != name:
        bad.append((name, "name 字段(%r) 与目录名不符" % data.get("name")))
        continue
    desc = str(data.get("description") or "")
    if not desc.strip():
        bad.append((name, "description 为空"))
        continue
    if "触发词" not in desc:
        bad.append((name, "description 未含触发词"))
        continue
    body = t[m.end():]
    if len(body.strip()) < 200:
        bad.append((name, "正文过短（%d 字符），可能被截断" % len(body.strip())))
        continue
    if "# " not in body:
        bad.append((name, "正文缺 H1 标题"))
        continue
    ok.append(name)

print("通过: %d 个" % len(ok))
if bad:
    print("异常: %d 个" % len(bad))
    for n, why in bad:
        print("  ! %s -> %s" % (n, why))
    sys.exit(1)
print("全部校验通过")
