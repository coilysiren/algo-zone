import helpers


# pylint: disable=wrong-import-order


########################
# business logic start #
########################


import json


class SQL:
    __data: dict = {}

    def __init__(self) -> None:
        self.clear_data()

    def clear_data(self):
        self.__data = {}

    def read_data_table(self, table_name: str) -> dict:
        return self.__data.get(table_name, {})

    def read_information_schema_tables(self) -> list[dict]:
        return [data["metadata"] for data in self.__data.values()]

    def write_table_meta(self, table_name: str, data: dict):
        self.__data[table_name] = data

    def write_table_data(self, table_name: str, data: dict):
        self.__data[table_name]["data"] = data

    def create_table(self, *args, table_schema="public") -> dict:
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

        if self.read_data_table(table_name):
            self.write_table_meta(
                table_name,
                {
                    "metadata": {
                        "table_name": table_name,
                        "table_schema": table_schema,
                        "colums": columns,
                    }
                },
            )
        return {}

    create_table.sql = "CREATE TABLE"

    def insert_into(self, *args) -> dict:
        print(f"args: {args}")
        pass

    insert_into.sql = "INSERT INTO"

    def select(self, *args) -> dict:
        output = {}

        from_index = None
        where_index = None
        for i, arg in enumerate(args):
            if arg == "FROM":
                from_index = i
            if arg == "WHERE":
                where_index = i

        # get select keys by getting the slice of args before FROM
        select_keys = " ".join(args[1:from_index]).split(",")

        # get where keys by getting the slice of args after WHERE
        from_value = args[from_index + 1]

        # consider "information_schema.tables" a special case until
        # we figure out why its so different from the others
        if from_value == "information_schema.tables":
            target = self.read_information_schema_tables()
        else:
            target = self.read_data_table(from_value)

        # fmt: off
        output = {
            key: [
                value for data in target
                for key, value in data.items()
                if key in select_keys
            ]
            for key in select_keys
        }
        # fmt: on

        return output

    select.sql = "SELECT"

    sql_map = {
        create_table.sql: create_table,
        select.sql: select,
        insert_into.sql: insert_into,
    }

    def run(self, input_sql: list[str]) -> list[str]:
        output = {}

        # remove comments
        input_sql = [line.strip() for line in input_sql if not line.startswith("--")]

        # re-split on semi-colons
        input_sql = " ".join(input_sql).split(";")

        # iterate over each line of sql
        for line in input_sql:
            words = line.split(" ")
            for i in reversed(range(len(words) + 1)):
                key = " ".join(words[:i]).strip()
                # print(f'key: "{key}"')
                if func := self.sql_map.get(key):
                    # print(f'running "{func.__name__}" with {words}')
                    output = func(self, *[word for word in words if word])
                    break

        return [json.dumps(output)]


######################
# business logic end #
######################

if __name__ == "__main__":
    helpers.run(SQL().run)
