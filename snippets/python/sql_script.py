
import dataclasses
import json
import re
import typing

import tokenizer_script


@dataclasses.dataclass(frozen=True)
class SQLState:
    state: dict

    def read_table_meta(self, table_name: str) -> dict:
        return self.state.get(table_name, {}).get("metadata", {})

    def read_table_rows(self, table_name: str) -> list[dict]:
        return self.state.get(table_name, {}).get("rows", [])

    def read_information_schema(self) -> list[dict]:
        return [data["metadata"] for data in self.state.values()]

    def write_table_meta(self, table_name: str, data: dict):
        state = self.state
        table = state.get(table_name, {})
        metadata = table.get("metadata", {})
        metadata.update(data)
        table["metadata"] = metadata
        state[table_name] = table
        return self.__class__(state)

    def write_table_rows(self, table_name: str, data: dict):
        state = self.state
        table = state.get(table_name, {})
        rows = table.get("rows", [])
        rows.append(data)
        table["rows"] = rows
        state[table_name] = table
        return self.__class__(state)


class SQLType:
    @staticmethod
    def varchar(data) -> str:
        data_str = str(data).strip()
        data_str = re.sub(r'^["\']', "", data_str)  # leading ' or "
        data_str = re.sub(r'["\']$', "", data_str)  # trailing ' or "
        return data_str

    @staticmethod
    def int(data) -> int:
        return int(data.strip())


class SQLFunctions:
    @staticmethod
    def create_table(state: SQLState, *args, table_schema="public") -> typing.Tuple[list, SQLState]:
        output: list[dict] = []
        table_name = args[0]

        # get columns
        columns = {}
        columns_str = args[1]
        if columns_str:
            # fmt: off
            columns = {
                columns_str[i]: columns_str[i + 1]
                for i in range(0, len(columns_str), 2)
            }
            # fmt: on

        if not state.read_table_meta(table_name):
            state = state.write_table_meta(
                table_name,
                {
                    "table_name": table_name,
                    "table_schema": table_schema,
                    "colums": columns,
                },
            )
        return (output, state)

    @staticmethod
    def insert_into(state: SQLState, *args) -> typing.Tuple[list, SQLState]:
        output: list[dict] = []
        table_name = args[0]
        keys = args[1]
        values = args[3]
        key_value_map = dict(zip(keys, values))

        sql_type_map = {
            "VARCHAR": SQLType.varchar,
            "INT": SQLType.int,
        }

        data = {}
        metadata = state.read_table_meta(table_name)
        if metadata:
            for key, value in key_value_map.items():
                data[key] = sql_type_map[metadata["colums"][key]](value)
            state = state.write_table_rows(table_name, data)

        return (output, state)

    @staticmethod
    def select(state: SQLState, *args) -> typing.Tuple[list, SQLState]:
        output: list[dict] = []
        select_columns = args[0] if isinstance(args[0], list) else [args[0]]
        from_value = args[2]

        # `information_schema.tables` is a special case
        if from_value == "information_schema.tables":
            data = state.read_information_schema()
        else:
            data = state.read_table_rows(from_value)

        output = []
        for datum in data:
            # fmt: off
            output.append({
                key: datum.get(key)
                for key in select_columns
            })
            # fmt: on

        return (output, state)


def run_sql(input_sql: list[str]) -> list[str]:
    output = []
    state = SQLState(state={})
    sql_tokenizer = tokenizer_script.SQLTokenizer(
        {
            "CREATE TABLE": SQLFunctions.create_table,
            "INSERT INTO": SQLFunctions.insert_into,
            "SELECT": SQLFunctions.select,
        }
    )
    sql_token_list = sql_tokenizer.tokenize_sql(input_sql)

    # iterate over each line of sql
    for sql_tokens in sql_token_list:
        output, state = sql_tokens.worker_func(state, *sql_tokens.args)

    return [json.dumps(output)]

