import helpers


# pylint: disable=wrong-import-order


########################
# business logic start #
########################


import json


class SQL:
    data: dict = {}

    def __init__(self) -> None:
        self.data = {}

    def information_schema_tables(self) -> list[dict]:
        return [data["metadata"] for data in self.data.values()]

    def create_table(self, *args, table_schema="public") -> dict:
        table_name = args[2]
        if not self.data.get(table_name):
            self.data[table_name] = {
                "metadata": {
                    "table_name": table_name,
                    "table_schema": table_schema,
                },
            }
        return {}

    create_table.sql = "CREATE TABLE"

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
            target = self.information_schema_tables()

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
    }

    def run(self, input_sql: list[str]) -> list[str]:
        output = {}

        for line in input_sql:
            if not line.startswith("--"):
                words = line.split(" ")
                for i in reversed(range(len(words))):
                    key = " ".join(words[:i])
                    if func := self.sql_map.get(key):
                        output = func(self, *words)
                        break

        return [json.dumps(output)]


######################
# business logic end #
######################

if __name__ == "__main__":
    helpers.run(SQL().run)
