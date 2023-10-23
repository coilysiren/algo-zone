import helpers

########################
# business logic start #
########################


import dataclasses
import json
import os
import typing


DEBUG = bool(int(os.getenv("DEBUG", "0")))


@dataclasses.dataclass(frozen=True)
class SQLTokens:
    worker_str: str
    worker_func: typing.Callable | None
    args: list[typing.Any]


@dataclasses.dataclass(frozen=True)
class SQLTokenizer:
    sql_function_map: dict[str, typing.Callable | None]

    def tokenize_sql(self, sql: list[str]) -> list[SQLTokens]:
        # remove comments
        sql = [line.strip() for line in sql if not line.startswith("--")]
        # re-split on semi-colons, the semi-colons are the true line breaks in SQL
        sql = " ".join(sql).split(";")
        # remove empty lines
        sql = [line.strip() for line in sql if line]

        # get worker strings
        worker_strs = []
        worker_funcs = []
        args_strs = []
        for line in sql:
            this_worker_str = None
            # We sort the SQL function map by its key length, longest first.
            # This is a low complexity way to ensure that we can match, for example,
            # both `SET SESSION AUTHORIZATION` and `SET`.
            # fmt: off
            sql_function_map_ordered_keys = sorted([
                key
                for key in self.sql_function_map.keys()
            ], key=len, reverse=True)
            # fmt: on
            for key in sql_function_map_ordered_keys:
                if line.startswith(key):
                    this_worker_str = key
                    worker_strs.append(key)
                    worker_funcs.append(self.sql_function_map[key])
                    args_strs.append(line.replace(key, "").strip())
                    break
            if this_worker_str is None:
                raise ValueError(f"Unknown worker function: {this_worker_str}")

        # tokenize args
        args_list: list[list] = []
        for i, sentence in enumerate(args_strs):
            args_list.append([])
            word_start: int | None = 0
            inside_list = False
            string_start: tuple[int | None, str | None] = (None, None)
            for k, letter in enumerate(sentence):
                if (string_start[0] is None) and (letter in ["'", '"']):
                    if DEBUG:
                        print(f"at letter: {letter}, starting a string")
                    string_start = (k, letter)
                elif (word_start is None) and (letter not in ["(", ")", ",", " "]):
                    if DEBUG:
                        print(f"at letter: {letter}, starting a word")
                    word_start = k
                elif (letter == string_start[1]) and (sentence[k - 1] != "\\") and (inside_list):
                    if DEBUG:
                        print(f"at letter: {letter}, ending string: {sentence[string_start[0]:k+1]}")
                    string = sentence[string_start[0] : k + 1]
                    args_list[i][-1].append(string)
                    string_start = (None, None)
                    word_start = None
                elif (string_start[0] is not None) and (letter == string_start[1]) and (sentence[k - 1] != "\\"):
                    if DEBUG:
                        print(f"at letter: {letter}, ending string: {sentence[string_start[0]:k+1]}")
                    string = sentence[string_start[0] : k + 1]
                    args_list[i].append(string)
                    string_start = (None, None)
                    word_start = None
                elif (word_start is not None) and (letter in [")"]) and (inside_list) and (string_start[0] is None):
                    if DEBUG:
                        print(
                            f"at letter: {letter}, adding word: {sentence[word_start:k]}, to list: {args_list[i][-1]}"
                        )
                    word = sentence[word_start:k]
                    args_list[i][-1].append(word)
                    word_start = None
                    inside_list = False
                elif (
                    (word_start is not None) and (letter in [" ", ","]) and (inside_list) and (string_start[0] is None)
                ):
                    if DEBUG:
                        print(
                            f"at letter: {letter}, adding word: {sentence[word_start:k]}, to list: {args_list[i][-1]}"
                        )
                    word = sentence[word_start:k]
                    args_list[i][-1].append(word)
                    word_start = None
                elif (word_start is not None) and (letter in [" ", ")", ","]) and (string_start[0] is None):
                    if DEBUG:
                        print(f"at letter: {letter}, adding word: {sentence[word_start:k]}")
                    word = sentence[word_start:k]
                    args_list[i].append(word)
                    word_start = None
                elif (word_start is not None) and (k == len(sentence) - 1):
                    if DEBUG:
                        print(f"at letter: {letter}, last word: {sentence[word_start:]}")
                    word = sentence[word_start:]
                    args_list[i].append(word)
                    word_start = None
                elif letter == "(":
                    if DEBUG:
                        print(f"at letter: {letter}, starting a list")
                    inside_list = True
                    args_list[i].append([])
                    word_start = None
                elif (inside_list) and (letter in ")"):
                    if DEBUG:
                        print(f"at letter: {letter}, ending list")
                    inside_list = False
                elif word_start is not None:
                    if DEBUG:
                        print(f"at letter: {letter}, inside of a word: {sentence[word_start:k]}")
                else:
                    if DEBUG:
                        print(f"at letter: {letter}")

        return [
            SQLTokens(
                worker_str=worker_str,
                worker_func=worker_func,
                args=args_list,
            )
            for worker_str, worker_func, args_list in zip(worker_strs, worker_funcs, args_list)
        ]

    ######################
    # business logic end #
    ######################

    def tokenize_sql_to_json(self, sql: list[str]) -> list[str]:
        return [
            json.dumps(
                [
                    {
                        "worker": sql_tokens.worker_str,
                        "args": sql_tokens.args,
                    }
                    for sql_tokens in self.tokenize_sql(sql)
                ]
            )
        ]


if __name__ == "__main__":
    helpers.run(
        SQLTokenizer(
            {
                "CREATE TABLE": None,
                "INSERT INTO": None,
                "SELECT": None,
            }
        ).tokenize_sql_to_json
    )
