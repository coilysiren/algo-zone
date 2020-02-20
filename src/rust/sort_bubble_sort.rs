use std::env;
use std::fs;
use std::fs::File;
use std::io::Write;

///////////////////////
// sort script start //
///////////////////////

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

/////////////////////
// sort script end //
/////////////////////

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
