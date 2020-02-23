# builtin packages
import filecmp
import glob
import os
import string
import subprocess
import sys

# 3rd party packages
import yaml


class TestRunner(object):
    # successful tracks the success status of the test runs
    successful = None
    # language is the programming language to run scripts in
    language = ""
    # input_script is the name of a script you want to run
    input_script = ""
    # base_directory is prepended to many of our paths
    base_directory = ""
    # config contains language specific configuration
    config = {}

    # __init__ reads off of sys.argv, and the first input arg is the name of this file
    def __init__(self, _, language="python", input_script=""):
        self.language = language
        self.input_script = input_script
        self.base_directory = os.getcwd()
        with open(f"{self.base_directory}/config.yml", "r") as obj:
            data = obj.read()
            config_yaml = yaml.safe_load(data)
            self.config = config_yaml[self.language]

    def run_tests(self):
        # for everything in the data folder
        for data_folder_name in os.listdir(f"{self.base_directory}/data/"):

            # expand the data folder name into it's full path
            data_folder_path = f"./data/{data_folder_name}"

            # check if it's a sub-folder containing data, and continue if not
            if not os.path.isdir(data_folder_path):
                continue

            # run every sort script
            for script_path in glob.glob(
                f"{self.base_directory}/src/{self.language}/sort_*"
            ):

                # given "src/python/sort_builtin.py" => split on "/" and return "sort_builtin.py"
                script_path_split_on_slash = script_path.split("/")
                script_name_with_file_type = script_path_split_on_slash[-1]

                # given "sort_builtin.py" => split on "." and return "sort_builtin"
                script_name_split_on_dot = script_name_with_file_type.split(".")
                script_name = script_name_split_on_dot[0]

                # this path is used in various places later
                script_relative_path = (
                    f"./src/{self.language}/{script_name_with_file_type}"
                )

                # get the path of the file that's been prepared in advance
                # and has the output we would be expecting from out script
                preparedFilePath = f"{data_folder_path}/sorted.txt"

                # our scripts write their output files to this path
                script_output_file_name = f"sorted_by_{self.language}_{script_name}.txt"
                script_output_file_path = (
                    f"{data_folder_path}/{script_output_file_name}"
                )

                # if an input script was passed in, and this script is not that input script
                # then continue on to the next script
                if (self.input_script != "") and (script_name != self.input_script):
                    continue

                # if an old script output file already exists, remove it
                if os.path.isfile(script_output_file_path):
                    os.remove(script_output_file_path)

                # script_invoker is command that we run in a subprocess to invoke our script
                # it needs to be split on spaces since subprocess.call excepts a list as input
                # whenever we aren't using the shell=True arguement
                script_invoker = self.config["scriptInvoker"].split(" ")

                # script_to_invoke is the literal script name that we pass to the invoker
                # we assume that invokers accept paths by default (eg. script_path)
                # and that other invokers want script names (eg. script_name)
                # the useShortScriptName config value controls this behavior
                if self.config.get("useShortScriptName", False) == False:
                    script_to_invoke = script_relative_path
                else:
                    script_to_invoke = script_name

                # construction initial call args
                call_args = [
                    "docker",
                    "run",
                    f"--volume={self.base_directory}:/workdir",
                    f"-w=/workdir",
                ]

                # construct env vars CLI args
                envVars = self.config.get("envVars", "")
                if envVars != "":
                    call_args.append(f"-e={envVars}")

                # construct ending call args
                call_args += [
                    f"-e=INPUT_PATH={data_folder_path}/randomized.txt",
                    f"-e=OUTPUT_PATH={script_output_file_path}",
                    self.config["dockerImage"],
                    *script_invoker,
                    script_to_invoke,
                    self.config.get("scriptSuffix", ""),
                ]
                status = subprocess.call(call_args)

                # check if the script invoke failed
                if status != 0:
                    self.set_success_status(False)
                    print(
                        f'🔴 script "{script_relative_path}" failed on data "{data_folder_name}", reason:'
                    )
                    print(f'\t the exit code "{status}" was not 0')

                # check if the output file was created
                if not os.path.isfile(script_output_file_path):
                    self.set_success_status(False)
                    print(
                        f'🔴 script "{script_relative_path}" failed on data "{data_folder_name}", reason:'
                    )
                    print(
                        f"\t the output {script_output_file_name} file was not created"
                    )

                # check if the output file matches the prepared file
                if filecmp.cmp(preparedFilePath, script_output_file_path):
                    self.set_success_status(True)
                    print(
                        f'🟢 script "{script_relative_path}" succeeded on data "{data_folder_name}"'
                    )
                else:
                    self.set_success_status(False)
                    print(
                        f'🔴 script "{script_relative_path}" failed on data "{data_folder_name}", reason:'
                    )
                    print(
                        f"\t output file {script_output_file_name} has does not match the prepared file"
                    )

    def set_success_status(self, status: bool):
        # only update the test success status if it wasnt already false
        if self.successful != False:
            self.successful = status

    def show_results(self):
        if self.successful == True:
            print("✨ script run success ✨")
            sys.exit(0)
        else:
            print("🚨 script run failure 🚨")
            sys.exit(1)


if __name__ == "__main__":
    # run tests
    runner = TestRunner(*sys.argv)
    runner.run_tests()
    runner.show_results()
