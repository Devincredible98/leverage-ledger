#!/bin/bash
# The Leverage Ledger — daily generate + push to GitHub Pages
# Requires: GITHUB_TOKEN (classic PAT, repo scope) and a repo <owner>/leverage-ledger
set -e
cd /Users/devinhandford/leverage-ledger

# 1. generate today's issue
python3 generate.py

# 2. commit + push
git add feed.xml newsletter.md
if git diff --cached --quiet; then
  echo "No changes to push"
else
  git -c user.name="Devin Handford" -c user.email="devincredible0@gmail.com" \
    commit -m "Daily Leverage Ledger issue $(date +%Y-%m-%d)"
  git push https://${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git main
  echo "Pushed to GitHub Pages"
fi
