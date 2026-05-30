import helpers


# business logic start #

# selection sort - https://en.wikipedia.org/wiki/Selection_sort
# repeatedly pick the smallest remaining element and append it to the output list


def do_sorting(input_list):
    return selection_sort(input_list)


def selection_sort(input_list):
    sorted_elements = []
    unsorted_elements = input_list

    # iterate over the length, not the list itself: popping while iterating directly
    # makes some languages (python included) end the loop early
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


# business logic end #

if __name__ == "__main__":
    helpers.run(do_sorting)
