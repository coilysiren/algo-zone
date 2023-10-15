# insertion sort!
#
# docs: https://en.wikipedia.org/wiki/Insertion_sort
#
# insertion sort steps through an input list, using it to grow an output list.
# on every step, it inserts the current element into its proper location on the output list.
# it continues until the input list is empty.


def do_sorting(input_list):
    return insertion_sort(input_list)


def insertion_sort(input_list: list[str]) -> list[str]:
    output_list = []

    for index, element in enumerate(input_list):
        output_list.append(element)
        output_list = insert_element(output_list, element, index)

    return output_list


def insert_element(input_list: list[str], element: str, index: int) -> list[str]:
    output_list = input_list
    target_index = index

    while (target_index != 0) and (element < output_list[target_index - 1]):
        # swap order
        output_list[target_index], output_list[target_index - 1] = (
            output_list[target_index - 1],
            output_list[target_index],
        )
        target_index = target_index - 1

    return output_list

