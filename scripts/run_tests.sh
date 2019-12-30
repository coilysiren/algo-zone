#!/bin/bash

set -euo pipefail

language="${1:-python}"

# at the beginning, we assume no script has failed
# at the end, we check if any script has failed
aScriptHasFailed="false"

# the base directory is prepended to the path that
# we give to our scripts, to prevent unfortunate path
# tragedies
baseDirectory=$PWD

# for everything in the data folder
for baseDataFilePath in ./data/*; do
  # results come out looking like
  #  ./data/first-names
  #  ./data/readme.md
  # etc, without including any folder contents

  # except for readmes
  if [[ "$baseDataFilePath" == *readme.md* ]]; then continue; fi

  # get the full path for the randomized data
  randomDataFilePath="$baseDirectory/./$baseDataFilePath/randomized.txt"

  # load the expected data into a variable, for comparison (later)
  expectedOutputDataFileName="sorted.txt"
  expectedOutputDataPath="$baseDataFilePath/$expectedOutputDataFileName"
  expectedOutputData=$(< "$expectedOutputDataPath")

  # sort with every sort script
  for sortScript in ./src/"$language"/sort_*; do

    # cleanup the script name, for later use as a file name
    #   - the 1st sed removes "./src/"
    #   - the 2nd sed turns "/" into "_"
    #   - the 3rd sed turns "." into "_"
    # result "./src/python/sort_builtin.py" => "python_sort_builtin_py"
    scriptName=$(echo "$sortScript" \
      | sed "s/\.\/src\///" \
      | sed "s/\//_/" \
      | sed "s/\./_/" \
    )

    # get the full path for the script output data
    scriptOutputDataFileName="sorted_by_$scriptName.txt"
    scriptOutputDataFilePath="$baseDirectory/./$baseDataFilePath/$scriptOutputDataFileName"

    # if an old script output file already exists, remove it
    rm -f "$scriptOutputDataFilePath"

    # use the language to run the sort script with the two file paths as arguments
    set +e # dont exit if the language script errors
    $language "$sortScript" "$randomDataFilePath" "$scriptOutputDataFilePath"

    # check to see if our script exited successfully
    scriptExitCode=$?
    if [[ "$scriptExitCode" != 0 ]]; then
        aScriptHasFailed="true"
        echo "🔴 script $sortScript failed, reason:"
        echo "   the exit code \"$scriptExitCode\" was not 0"
        continue
    fi
    set -e # re-enable exiting on unknown errors

    # check to see if our script wrote to the data file path
    if [[ ! -f "$scriptOutputDataFilePath" ]]; then
        aScriptHasFailed="true"
        echo "🔴 script $sortScript failed, reason:"
        echo "   no output file created, the script likely has an error"
        continue
    fi

    # load the script sorted data into a variable, for comparison
    scriptOutputData=$(< "$scriptOutputDataFilePath")

    # compare the script sorted data with the expected sorted data
    if [[ "$scriptOutputData" == "$expectedOutputData" ]]; then
      echo "🟢 script $sortScript succeeded"
    else
      aScriptHasFailed="true"
      echo "🔴 script $sortScript failed, reason:"
      echo "   output file $scriptOutputDataFileName has incorrect contents"
      echo "   displaying file diff for $expectedOutputDataFileName vs $scriptOutputDataFileName"
      set +e # ignore exit code from the diff command
      diff -d "$expectedOutputDataPath" "$scriptOutputDataFilePath"
      set -e # re-enable exiting on unknown errors
    fi

  done

done

# check to see if any script has failed
if [[ $aScriptHasFailed == "false" ]]; then
  echo "✨ all scripts succeeded ✨"
  exit 1
else
  echo "🚨 a script failed! 🚨"
  exit 0
fi
