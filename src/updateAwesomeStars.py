import os
import sys
from pathlib import Path

import requests


def load_env(path=".env"):
    env = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env[key] = value
    return env


def anchor(lang):
    return (
        lang.lower()
        .replace("#", "sharp")
        .replace("+", "plus")
        .replace(" ", "-")
        .replace(".", "")
    )


def main():
    env = load_env()
    token = env.get("GH_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    username = os.environ.get("GITHUB_USER", "dllen")

    stars = []
    page = 1
    while True:
        r = requests.get(
            f"https://api.github.com/users/{username}/starred",
            headers=headers,
            params={"per_page": 100, "page": page},
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        stars.extend(data)
        if len(data) < 100:
            break
        page += 1

    by_lang = {}
    for repo in stars:
        lang = repo["language"] or "Unknown"
        by_lang.setdefault(lang, []).append(repo)

    lines = [
        "<!--lint disable awesome-contributing awesome-license awesome-list-item match-punctuation no-repeat-punctuation no-undefined-references awesome-spell-check-->",
        '# Awesome Stars [![Awesome](https://awesome.re/badge.svg)](https://github.com/sindresorhus/awesome)',
        "",
        "> A curated list of my GitHub stars!",
        "",
        "## Contents",
        "",
    ]

    for lang in sorted(by_lang):
        lines.append(f"- [{lang}](#{anchor(lang)})")

    lines.append("")

    for lang in sorted(by_lang):
        lines.append(f"## {lang}")
        lines.append("")
        for repo in sorted(by_lang[lang], key=lambda r: r["stargazers_count"], reverse=True):
            desc = repo["description"] or ""
            lines.append(f'- [{repo["full_name"]}]({repo["html_url"]}) — {desc}')
        lines.append("")

    Path("AWESOME-STARS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated AWESOME-STARS.md with {len(stars)} repos")


if __name__ == "__main__":
    main()
