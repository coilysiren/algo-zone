import os
import sys
from typing import List


#####################
# sort script start #
#####################


# insertion sort!
#
# docs: https://en.wikipedia.org/wiki/Insertion_sort
#
# insertion sort steps through an input list, using it to grow an output list.
# on every step, it inserts the current element into its proper location on the output list.
# it continues until the input list is empty.


def do_sorting(input_list):
    return insertion_sort(input_list)


def insertion_sort(input_list: List[str]) -> List[str]:
    output_list = []

    for index, element in enumerate(input_list):
        output_list.append(element)
        target_index = index
        while (target_index != 0) and (element < output_list[index - 1]):
            # swap order
            output_list[target_index], output_list[target_index - 1] = (
                output_list[target_index - 1],
                output_list[target_index],
            )
            target_index = target_index - 1

    return output_list


###################
# sort script end #
###################

# 👇🏽 copy pasted helpers

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
