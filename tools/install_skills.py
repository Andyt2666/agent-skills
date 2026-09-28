# -*- coding: utf-8 -*-
"""
把本合集的 skill 挂载到（或从）WorkBuddy 的 skills 目录。

默认是 **dry-run**，只打印会做什么，不动任何文件。
必须显式给 --yes 才真正执行。

用法
----
    # 看看会挂哪些（不动文件）
    python install_skills.py --all

    # 只挂科研类
    python install_skills.py --only research-paper-reading,research-experiment-log --yes

    # 挂全部
    python install_skills.py --all --yes

    # 卸载（只删本合集装进去的，不动原有的）
    python install_skills.py --uninstall --all --yes

    # 指定目标目录
    python install_skills.py --all --dest "I:/some/skills" --yes
"""
import argparse
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, os.pardir, "skills")
SRC = os.path.normpath(SRC)

# 本机默认的 WorkBuddy 用户级 skills 目录（已 junction 到 I 盘）
DEFAULT_DEST = os.path.join(os.path.expanduser("~"), ".workbuddy-ai", "skills")

# 本合集自带的元数据文件，不算 skill
SKIP = {".DS_Store", "Thumbs.db", "desktop.ini"}


def list_skills():
    out = []
    for n in sorted(os.listdir(SRC)):
        d = os.path.join(SRC, n)
        if os.path.isdir(d) and os.path.isfile(os.path.join(d, "SKILL.md")):
            out.append(n)
    return out


def main():
    ap = argparse.ArgumentParser(description="挂载 / 卸载 skill 合集")
    ap.add_argument("--all", action="store_true", help="选中全部 skill")
    ap.add_argument("--only", default="", help="逗号分隔的 skill 名列表")
    ap.add_argument("--dest", default=DEFAULT_DEST, help="目标 skills 目录")
    ap.add_argument("--uninstall", action="store_true", help="卸载而不是安装")
    ap.add_argument("--force", action="store_true", help="覆盖已存在的同名 skill")
    ap.add_argument("--yes", action="store_true", help="真正执行（默认 dry-run）")
    a = ap.parse_args()

    avail = list_skills()
    if a.all:
        picked = avail
    elif a.only:
        picked = [s.strip() for s in a.only.split(",") if s.strip()]
        unknown = [s for s in picked if s not in avail]
        if unknown:
            print("未知 skill: %s" % ", ".join(unknown))
            print("可用: %s" % ", ".join(avail))
            sys.exit(1)
    else:
        print("请指定 --all 或 --only <名称列表>")
        print("可用 skill（%d 个）：" % len(avail))
        for s in avail:
            print("  ", s)
        sys.exit(0)

    dest = os.path.normpath(a.dest)
    mode = "卸载" if a.uninstall else "挂载"
    print("源目录  : %s" % SRC)
    print("目标目录: %s" % dest)
    print("模式    : %s%s" % (mode, "" if a.yes else "  【DRY-RUN，未执行】"))
    print("-" * 56)

    if not os.path.isdir(dest):
        print("目标目录不存在：%s" % dest)
        sys.exit(1)

    done, skipped, missing = [], [], []
    for name in picked:
        src_d = os.path.join(SRC, name)
        dst_d = os.path.join(dest, name)
        if a.uninstall:
            if not os.path.isdir(dst_d):
                missing.append(name)
                continue
            if a.yes:
                shutil.rmtree(dst_d)
            done.append(name)
        else:
            if os.path.exists(dst_d) and not a.force:
                skipped.append(name)
                continue
            if a.yes:
                if os.path.exists(dst_d):
                    shutil.rmtree(dst_d)
                shutil.copytree(src_d, dst_d, ignore=shutil.ignore_patterns(*SKIP))
            done.append(name)

    verb = "已卸载" if a.uninstall else "已挂载"
    if not a.yes:
        verb = "将" + ("卸载" if a.uninstall else "挂载")
    print("%s %d 个：" % (verb, len(done)))
    for n in done:
        print("  -", n)
    if skipped:
        print("跳过 %d 个（已存在，加 --force 可覆盖）：" % len(skipped))
        for n in skipped:
            print("  ~", n)
    if missing:
        print("未找到 %d 个（目标目录里没有）：" % len(missing))
        for n in missing:
            print("  ?", n)

    if not a.yes:
        print("-" * 56)
        print("这是 dry-run。确认无误后加 --yes 真正执行。")


if __name__ == "__main__":
    main()
