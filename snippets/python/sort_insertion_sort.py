# insertion sort - https://en.wikipedia.org/wiki/Insertion_sort
# steps through the input, inserting each element into its place in a growing output list.


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

