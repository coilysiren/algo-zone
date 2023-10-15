use std::env;
use std::fs;
use std::fs::File;
use std::io::Write;

//////////////////////////
// business logic start //
//////////////////////////

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

////////////////////////
// business logic end //
////////////////////////

// 👇🏽 copy pasted helpers

fn main() -> Result<(), Box<dyn std::error::Error + 'static>> {
    // setup
    let input_file_path = env::var("INPUT_PATH").unwrap();
    let output_file_path = env::var("OUTPUT_PATH").unwrap();

    // get input data
    let input_data_string = fs::read_to_string(input_file_path)?;
    let input_data_vec = input_data_string.lines().collect();

    // do sorting
    let sorted_data = do_sorting(input_data_vec);

    // write output data
    // join on \n, and add an additional trailing \n
    let output_data_string = sorted_data.join("\n") + "\n";
    let output_data_bytes = output_data_string.as_bytes();
    let mut output_file = File::create(output_file_path)?;
    output_file.write_all(output_data_bytes)?;

    // teardown
    Ok(())
}
