#!/bin/bash
cd "/Users/nealbarenblat/Documents/Claude Playground/Projects/Chile News/Chile News"
git add .
git commit -m "Digest 260528 — with source links" --allow-empty
git push origin main
echo ""
echo "✓ Done. This window can be closed."
read -n1
