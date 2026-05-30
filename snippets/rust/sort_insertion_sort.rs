// insertion sort - https://en.wikipedia.org/wiki/Insertion_sort
// steps through the input, inserting each element into place in a growing output list.

fn do_sorting(input_list: Vec<&str>) -> Vec<&str> {
    return insertion_sort(input_list);
}

fn insertion_sort(input_list: Vec<&str>) -> Vec<&str> {
    let mut output_list: Vec<&str> = vec![];

    for (index, element) in input_list.iter().enumerate() {
        output_list.push(element);
        if index != 0 && element < &output_list[index - 1] {
            let mut target_index = index;
            while target_index != 0 && element < &output_list[target_index - 1] {
                output_list.swap(target_index, target_index - 1);
                target_index = target_index - 1;
            }
        }
    }

    return output_list;
}
