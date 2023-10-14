import os


def run(func):
    # read input file
    input_file_path = os.getenv("INPUT_PATH")
    with open(input_file_path, "r", encoding="utf-8") as input_file_object:
        input_file_data = input_file_object.readlines()

    # clean input data
    cleaned_input_data = []
    for element in input_file_data:
        cleaned_input_data.append(element.strip())

    # do business logic
    output_data = func(cleaned_input_data)

    # write output file
    output_file_path = os.getenv("OUTPUT_PATH")
    with open(output_file_path, "w", encoding="utf-8") as output_file_object:
        for element in output_data:
            output_file_object.write(element + "\n")
