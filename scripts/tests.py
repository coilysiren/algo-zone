# builtin packages
import filecmp
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
a_script_has_failed = False

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
for data_folder_name in os.listdir(f"{base_directory}/data/"):

    # expand the data folder name into it's full path
    data_folder_path = f"./data/{data_folder_name}"

    # check if it's a sub-folder containing data, and continue if not
    if not os.path.isdir(data_folder_path):
        continue

    # run every sort script
    for script_path in glob.glob(f"{base_directory}/src/{language}/sort_*"):

        # given "src/python/sort_builtin.py" => split on "/" and return "sort_builtin.py"
        script_path_split_on_slash = script_path.split("/")
        script_name_with_file_type = script_path_split_on_slash[-1]

        # given "sort_builtin.py" => split on "." and return "sort_builtin"
        script_name_split_on_dot = script_name_with_file_type.split(".")
        script_name = script_name_split_on_dot[0]

        # this path is used in various places later
        script_relative_path = f"./src/{language}/{script_name_with_file_type}"

        # get the path of the file that's been prepared in advance
        # and has the output we would be expecting from out script
        preparedFilePath = f"{data_folder_path}/sorted.txt"

        # our scripts write their output files to this path
        script_output_file_name = f"sorted_by_{language}_{script_name}.txt"
        script_output_file_path = f"{data_folder_path}/{script_output_file_name}"

        # if an old script output file already exists, remove it
        if os.path.isfile(script_output_file_path):
            os.remove(script_output_file_path)

        # script_invoker is command that we run in a subprocess to invoke our script
        # it needs to be split on spaces since subprocess.call excepts a list as input
        # whenever we aren't using the shell=True arguement
        script_invoker = config[language]["scriptInvoker"].split(" ")

        # script_to_invoke is the literal script name that we pass to the invoker
        # we assume that invokers accept paths by default (eg. script_path)
        # and that other invokers want script names (eg. script_name)
        # the useShortScriptName config value controls this behavior
        if config[language].get("useShortScriptName", False) == False:
            script_to_invoke = script_relative_path
        else:
            script_to_invoke = script_name

        # construction initial call args
        call_args = [
            "docker",
            "run",
            f"--volume={base_directory}:/workdir",
            f"-w=/workdir",
        ]

        # construct env vars CLI args
        envVars = config[language].get("envVars", "")
        if envVars != "":
            call_args.append(f"-e={envVars}")

        # construct ending call args
        call_args += [
            f"-e=INPUT_PATH={data_folder_path}/randomized.txt",
            f"-e=OUTPUT_PATH={script_output_file_path}",
            config[language]["dockerImage"],
            *script_invoker,
            script_to_invoke,
            config[language].get("scriptSuffix", ""),
        ]
        status = subprocess.call(call_args)

        # check if the script invoke failed
        if status != 0:
            print(
                f'🔴 script "{script_relative_path}" failed on data "{data_folder_name}", reason:'
            )
            print(f'\t the exit code "{status}" was not 0')
            a_script_has_failed = True
            continue

        # check if the output file was created
        if not os.path.isfile(script_output_file_path):
            print(
                f'🔴 script "{script_relative_path}" failed on data "{data_folder_name}", reason:'
            )
            print(f"\t the output {script_output_file_name} file was not created")
            a_script_has_failed = True
            continue

        # check if the output file matches the prepared file
        if filecmp.cmp(preparedFilePath, script_output_file_path):
            print(
                f'🟢 script "{script_relative_path}" succeeded on data "{data_folder_name}"'
            )
        else:
            print(
                f'🔴 script "{script_relative_path}" failed on data "{data_folder_name}", reason:'
            )
            print(
                f"\t output file {script_output_file_name} has does not match the prepared file"
            )

if a_script_has_failed:
    print("🚨 a script failed! 🚨")
    sys.exit(1)
else:
    print("✨ all scripts succeeded ✨")
    sys.exit(0)
