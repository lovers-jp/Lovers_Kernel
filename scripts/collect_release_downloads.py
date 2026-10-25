#!/usr/bin/env python3
"""Collect GitHub Release asset cumulative download counts into dated CSVs.

No third-party dependencies. Run in GitHub Actions with GITHUB_TOKEN.
"""

import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "lovers-jp/Lovers_Kernel")
TOKEN = os.environ.get("GH_TOKEN", os.environ.get("GITHUB_TOKEN", ""))
DATE = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d")
ROOT = Path("stats")
HISTORY = ROOT / "history"
COLUMNS = ["date_jst", "tag", "asset_id", "asset_name", "downloads"]


def api_releases():
    """Return all public/published releases via API pagination."""
    all_releases = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{REPOSITORY}/releases?per_page=100&page={page}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "LoversKernel-ReleaseDownloadStats",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if TOKEN:
            headers["Authorization"] = f"Bearer {TOKEN}"
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=35) as response:
                batch = json.load(response)
        except HTTPError as e:
            raise RuntimeError(f"GitHub API error {e.code} while requesting release page {page}") from e
        except URLError as e:
            raise RuntimeError(f"Network error while requesting release page {page}: {e}") from e
        if not isinstance(batch, list):
            raise RuntimeError("Unexpected GitHub API response: expected list of releases")
        all_releases.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return all_releases


def read_previous_snapshot():
    """Use the latest *earlier-day* snapshot as the comparison baseline."""
    candidates = sorted(path for path in HISTORY.glob("????-??-??.csv") if path.stem < DATE)
    if not candidates:
        return None, {}
    previous = candidates[-1]
    with previous.open("r", newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return previous.stem, {row["asset_id"]: int(row["downloads"]) for row in rows}


def main():
    if "/" not in REPOSITORY:
        raise ValueError("GITHUB_REPOSITORY must be owner/repository")
    releases = api_releases()
    HISTORY.mkdir(parents=True, exist_ok=True)
    prev_date, prev_counts = read_previous_snapshot()
    rows = []
    for release in releases:
        tag = release.get("tag_name") or "(untagged)"
        for asset in release.get("assets", []):
            if asset.get("state") != "uploaded":
                continue
            rows.append({
                "date_jst": DATE,
                "tag": tag,
                "asset_id": str(asset["id"]),
                "asset_name": asset["name"],
                "downloads": int(asset["download_count"]),
            })

    output = HISTORY / f"{DATE}.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    # latest.csv contains the current cumulative totals, useful for spreadsheets.
    with (ROOT / "latest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    overall = sum(row["downloads"] for row in rows)
    kernel_zip = sum(row["downloads"] for row in rows if row["asset_name"].lower().endswith(".zip"))
    apk = sum(row["downloads"] for row in rows if row["asset_name"].lower().endswith(".apk"))

    lines = [
        "# Lovers_Kernel Releaseダウンロード統計",
        "",
        f"集計日（日本時間）: **{DATE}**",
        "",
        f"- 全添付ファイルの累計DL数（延べ回数）: **{overall:,}**",
        f"- ZIPファイルの累計DL数: **{kernel_zip:,}**",
        f"- APKファイルの累計DL数: **{apk:,}**",
        f"- 集計対象: **{len(rows)} ファイル**",
        "",
        f"前回の記録日: **{prev_date or 'なし（初回記録）'}**",
        "",
        "| リリース | ファイル | 累計DL数 | 前回記録比 |",
        "|---|---|---:|---:|",
    ]
    for row in rows:
        key = row["asset_id"]
        old = prev_counts.get(key)
        delta = f"+{max(row['downloads'] - old, 0):,}" if old is not None else "—"
        name = row["asset_name"].replace("|", "\\|")
        tag = row["tag"].replace("|", "\\|")
        lines.append(f"| {tag} | {name} | {row['downloads']:,} | {delta} |")
    if not rows:
        lines.append("| — | 公開済みリリースの添付ファイルなし | 0 | — |")
    lines.extend([
        "",
        "※ ダウンロード数はGitHub APIの `download_count` に基づく延べ回数です。ユニークユーザー数ではありません。",
        "",
        "※ 前回記録比は、同じAsset IDが過去の記録にも存在する場合のみ表示します。初回・新規ファイルは『—』です。",
        "",
        "※ GitHubが自動生成するSource code (zip/tar.gz)は集計対象ではありません。",
        "",
        "※ 日付は各実行日のスナップショット取得日であり、正確なダウンロード発生日時ではありません。",
        "",
    ])
    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Release files: {len(rows)}, overall downloads: {overall}")
    print(f"Wrote {output}, {ROOT / 'latest.csv'}, {ROOT / 'README.md'}")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
