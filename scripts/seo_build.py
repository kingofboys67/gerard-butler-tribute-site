#!/usr/bin/env python3
"""
One-command SEO build for gerardbutlerofficial.com.

Pipeline (all steps idempotent):
  1. seo_hardening.py    meta/social dedupe, descriptions, image dims, OG cards,
                         hreflang, footer site index + freshness date
  2. build_film_index.py full A-Z filmography index + per-film cross-links & FAQ
  3. build_seo_files.py  robots.txt, sitemap.xml, llms.txt, ai-knowledge.json
  4. deep_seo_audit.py   verification report

Usage:
  python3 scripts/seo_build.py          # build + audit summary
  python3 scripts/seo_build.py --quiet  # build only
"""

import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEPS = ["seo_hardening.py", "build_film_index.py", "build_seo_files.py"]


def run(script):
    print("\n=== %s ===" % script)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", script)], cwd=ROOT)
    if r.returncode != 0:
        sys.exit("FAILED: %s" % script)


def main():
    for step in STEPS:
        run(step)
    if "--quiet" not in sys.argv:
        run("deep_seo_audit.py")


if __name__ == "__main__":
    main()
