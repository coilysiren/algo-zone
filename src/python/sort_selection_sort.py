import os
import sys
from typing import List


#####################
# sort script start #
#####################

# selection sort!
#
# docs: https://en.wikipedia.org/wiki/Selection_sort
#
# Selection sort looks through every element an input list, and finds the smallest element.
# That element is then appended to the end of an output list. Which it reaches the end
# of the input list, all of the output elements will be sorted.


def do_sorting(input_list):
    return selection_sort(input_list)


def selection_sort(input_list):
    sorted_elements = []
    unsorted_elements = input_list

    # do: iterate over the length of the unsorted_elements
    # do not: iterate over the unsorted_elements list directly
    # why:
    #   it's risky, because some languages (like python) WILL for sure
    #   stop list iteration early because of you popping an element
    #   out of the list
    for _ in range(len(unsorted_elements)):

        # print("--- for _ in unsorted_elements: ---")
        # print(f"unsorted_elements => {unsorted_elements}")
        # print(f"sorted_elements => {sorted_elements}")
        smallest_index = find_smallest_index(unsorted_elements)
        smallest_element = unsorted_elements[smallest_index]
        sorted_elements.append(smallest_element)
        unsorted_elements.pop(smallest_index)
        # print(f"smallest_index => {smallest_index}")
        # print(f"sorted_elements => {sorted_elements}")
        # print(f"unsorted_elements => {unsorted_elements}")

    return sorted_elements


def find_smallest_index(input_list):
    smallest_index = 0

    for index, element in enumerate(input_list):
        if element < input_list[smallest_index]:
            smallest_index = index

    return smallest_index


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
