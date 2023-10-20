
import json


def run_sql(input_sql: list[str]) -> list[str]:
    output = {}
    lines = []

    for line in input_sql:
        if line.startswith("--"):
            continue
        lines.append(line)

    return [json.dumps(output)]

