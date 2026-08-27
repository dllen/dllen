import re
from pathlib import Path


def main():
    atom = Path("atom.xml").read_text(encoding="utf-8")
    entries = re.findall(r"<entry\b[\s\S]*?</entry>", atom)[:5]

    posts = []
    for e in entries:
        title = re.search(r"<title>([\s\S]*?)</title>", e).group(1)
        date = re.search(r"<updated>([\s\S]*?)</updated>", e).group(1).split("T")[0]
        url = re.search(r'<link rel="alternate"[^>]*href="([^"]+)"', e).group(1)
        posts.append(f"-   {date} [{title}]({url}?utm_source=GitHubProfile)")

    readme = Path("README.md").read_text(encoding="utf-8")
    readme = re.sub(
        r"(?<=<!--START_SECTION:blog-posts-->\n)[\s\S]*(?=\n<!--END_SECTION:blog-posts-->)",
        "\n".join(posts),
        readme,
    )
    Path("README.md").write_text(readme, encoding="utf-8")
    print(f"Updated {len(posts)} blog posts")


if __name__ == "__main__":
    main()
