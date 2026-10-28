# Gerard Butler Official — static site tooling
# This is not a Node project: Vercel serves the pre-built HTML directly.
# The build pipeline is Python (stdlib + Pillow for OG card generation).

.PHONY: build pages audit check indexnow serve clean-og

build:
	python3 scripts/seo_build.py --quiet
	python3 scripts/check_html.py

pages:
	python3 scripts/build_reference_pages.py

audit:
	python3 scripts/deep_seo_audit.py

check:
	python3 scripts/check_html.py

indexnow:
	python3 scripts/ping_indexnow.py

serve:
	python3 -m http.server 8765

clean-og:
	rm -rf img/og && echo "OG cards cleared — next build regenerates them"
