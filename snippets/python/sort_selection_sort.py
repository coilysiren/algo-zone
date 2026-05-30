# selection sort - https://en.wikipedia.org/wiki/Selection_sort
# repeatedly find the smallest unsorted element and append it to the sorted output


def do_sorting(input_list):
    return selection_sort(input_list)


def selection_sort(input_list):
    sorted_elements = []
    unsorted_elements = input_list

    # iterate by length, not over the list: popping during iteration ends it early
    # in some languages (python included)
    for _ in range(len(unsorted_elements)):
        smallest_index = find_smallest_index(unsorted_elements)
        smallest_element = unsorted_elements[smallest_index]
        sorted_elements.append(smallest_element)
        unsorted_elements.pop(smallest_index)

    return sorted_elements


def find_smallest_index(input_list):
    smallest_index = 0

    for index, element in enumerate(input_list):
        if element < input_list[smallest_index]:
            smallest_index = index

    return smallest_index

