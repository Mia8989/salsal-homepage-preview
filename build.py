#!/usr/bin/env python3
"""SALSAL site: stamp the global nav + footer partials into every page.

Divi-style global elements for a static site. Edit partials/nav.html or
partials/footer.html once, run `python3 build.py`, and every *.html page in
this folder gets the updated block. Idempotent: blocks live between
NAV:START/NAV:END and FOOTER:START/FOOTER:END markers; on first run, legacy
unmarked nav/footer blocks (copied from the exemplar) are migrated to markers.
Active nav state is set client-side by the small script inside the nav partial,
so the same markup works on every page.
"""
import re, sys, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

nav = read(os.path.join(HERE, "partials", "nav.html")).strip()
footer = read(os.path.join(HERE, "partials", "footer.html")).strip()

NAV_BLOCK = "<!-- NAV:START (edit partials/nav.html, then run build.py) -->\n" + nav + "\n<!-- NAV:END -->"
FOOT_BLOCK = "<!-- FOOTER:START (edit partials/footer.html, then run build.py) -->\n" + footer + "\n<!-- FOOTER:END -->"

# marked blocks (idempotent path)
RE_NAV_MARK = re.compile(r"<!-- NAV:START.*?<!-- NAV:END -->", re.S)
RE_FOOT_MARK = re.compile(r"<!-- FOOTER:START.*?<!-- FOOTER:END -->", re.S)
# legacy unmarked blocks (first-run migration)
RE_NAV_LEGACY = re.compile(r'<div class="navwrap">.*?</nav>\s*</div>', re.S)
RE_FOOT_LEGACY = re.compile(r'<footer class="footer">.*?</footer>', re.S)

changed, skipped = [], []
for path in sorted(glob.glob(os.path.join(HERE, "*.html"))):
    name = os.path.basename(path)
    html = read(path)
    orig = html

    if RE_NAV_MARK.search(html):
        html = RE_NAV_MARK.sub(lambda m: NAV_BLOCK, html, count=1)
    elif RE_NAV_LEGACY.search(html):
        html = RE_NAV_LEGACY.sub(lambda m: NAV_BLOCK, html, count=1)
    else:
        print(f"  ! {name}: no nav found (page skipped for nav)")

    if RE_FOOT_MARK.search(html):
        html = RE_FOOT_MARK.sub(lambda m: FOOT_BLOCK, html, count=1)
    elif RE_FOOT_LEGACY.search(html):
        html = RE_FOOT_LEGACY.sub(lambda m: FOOT_BLOCK, html, count=1)
    else:
        print(f"  ! {name}: no footer found (page skipped for footer)")

    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        changed.append(name)
    else:
        skipped.append(name)

print(f"updated: {len(changed)} -> {', '.join(changed) if changed else 'none'}")
print(f"unchanged: {len(skipped)} -> {', '.join(skipped) if skipped else 'none'}")
