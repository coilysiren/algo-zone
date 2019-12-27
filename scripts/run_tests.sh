#!/bin/bash

set -euo pipefail
set -o xtrace

language="${1:-python}"

# for everything in the data folder
for dataFile in ./data/*; do
  # results come out looking like
  #  ./data/first-names
  #  ./data/readme.md
  # etc, without including any folder contents

  # except for readmes
  if [[  $dataFile == "*/readme.md" ]]; then continue end

  # sort them with every sort script
  for sortScript in ./src/$language/sort_*; do
    $language $sortScript $dataFile"/
  done

  if dataFile ==
  echo $dataFile
  # TODO
done
