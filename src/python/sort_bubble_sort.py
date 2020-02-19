# bubble sort!
#
# docs: https://en.wikipedia.org/wiki/Bubble_sort
#
# bubble sort steps through a list, comparing adjacent elements and swapping them if they are in the wrong order
# it passes through the list repeatedly until the list is sorted


import sys
from typing import List


###################
# read input file #
###################


inputFilePath = sys.argv[1]
with open(inputFilePath, "r") as inputFileObject:
    inputFileData = inputFileObject.readlines()


##############
# sort input #
##############


# bubble_sort is the top level function responsible for ... bubble sorting!
def bubble_sort(input_list: List[str]) -> List[str]:
    # set defaults
    output_list = []
    is_sorted = False

    # cleanup our input data
    output_list = clean_whitespace(input_list)

    # continuously do sorting rounds as long as the list remains unsorted
    while is_sorted == False:
        output_list, is_sorted = do_sorting_round(output_list)

    # mission accomplished! ✨
    return output_list


# clean_whitespace cleans up our input data
def clean_whitespace(input_list: List[str]) -> List[str]:
    # set defaults
    output_list = []

    for element in input_list:
        output_list.append(element.strip())

    return output_list


# do_sorting_round does the "actual sorting"
def do_sorting_round(input_list: List[str]) -> (List[str], bool):
    # set defaults
    output_list = []
    is_sorted = True

    for index, element in enumerate(input_list):

        # we compare (index VS index - 1) so there's
        # nothing to compare when looking at the 0th index
        if index == 0:
            output_list.append(element)
            continue

        # grab (index - 1)
        previous_element = output_list[index - 1]

        # if this element is less than the previous element then swap their order
        if element < previous_element:
            output_list.pop()
            output_list.append(element)
            output_list.append(previous_element)
            is_sorted = False
        # otherwise append
        else:
            output_list.append(element)

    return output_list, is_sorted


sortedData = bubble_sort(inputFileData)


#####################
# write output file #
#####################


outputFilePath = sys.argv[2]
with open(outputFilePath, "w") as outputFileObject:
    for element in sortedData:
        outputFileObject.write(element + "\n")
