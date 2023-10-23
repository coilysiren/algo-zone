# builtin packages
import unittest
import filecmp
import glob
import os
import sys
import dataclasses
import json
import time
import traceback

# 3rd party packages
import yaml
import invoke


def inputs_are_truthy_and_different(first, second):
    # check if inputs are truthy
    if (not first) or (not second):
        return False
    # allow for wildcard matching
    wildcard_keyword = "any"
    if (first == wildcard_keyword) or (second == wildcard_keyword):
        return False
    # check if inputs are different
    if first != second:
        return True
    return False


def clean_string(inp):
    """remove unwanted characters from a string"""
    if inp:
        inp = inp.lower().strip()
        for element in ["-", "_", "test", "script", "sort"]:
            inp = inp.replace(element, "")
    return inp


@dataclasses.dataclass
class TestRunnerContext:
    language: str
    script_name: str
    docker_pull: str
    docker_run_test: str
    script_type: str
    script_relative_path: str
    script_name_with_file_type: str
    script_output_file_path: str
    script_output_file_name: str
    input_file_path: str
    prepared_file_path: str
    prepared_file_type: str
    snippet_start_line: int
    snippet_end_line: int

    @property
    def data(self):
        return vars(self)


class TestRunnerContexts:
    base_directory = os.getcwd()
    data_folder_path = "./data"
    debug = False
    ctxs: list[TestRunnerContext] = []
    # We use these strings to mark the start and end of the important part of our scripts
    snippet_start_text = "business logic start"
    snippet_end_text = "business logic end"

    def __init__(self, language, input_data_index, debug=False) -> None:
        self.debug = debug

        # get the language specific config
        with open(f"{self.base_directory}/config.yml", "r", encoding="utf-8") as obj:
            data = obj.read()
            config_yaml = yaml.safe_load(data)
            config = config_yaml[language]

        # generate the contexts
        self.ctxs = []
        for script_path in glob.glob(f"{self.base_directory}/src/{language}/*"):
            # given "src/python/sort_builtin.py" => return "sort"
            script_type = script_path.split("/")[-1].split("_")[0]

            # ignore helpers, metadata files, etc
            if config.get("ignoreFiles") and script_path.split("/")[-1] in config.get("ignoreFiles"):
                continue

            # ignore directories, generally compiled code
            if not os.path.isfile(script_path):
                continue

            for input_file_path in glob.glob(f"{self.data_folder_path}/{script_type}_input_*"):
                # given "data/sort_input_1.txt" => return "1"
                input_file_index = input_file_path.split("_")[-1].split(".")[0]

                # skip this input file if it's not the one we want to run
                if inputs_are_truthy_and_different(
                    clean_string(input_file_index),
                    clean_string(input_data_index),
                ):
                    continue

                # generate a context for this particular script
                if ctx := self.generate(language, config, script_path, input_file_path):
                    self.ctxs.append(ctx)

    @property
    def data(self):
        return [ctx.data for ctx in self.ctxs]

    def generate(self, language, config, script_path, input_file_path):
        # given "src/python/sort_builtin.py" => split on "/" and return "sort_builtin.py"
        script_path_split_on_slash = script_path.split("/")
        script_name_with_file_type = script_path_split_on_slash[-1]

        # given "sort_builtin.py" => split on "." and return "sort_builtin"
        script_name_split_on_dot = script_name_with_file_type.split(".")
        script_name = script_name_split_on_dot[0]

        # given "sort_builtin" => return "sort"
        script_type = script_name.split("_")[0]

        # this path is used in various places later
        script_relative_path = f"./src/{language}/{script_name_with_file_type}"

        # given "./data/sql_input_1.txt" => return "data/sql_output_1"
        partial_output_file_path = "." + input_file_path.replace("input", "output").split(".")[1]

        # get the actual output file path
        potentional_output_file_paths = glob.glob(f"{partial_output_file_path}.*")
        if len(potentional_output_file_paths) == 0:
            raise Exception(f"could not find output file for input file {input_file_path}")
        if len(potentional_output_file_paths) > 1:
            raise Exception(
                f"Found multiple output files for a single input file: {potentional_output_file_paths}. "
                f"The input file was {input_file_path}."
            )
        prepared_file_path = potentional_output_file_paths[0]

        # given "data/sort_input_1.txt" => return "1"
        prepared_file_index = prepared_file_path.split("_")[-1].split(".")[0]

        # given "data/sql_output_0.json" => return "json"
        prepared_file_type = prepared_file_path.split(".")[-1]

        # our scripts write their output files to this path
        script_output_file_name = f"output_{language}_{script_name}_{prepared_file_index}.{prepared_file_type}"
        script_output_file_path = f"{self.data_folder_path}/{script_output_file_name}"

        # script_invoker is command that we run in a subprocess to invoke our script
        # it needs to be split on spaces since subprocess.call excepts a list as input
        # whenever we aren't using the shell=True arguement
        script_invoker = config["scriptInvoker"].split(" ")

        # script_to_invoke is the literal script name that we pass to the invoker
        # we assume that invokers accept paths by default (eg. script_path)
        # and that other invokers want script names (eg. script_name)
        # the useShortScriptName config value controls this behavior
        if config.get("useShortScriptName", False) is False:
            script_to_invoke = script_relative_path
        else:
            script_to_invoke = script_name

        # construction initial call args
        docker_run_test_list = [
            "docker",
            "run",
            "--rm",
            f"--name={language}",
            f"--volume={self.base_directory}:/workdir",
            "-w=/workdir",
        ]

        # construct env vars CLI args
        if env_vars := config.get("env_vars"):
            docker_run_test_list.append(f"-e={env_vars}")

        # construct ending call args
        docker_run_test_list += [
            f"-e=DEBUG={1 if self.debug else 0}",
            f"-e=INPUT_PATH={input_file_path}",
            f"-e=OUTPUT_PATH={script_output_file_path}",
            config["dockerImage"],
            *script_invoker,
            script_to_invoke,
            config.get("scriptSuffix", ""),
        ]
        docker_run_test = " ".join(docker_run_test_list)

        # construct docker pull command
        docker_pull = f"docker pull --quiet {config['dockerImage']}"

        # get the script contents
        with open(script_relative_path, "r", encoding="utf-8") as obj:
            script_contents = obj.readlines()

        # find the start and end lines of the script
        # the start line is the location of the start text, plus 3 lines
        # the end line is the location of the end text, minus 3 lines
        snippet_start_line = 0
        snippet_start_line_offset = 3
        snippet_end_line = 0
        snippet_end_line_offset = 2
        for idx, line in enumerate(script_contents):
            if self.snippet_start_text in line:
                if snippet_start_line != 0:
                    raise Exception(
                        f'Found multiple "{self.snippet_start_text}" lines in {script_relative_path}.\n'
                        f"The lines were {snippet_start_line - snippet_start_line_offset + 1} and {idx + 1}."
                    )
                snippet_start_line = idx + 3
            if self.snippet_end_text in line:
                if snippet_end_line != 0:
                    raise Exception(
                        f'Found multiple "{self.snippet_end_text}" lines in {script_relative_path}.\n'
                        f"The lines were {snippet_end_line + snippet_end_line_offset + 1} and {idx + 1}."
                    )
                snippet_end_line = idx - snippet_end_line_offset
        if snippet_start_line == 0:
            raise Exception(f'could not find the text "{self.snippet_start_text}" in {script_relative_path}')
        if snippet_end_line == 0:
            raise Exception(f'could not find the text "{self.snippet_end_text}" in {script_relative_path}')

        # return the fully constructed context
        return TestRunnerContext(
            language=language,
            script_name=script_name,
            docker_pull=docker_pull,
            docker_run_test=docker_run_test,
            script_type=script_type,
            script_relative_path=script_relative_path,
            script_name_with_file_type=script_name_with_file_type,
            script_output_file_path=script_output_file_path,
            script_output_file_name=script_output_file_name,
            input_file_path=input_file_path,
            prepared_file_path=prepared_file_path,
            prepared_file_type=prepared_file_type,
            snippet_start_line=snippet_start_line,
            snippet_end_line=snippet_end_line,
        )


class TestRunner:
    # __successful tracks the success status of the test runs
    __successful: None | bool = None
    invoke: invoke.Context
    ctxs: TestRunnerContexts

    def __init__(self, _invoke, language, input_data_index, debug=False) -> None:
        self.invoke = _invoke
        self.ctxs = TestRunnerContexts(language, input_data_index, debug=debug)

    def run_tests(self, input_script):
        # run every test
        for ctx in self.ctxs.ctxs:
            try:
                # determine if we this is one if the scripts we want to run
                if inputs_are_truthy_and_different(
                    clean_string(input_script),
                    clean_string(ctx.script_name),
                ):
                    continue

                # if an old script output file already exists, remove it
                if os.path.isfile(ctx.script_output_file_path):
                    os.remove(ctx.script_output_file_path)

                # Pull the docker image if we are in CI.
                # We only do this in CI it helps with getting consistent timing in that context.
                # When running locally, you get consistent timing by running the script twice.
                if os.getenv("CI"):
                    self.invoke.run(ctx.docker_pull, echo=True, pty=True)

                # run the script
                start_time = time.time()
                print(f"docker run ... {ctx.language} {ctx.script_relative_path}")
                output = self.invoke.run(ctx.docker_run_test, echo=False, pty=True)
                end_time = time.time()

                # report timing
                # we round the number so humans dont over-index on small differences
                print(
                    f"\t⏱  {ctx.script_relative_path} on {ctx.input_file_path} "
                    f"ran for {round(end_time - start_time, 2)} seconds"
                )

                # check if the script invoke failed
                if output.exited != 0:
                    self.set_success_status(False)
                    print(f"\t🔴 {ctx.script_relative_path} on {ctx.input_file_path} failed, reason:")
                    print(f'\t\t the exit code "{output.exited}" was not 0')

                # check if the output file was created
                if not os.path.exists(ctx.script_output_file_path):
                    self.set_success_status(False)
                    print(f"\t🔴 {ctx.script_relative_path} on {ctx.input_file_path} failed, reason:")
                    print(f"\t\t the output {ctx.script_output_file_name} file was not created")
                    continue

                # check if the output file matches the prepared file, when both files are json
                if ctx.prepared_file_type == "json":
                    with open(ctx.prepared_file_path, "r", encoding="utf-8") as reader:
                        prepared_file_data = json.load(reader)
                    with open(ctx.script_output_file_path, "r", encoding="utf-8") as reader:
                        script_output_file_data = json.load(reader)
                    unittest.TestCase().assertListEqual(prepared_file_data, script_output_file_data)
                    self.set_success_status(True)
                    print(f"\t🟢 {ctx.script_relative_path} on {ctx.input_file_path} succeeded")
                    continue

                # check if the output file matches the prepared file
                if filecmp.cmp(ctx.prepared_file_path, ctx.script_output_file_path):
                    self.set_success_status(True)
                    print(f"\t🟢 {ctx.script_relative_path} on {ctx.input_file_path} succeeded")
                else:
                    self.set_success_status(False)
                    print(f"\t🔴 {ctx.script_relative_path} on {ctx.input_file_path} failed, reason:")
                    print(f"\t\t output file {ctx.script_output_file_name} has does not match the prepared file")

            # catch any errors, mark the test as failed, and continue
            except Exception as exc:
                print(self.error_context(ctx.data, exc))
                self.set_success_status(False)

    def generate_snippets(self, input_script):
        # run every test
        for ctx in self.ctxs.ctxs:
            try:
                # determine if we this is one if the scripts we want to run
                if inputs_are_truthy_and_different(
                    clean_string(input_script),
                    clean_string(ctx.script_name),
                ):
                    continue

                # read the snippet
                os.makedirs(f"snippets/{ctx.language}", exist_ok=True)
                with open(
                    ctx.script_relative_path,
                    "r",
                    encoding="utf-8",
                ) as reader:
                    snippet = reader.readlines()[ctx.snippet_start_line : ctx.snippet_end_line]

                # write the snippet
                with open(
                    f"snippets/{ctx.language}/{ctx.script_name_with_file_type}",
                    "w",
                    encoding="utf-8",
                ) as writer:
                    writer.writelines(snippet)

                # check if there are unsaved changes on the snippet
                self.invoke.run("git add snippets")
                output = self.invoke.run(
                    f"git diff --cached --exit-code snippets/{ctx.language}/{ctx.script_name_with_file_type}",
                    warn=True,
                )

                # Check if there are unsaved changes on the snippets.
                if output.exited != 0:
                    self.set_success_status(False)
                    print(f"🔴 snippets/{ctx.language}/{ctx.script_name_with_file_type} has uncommitted changes")

            # catch any errors, mark the test as failed, and continue
            except Exception as exc:
                print(self.error_context(ctx.data, exc))
                self.set_success_status(False)

    def error_context(self, data: dict, exc: Exception) -> str:
        return "\n" + "\n".join(
            [
                "TestRunnerContext:",
                json.dumps(data, indent=4),
                "".join(traceback.format_exception(None, exc, exc.__traceback__)),
            ]
        )

    def set_success_status(self, status: bool):
        # Only update the test success status if it wasnt already false.
        # This function is useless if the test has already failed.
        # It's here to make sure you don't accidentally mark a test as successful
        # when it has already failed.
        if self.__successful is not False:
            self.__successful = status

    def show_results(self):
        if self.__successful is True:
            print("\n✨ script run success ✨")
            sys.exit(0)
        else:
            print("\n🚨 script run failure 🚨")
            sys.exit(1)


@invoke.task
def test(ctx: invoke.Context, language, input_script, input_data_index, snippets=False, debug=False):
    # language is the programming language to run scripts in
    # input_script is the name of a script you want to run
    runner = TestRunner(ctx, language, input_data_index, debug=debug)
    runner.run_tests(input_script)
    if snippets:
        runner.generate_snippets(input_script)
    runner.show_results()


@invoke.task
def clean(ctx: invoke.Context):
    ctx.run("git clean -fdx ./data/output_*")
