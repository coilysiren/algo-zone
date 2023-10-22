import helpers


# pylint: disable=wrong-import-order


########################
# business logic start #
########################


import dataclasses
import json
import typing


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
        if data_str.startswith("'") or data_str.startswith('"'):
            data_str = data_str[1:]
        if data_str.endswith("'") or data_str.endswith('"'):
            data_str = data_str[:-1]
        return data_str

    @staticmethod
    def int(data) -> int:
        return int(data.strip())


sql_type_map = {
    "VARCHAR": SQLType.varchar,
    "INT": SQLType.int,
}


class SQLFunctions:
    @staticmethod
    def create_table(state: SQLState, *args, table_schema="public") -> typing.Tuple[list, SQLState]:
        output: list[dict] = []
        table_name = args[2]

        # get columns
        columns = {}
        columns_str = " ".join(args[3:]).replace("(", "").replace(")", "").strip()
        if columns_str:
            # fmt: off
            columns = {
                column.strip().split(" ")[0]: column.strip().split(" ")[1]
                for column in columns_str.split(",")
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
        table_name = args[2]

        values_index = None
        for i, arg in enumerate(args):
            if arg == "VALUES":
                values_index = i
        if values_index is None:
            raise ValueError("VALUES not found")

        keys = " ".join(args[3:values_index]).replace("(", "").replace(")", "").split(",")
        keys = [key.strip() for key in keys]
        values = " ".join(args[values_index + 1 :]).replace("(", "").replace(")", "").split(",")
        values = [value.strip() for value in values]
        key_value_map = dict(zip(keys, values))

        data = {}
        if metadata := state.read_table_meta(table_name):
            for key, value in key_value_map.items():
                data[key] = sql_type_map[metadata["colums"][key]](value)
            state = state.write_table_rows(table_name, data)

        return (output, state)

    @staticmethod
    def select(state: SQLState, *args) -> typing.Tuple[list, SQLState]:
        output: list[dict] = []

        from_index = None
        where_index = None
        for i, arg in enumerate(args):
            if arg == "FROM":
                from_index = i
            if arg == "WHERE":
                where_index = i
        if from_index is None:
            raise ValueError("FROM not found")

        # get select keys by getting the slice of args before FROM
        select_keys = " ".join(args[1:from_index]).split(",")
        select_keys = [key.strip() for key in select_keys]

        # get where keys by getting the slice of args after WHERE
        from_value = args[from_index + 1]

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
                for key in select_keys
            })
            # fmt: on

        return (output, state)


sql_function_map: dict[str, typing.Callable] = {
    "CREATE TABLE": SQLFunctions.create_table,
    "SELECT": SQLFunctions.select,
    "INSERT INTO": SQLFunctions.insert_into,
}


def run_sql(input_sql: list[str]) -> list[str]:
    output = []
    state = SQLState(state={})

    # remove comments
    input_sql = [line.strip() for line in input_sql if not line.startswith("--")]

    # re-split on semi-colons
    input_sql = " ".join(input_sql).split(";")

    # iterate over each line of sql
    for line in input_sql:
        words = line.split(" ")
        for i in reversed(range(len(words) + 1)):
            key = " ".join(words[:i]).strip()
            if func := sql_function_map.get(key):
                output, state = func(state, *[word for word in words if word])
                break

    return [json.dumps(output)]


######################
# business logic end #
######################

if __name__ == "__main__":
    helpers.run(run_sql)
