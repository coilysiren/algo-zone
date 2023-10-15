# bubble sort!
#
# docs: https://en.wikipedia.org/wiki/Bubble_sort
#
# bubble sort steps through a list, comparing adjacent elements and swapping them if they
# are in the wrong order. it passes through the list repeatedly until the list is sorted


def do_sorting(input_list):
    return bubble_sort(input_list)


# bubble_sort is the top level function responsible for ... bubble sorting!
def bubble_sort(input_list: list[str]) -> list[str]:
    # set defaults
    output_list = input_list
    is_sorted = False

    # continuously do sorting rounds as long as the list remains unsorted
    while is_sorted is False:
        output_list, is_sorted = do_sorting_round(output_list)

    # mission accomplished! ✨
    return output_list


# do_sorting_round does the "actual sorting"
def do_sorting_round(input_list: list[str]) -> (list[str], bool):
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
