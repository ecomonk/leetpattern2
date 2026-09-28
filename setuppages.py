from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def write_file(path: Path, content: str):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Created: {path.relative_to(ROOT)}")
    else:
        print(f"Exists:  {path.relative_to(ROOT)}")


def run(cmd):
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


# ---------------------------------------------------------
# Jekyll configuration
# ---------------------------------------------------------

write_file(
    ROOT / "_config.yml",
    """title: My Notes
description: My Markdown notes
theme: minima

markdown: kramdown

# Make Markdown files available as pages.
collections:
  notes:
    output: true
    permalink: /:name/
""",
)


# ---------------------------------------------------------
# Homepage
# ---------------------------------------------------------

write_file(
    ROOT / "index.md",
    """---
layout: home
title: My Notes
---

Welcome to my notes.

{% assign notes = site.static_files | where_exp: "file", "file.path contains '.md'" %}

## Notes

{% for file in notes %}
{% unless file.path contains "index.md" %}
- [{{ file.basename | replace: "-", " " | capitalize }}]({{ file.path | relative_url }})
{% endunless %}
{% endfor %}
""",
)


# ---------------------------------------------------------
# Gemfile
# ---------------------------------------------------------

write_file(
    ROOT / "Gemfile",
    """source "https://rubygems.org"

gem "github-pages", group: :jekyll_plugins
""",
)


# ---------------------------------------------------------
# GitHub Pages workflow
# ---------------------------------------------------------

write_file(
    ROOT / ".github" / "workflows" / "pages.yml",
    """name: Build and Deploy GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: "3.3"
          bundler-cache: true

      - name: Build site
        run: bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"
        env:
          JEKYLL_ENV: production

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./_site

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
""",
)


# ---------------------------------------------------------
# .gitignore
# ---------------------------------------------------------

write_file(
    ROOT / ".gitignore",
    """_site/
.sass-cache/
.jekyll-cache/
.jekyll-metadata
.bundle/
vendor/
.DS_Store
*.swp
*.swo
""",
)


# ---------------------------------------------------------
# Git repository
# ---------------------------------------------------------

git_dir = ROOT / ".git"

if not git_dir.exists():
    print("Initializing Git repository...")
    run(["git", "init"])
    run(["git", "branch", "-M", "main"])
else:
    print("Git repository already exists.")


# ---------------------------------------------------------
# Commit
# ---------------------------------------------------------

run(["git", "add", "."])

result = subprocess.run(
    ["git", "diff", "--cached", "--quiet"],
    cwd=ROOT,
)

if result.returncode != 0:
    run(["git", "commit", "-m", "Set up GitHub Pages"])

print()
print("=" * 60)
print("GitHub Pages setup complete!")
print("=" * 60)
print()
print("Next step:")
print()
print("1. Create an empty repository on GitHub.")
print("2. Copy its HTTPS URL.")
print("3. Run:")
print()
print("   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git")
print("   git push -u origin main")
print()
print("Then enable GitHub Pages using:")
print()
print("   Settings -> Pages -> Source: GitHub Actions")
print()
print("After that, future .md files can simply be added and pushed.")
print()
