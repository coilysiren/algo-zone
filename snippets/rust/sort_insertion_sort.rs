// insertion sort!
//
// docs: https://en.wikipedia.org/wiki/Insertion_sort
//
// insertion sort steps through an input list, using it to grow an output list.
// on every step, it inserts the current element into its proper location on the output list.
// it continues until the input list is empty.

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
