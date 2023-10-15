fn do_sorting(input_list: Vec<&str>) -> Vec<&str> {
    return bubble_sort(input_list);
}

fn bubble_sort(input_list: Vec<&str>) -> Vec<&str> {
    let mut output_list = input_list;
    let mut is_sorted = false;

    while is_sorted == false {
        let (_output_list, _is_sorted) = do_sorting_round(output_list);
        output_list = _output_list;
        is_sorted = _is_sorted;
    }

    return output_list;
}

fn do_sorting_round(input_list: Vec<&str>) -> (Vec<&str>, bool) {
    let mut output_list: Vec<&str> = vec![];
    let mut is_sorted = true;

    for (index, element) in input_list.iter().enumerate() {
        if index == 0 {
            output_list.push(element);
        } else if element < &output_list[index - 1] {
            let previous_element = output_list[index - 1];
            output_list.pop();
            output_list.push(element);
            output_list.push(previous_element);
            is_sorted = false
        } else {
            output_list.push(element);
        }
    }

    return (output_list, is_sorted);
}
