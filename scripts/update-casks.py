#!/usr/bin/env python3
"""Update every cask in this tap using Homebrew's upstream release checks."""

import json
import subprocess

TAP = "jaredwad/personal"


def main():
    result = subprocess.run(
        ["brew", "livecheck", f"--tap={TAP}", "--cask", "--json"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )

    for package in json.loads(result.stdout):
        name = package["cask"].rsplit("/", 1)[-1]
        version = package.get("version")
        if not version:
            print(f"{name}: {package}", flush=True)
            continue
        if not version["outdated"]:
            print(f"{name}: current ({version['current']})", flush=True)
            continue

        latest = version["latest"]
        print(f"{name}: {version['current']} -> {latest}", flush=True)
        subprocess.run(
            [
                "brew", "bump-cask-pr", "--write-only", "--no-audit", "--no-style",
                f"--version={latest}", f"{TAP}/{name}",
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
