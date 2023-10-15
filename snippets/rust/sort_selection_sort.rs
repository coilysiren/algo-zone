// selection sort!
//
// docs: https://en.wikipedia.org/wiki/Selection_sort
//
// Selection sort looks through every element an input list, and finds the smallest element.
// That element is then appended to the end of an output list. Which it reaches the end
// of the input list, all of the output elements will be sorted.

fn do_sorting(input_list: Vec<&str>) -> Vec<&str> {
    return selection_sort(input_list);
}

fn selection_sort(input_list: Vec<&str>) -> Vec<&str> {
    let mut sorted_elements: Vec<&str> = vec![];
    let mut unsorted_elements: Vec<&str> = input_list;

    for _ in 0..unsorted_elements.len() {
        let smallest_index = find_smallest_index(&unsorted_elements);
        let smallest_element = unsorted_elements[smallest_index];
        sorted_elements.push(smallest_element);
        unsorted_elements.remove(smallest_index);
    }

    return sorted_elements;
}

fn find_smallest_index(input_list: &Vec<&str>) -> usize {
    let mut smallest_index: usize = 0;

    for (index, element) in input_list.iter().enumerate() {
        if element < &input_list[smallest_index] {
            smallest_index = index;
        }
    }

    return smallest_index;
}
