# builtin packages
import glob
import os
import string
import subprocess
import sys

# 3rd party packages
import yaml

# get the language to run, defaulting to python
if len(sys.argv) > 1:
    language = sys.argv[1]
else:
    language = "python"

# at the beginning, we assume no script has failed
# at the end, we check if any script has failed
aScriptHasFailed = False

# the base directory is prepended to the path that
# we give to our scripts, to prevent unfortunate path tragedies
base_directory = os.getcwd()

# get the config file, which contains customization info
# about each of our languages
with open(f"{base_directory}/config.yml", "r") as config_file_object:
    config_file_data = config_file_object.read()
    config = yaml.safe_load(config_file_data)
    # ^ this would be called `config_file_yaml` or similar to match the naming
    # but then we would have to use that verbose reference for the rest
    # of this script. so we opt for the short `config` instead.

# for everything in the data folder
for data_folder in [
    f"{base_directory}/data/{name}" for name in os.listdir(f"{base_directory}/data/")
]:

    # check if it's a sub-folder containing data, and continue if not
    if not os.path.isdir(data_folder):
        continue

    # run every sort script
    for scriptPath in glob.glob(f"{base_directory}/src/{language}/sort_*"):

        # given "src/python/sort_builtin.py" => split on "/" and return "sort_builtin.py"
        scriptPathSplitOnSlash = scriptPath.split("/")
        scriptNameWithFileType = scriptPathSplitOnSlash[-1]

        # given "sort_builtin.py" => split on "." and return "sort_builtin"
        scriptNameSplitOnDot = scriptNameWithFileType.split(".")
        scriptName = scriptNameSplitOnDot[0]

        # our scripts write their output files to this path
        scriptOutputFilePath = f"{data_folder}/sorted_by_{language}_{scriptName}.txt"

        # if an old script output file already exists, remove it
        if os.path.isfile(scriptOutputFilePath):
            os.remove(scriptOutputFilePath)

        # scriptInvoker is command that we run in a subprocess to invoke our script
        # it needs to be split on spaces since subprocess.call excepts a list as input
        # when we aren't using shell=True
        scriptInvoker = config[language]["scriptInvoker"].split(" ")

        # scriptToInvoke is the literal script name that we pass to the invoker
        # we assume that invokers accept paths by default (eg. scriptPath)
        # and that other invokers want script names (eg. scriptName)
        # the useShortScriptName config value controls this behavior
        if config[language].get("useShortScriptName", False) == False:
            scriptToInvoke = scriptPath
        else:
            scriptToInvoke = scriptName

        # this calls ends up looking like
        #   python ./src/python/sort_builtin.py \
        #       ./data/first-names/randomized.txt \
        #       ./data/first-names/sorted_by_python_sort_builtin.txt
        subprocess.call(
            [
                *scriptInvoker,
                scriptToInvoke,
                f"{data_folder}/randomized.txt",
                scriptOutputFilePath,
            ]
        )

#         scriptName = string.replace(scriptName, "./")

#     # cleanup the script name, for later use as a file name
#     #   - the 1st sed removes "./src/"
#     #   - the 2nd sed turns "/" into "_"
#     #   - the 3rd sed turns "." into "_"
#     # result "./src/python/sort_builtin.py" => "python_sort_builtin_py"
#     scriptName=$(echo "$script" \
#       | sed "s/\.\/src\///" \
#       | sed "s/\//_/" \
#       | sed "s/\./_/" \
#     )

#     # get the full path for the script output data
#     scriptOutputDataFileName="sorted_by_$scriptName.txt"
#     scriptOutputDataFilePath="$baseDirectory/./$baseDataFilePath/$scriptOutputDataFileName"

#     rm -f "$scriptOutputDataFilePath"

#     # use the language executable to run the script with the two file paths as arguments
#     set +e # dont exit if the language script errors
#     $scriptInvoker "$script" "$randomDataFilePath" "$scriptOutputDataFilePath"

#     # check to see if our script exited successfully
#     scriptExitCode=$?
#     if [[ "$scriptExitCode" != 0 ]]; then
#         aScriptHasFailed="true"
#         echo "🔴 script $script failed, reason:"
#         echo "   the exit code \"$scriptExitCode\" was not 0"
#         continue
#     fi
#     set -e # re-enable exiting on unknown errors

#     # check to see if our script wrote to the data file path
#     if [[ ! -f "$scriptOutputDataFilePath" ]]; then
#         aScriptHasFailed="true"
#         echo "🔴 script $script failed, reason:"
#         echo "   no output file created, the script likely has an error"
#         continue
#     fi

#     # load the script sorted data into a variable, for comparison
#     scriptOutputData=$(< "$scriptOutputDataFilePath")

#     # compare the script sorted data with the expected sorted data
#     if [[ "$scriptOutputData" == "$expectedOutputData" ]]; then
#       echo "🟢 script $script succeeded"
#     else
#       aScriptHasFailed="true"
#       echo "🔴 script $script failed, reason:"
#       echo "   output file $scriptOutputDataFileName has incorrect contents"
#       echo "   displaying file diff for $expectedOutputDataFileName vs $scriptOutputDataFileName"
#       set +e # ignore exit code from the diff command
#       diff -d "$expectedOutputDataPath" "$scriptOutputDataFilePath"
#       set -e # re-enable exiting on unknown errors
#     fi

#   done

# done

# # check to see if any script has failed
# if [[ $aScriptHasFailed == "false" ]]; then
#   echo "✨ all scripts succeeded ✨"
#   exit 0
# else
#   echo "🚨 a script failed! 🚨"
#   exit 1
# fi
