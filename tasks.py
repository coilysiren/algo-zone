# builtin packages
import filecmp
import glob
import os
import subprocess
import sys

# 3rd party packages
import yaml
import invoke


def inputs_are_truthy_and_different(first, second):
    # check if inputs are truthy
    if (not first) or (not second):
        return False
    # cleanup
    first_cleaned = clean_string(first)
    second_cleaned = clean_string(second)
    # allow for wildcard matching
    wildcard_keyword = "any"
    if (first_cleaned == wildcard_keyword) or (second_cleaned == wildcard_keyword):
        return False
    # check if inputs are different
    if first_cleaned != second_cleaned:
        return True
    return False


def clean_string(inp):
    for element in ["-", "_", "test", "sort"]:
        inp = inp.replace(element, "")
    return inp


class TestRunnerContext:
    script_name: str
    subprocess_args: list
    script_relative_path: str
    script_output_file_path: str
    script_output_file_name: str
    prepared_file_path: str

    def __init__(self, language, script_path) -> None:
        # setup our baseline configuration
        data_folder_path = "./data"
        base_directory = os.getcwd()

        # get the language specific config
        with open(f"{base_directory}/config.yml", "r", encoding="utf-8") as obj:
            data = obj.read()
            config_yaml = yaml.safe_load(data)
            config = config_yaml[language]

        # given "src/python/sort_builtin.py" => split on "/" and return "sort_builtin.py"
        script_path_split_on_slash = script_path.split("/")
        script_name_with_file_type = script_path_split_on_slash[-1]

        # given "sort_builtin.py" => split on "." and return "sort_builtin"
        script_name_split_on_dot = script_name_with_file_type.split(".")
        self.script_name = script_name_split_on_dot[0]

        # this path is used in various places later
        self.script_relative_path = f"./src/{language}/{script_name_with_file_type}"

        # get the path of the file that's been prepared in advance
        # and has the output we would be expecting from out script
        self.prepared_file_path = f"{data_folder_path}/sorted.txt"

        # our scripts write their output files to this path
        self.script_output_file_name = f"sorted_by_{language}_{self.script_name}.txt"
        self.script_output_file_path = (
            f"{data_folder_path}/{self.script_output_file_name}"
        )

        # script_invoker is command that we run in a subprocess to invoke our script
        # it needs to be split on spaces since subprocess.call excepts a list as input
        # whenever we aren't using the shell=True arguement
        script_invoker = config["scriptInvoker"].split(" ")

        # script_to_invoke is the literal script name that we pass to the invoker
        # we assume that invokers accept paths by default (eg. script_path)
        # and that other invokers want script names (eg. script_name)
        # the useShortScriptName config value controls this behavior
        if config.get("useShortScriptName", False) is False:
            script_to_invoke = self.script_relative_path
        else:
            script_to_invoke = self.script_name

        # construction initial call args
        self.subprocess_args = [
            "docker",
            "run",
            f"--volume={base_directory}:/workdir",
            "-w=/workdir",
        ]

        # construct env vars CLI args
        env_vars = config.get("env_vars", "")
        if env_vars != "":
            self.subprocess_args.append(f"-e={env_vars}")

        # construct ending call args
        self.subprocess_args += [
            f"-e=INPUT_PATH={data_folder_path}/randomized.txt",
            f"-e=OUTPUT_PATH={self.script_output_file_path}",
            config["dockerImage"],
            *script_invoker,
            script_to_invoke,
            config.get("scriptSuffix", ""),
        ]


class TestRunner:
    # successful tracks the success status of the test runs
    successful: None | bool = None

    def run_tests(self, language, input_script):
        # setup our baseline configuration
        base_directory = os.getcwd()

        # run every sort script
        for script_path in glob.glob(f"{base_directory}/src/{language}/sort_*"):
            ctx = TestRunnerContext(language, script_path)

            # if an input script was passed in, and this script is not that input script
            # then continue on to the next script
            if inputs_are_truthy_and_different(input_script, ctx.script_name):
                continue

            # if an old script output file already exists, remove it
            if os.path.isfile(ctx.script_output_file_path):
                os.remove(ctx.script_output_file_path)

            status = subprocess.call(ctx.subprocess_args)

            # check if the script invoke failed
            if status != 0:
                self.set_success_status(False)
                print(f'🔴 script "{ctx.script_relative_path}" failed, reason:')
                print(f'\t the exit code "{status}" was not 0')

            # check if the output file was created
            if not os.path.isfile(ctx.script_output_file_path):
                self.set_success_status(False)
                print(f'🔴 script "{ctx.script_relative_path}" failed, reason:')
                print(
                    f"\t the output {ctx.script_output_file_name} file was not created"
                )

            # check if the output file matches the prepared file
            if filecmp.cmp(ctx.prepared_file_path, ctx.script_output_file_path):
                self.set_success_status(True)
                print(f'🟢 script "{ctx.script_relative_path}" succeeded')
            else:
                self.set_success_status(False)
                print(f'🔴 script "{ctx.script_relative_path}" failed, reason:')
                print(
                    f"\t output file {ctx.script_output_file_name} has does not match the prepared file"
                )

    def set_success_status(self, status: bool):
        # only update the test success status if it wasnt already false
        if self.successful is not False:
            self.successful = status

    def show_results(self):
        if self.successful is True:
            print("✨ script run success ✨")
            sys.exit(0)
        else:
            print("🚨 script run failure 🚨")
            sys.exit(1)


@invoke.task
def test(_: invoke.Context, language, input_script):
    # language is the programming language to run scripts in
    # input_script is the name of a script you want to run
    runner = TestRunner()
    runner.run_tests(language, input_script)
    runner.show_results()
