import helpers


# pylint: disable=wrong-import-order


########################
# business logic start #
########################


import json


def run_sql(input_sql: list[str]) -> list[str]:
    output = {"table_name": ["city"]}
    return [json.dumps(output)]


######################
# business logic end #
######################

if __name__ == "__main__":
    helpers.run(run_sql)
