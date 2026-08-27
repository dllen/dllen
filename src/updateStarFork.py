import os
import sys

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


def main():
    env = load_env()
    token = env.get("GH_TOKEN")
    if not token:
        print("GH_TOKEN not found in .env", file=sys.stderr)
        sys.exit(1)

    repo = os.environ.get("GITHUB_REPO", "dllen/dllen")
    template = os.environ.get(
        "DESCRIPTION_TEMPLATE",
        "A profile README with <starCount> stars and <forkCount> forks 🌟",
    )

    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.github.com/repos/{repo}"

    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()

    description = (
        template.replace("<starCount>", str(data["stargazers_count"]))
        .replace("<forkCount>", str(data["forks_count"]))
    )

    r = requests.patch(url, headers=headers, json={"description": description})
    r.raise_for_status()
    print(f"Updated {repo} description: {description}")


if __name__ == "__main__":
    main()
