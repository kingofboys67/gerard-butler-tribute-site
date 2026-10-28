#!/usr/bin/env python3
"""Structural HTML sanity check: unclosed / stray tags on every page."""

import glob
import os
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "source", "track", "wbr", "path", "circle", "rect", "use",
}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append("unclosed <%s>" % self.stack.pop())
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append("stray </%s>" % tag)


def main():
    bad = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        name = os.path.basename(path)
        p = Checker()
        p.feed(open(path, encoding="utf-8", errors="ignore").read())
        leftover = [t for t in p.stack if t not in ("html", "body")]
        if p.errors or leftover:
            bad += 1
            print("%-42s errors=%s unclosed=%s" % (name, p.errors[:3], leftover[:4]))
    print("\nfiles with structural issues: %d" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
