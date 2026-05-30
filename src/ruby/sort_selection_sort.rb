# frozen_string_literal: true

# business logic start #

# selection sort - https://en.wikipedia.org/wiki/Selection_sort
# Repeatedly find the smallest unsorted element and append it to the output list.

def do_sorting(input_list)
  selection_sort(input_list)
end

def selection_sort(input_list)
  sorted_elements = []
  unsorted_elements = input_list

  (0..unsorted_elements.length).each do |_|
    smallest_index = find_smallest_index(unsorted_elements)
    smallest_element = unsorted_elements[smallest_index]
    sorted_elements.append(smallest_element)
    # ruby `delete_at` is the equivalent of python `pop` (ruby `pop` differs)
    unsorted_elements.delete_at(smallest_index)
  end

  sorted_elements
end

def find_smallest_index(input_list)
  smallest_index = 0

  input_list.each_with_index do |element, index|
    smallest_index = index if element < input_list[smallest_index]
  end

  smallest_index
end

# business logic end #

if __FILE__ == $PROGRAM_NAME
  input_file_path = ENV['INPUT_PATH']
  input_file = File.readlines(input_file_path)

  sorted_data = do_sorting(input_file)

  output_file_path = ENV['OUTPUT_PATH']
  File.open(output_file_path, 'wb') { |f| f.write(sorted_data.join('')) }
end
