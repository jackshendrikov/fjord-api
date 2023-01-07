#!/bin/sh

if ! git diff --cached --name-only --diff-filter=ACM | grep "^version.py$"; then
  echo "[INFO] You forgot to update the version, but I'll update for you this time :("

  current_version=$(grep -Eo "[0-9]\.[0-9]\.[0-9]+" version.py)
  new_version=$(echo "${current_version}" | awk -F. '/[0-9]+\./{$NF++;print}' OFS=.)
  sed -i "s/$current_version/$new_version/" version.py
fi
