import os
import re
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


def format_row(name, text, percent, total_blocks=25):
    filled = int(percent / 100 * total_blocks)
    partial = 1 if (percent / 100 * total_blocks) - filled > 0 else 0
    empty = total_blocks - filled - partial
    blocks = "🟩" * filled + "🟨" * partial + "⬜" * empty
    return f"{name:<16} {text:>14}  {blocks}  {percent:>6.2f} %"


def main():
    env = load_env()
    base_url = env.get("WAKAPI_BASE_URL", "").rstrip("/")
    api_key = env.get("WAKAPI_API_KEY")
    if not base_url or not api_key:
        print("WAKAPI_BASE_URL and WAKAPI_API_KEY required in .env", file=sys.stderr)
        sys.exit(1)

    time_range = os.environ.get("WAKA_RANGE", "last_30_days")
    url = f"{base_url}/api/compat/wakatime/v1/users/current/stats/{time_range}"
    r = requests.get(url, headers={"Authorization": f"Basic {api_key}"})
    r.raise_for_status()
    data = r.json()["data"]

    lines = [""]
    for lang in data.get("languages", []):
        lines.append(format_row(lang["name"], lang["text"], lang["percent"]))
    lines.append("")

    readme = Path("README.md").read_text(encoding="utf-8")
    readme = re.sub(
        r"(?<=<!--START_SECTION:waka-->\n)[\s\S]*(?=\n<!--END_SECTION:waka-->)",
        "\n".join(lines),
        readme,
    )
    Path("README.md").write_text(readme, encoding="utf-8")
    print(f"Updated Wakapi stats ({len(lines) - 2} languages)")


if __name__ == "__main__":
    main()
