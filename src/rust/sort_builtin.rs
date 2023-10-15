use std::env;
use std::fs;
use std::fs::File;
use std::io::Write;

//////////////////////////
// business logic start //
//////////////////////////

fn do_sorting(input_list: Vec<&str>) -> Vec<&str> {
    let mut output_list = input_list;
    output_list.sort();
    return output_list;
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
