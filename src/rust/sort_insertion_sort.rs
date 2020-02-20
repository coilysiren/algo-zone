use std::env;
use std::fs;
use std::fs::File;
use std::io::Write;

///////////////////////
// sort script start //
///////////////////////

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
    if index == 0 {
      output_list.push(element);
    } else if element < &output_list[index - 1] {
      let mut target_index = index;
      while &output_list[target_index] < &output_list[target_index - 1] {
        output_list.swap(target_index, target_index - 1);
        target_index = target_index - 1;
      }
    } else {
      output_list.push(element);
    }
  }

  return output_list;
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
