import os
import sys


#####################
# sort script start #
#####################


def do_sorting(input_list):
    return sorted(input_list)


###################
# sort script end #
###################


if __name__ == "__main__":
    # read input file
    inputFilePath = os.getenv("INPUT_PATH")
    with open(inputFilePath, "r") as inputFileObject:
        inputFileData = inputFileObject.readlines()

    # clean input data
    cleanedInputData = []
    for element in inputFileData:
        cleanedInputData.append(element.strip())

    # do sorting
    sortedData = do_sorting(cleanedInputData)

    # write output file
    outputFilePath = os.getenv("OUTPUT_PATH")
    with open(outputFilePath, "w") as outputFileObject:
        for element in sortedData:
            outputFileObject.write(element + "\n")
