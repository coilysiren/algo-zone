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
  if [[  $dataFile == "*/readme.md" ]]; then continue; fi

  # sort them with every sort script
  for sortScript in ./src/"$language"/sort_*; do
    # use the language to run the sort script with the two data files
    $language "$sortScript" "$dataFile/randomized.txt" "$dataFile/sorted.txt"
  done

done
