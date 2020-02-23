# frozen_string_literal: true

#####################
# sort script start #
#####################

# insertion sort!
#
# docs: https://en.wikipedia.org/wiki/Insertion_sort
#
# insertion sort steps through an input list, using it to grow an output list.
# on every step, it inserts the current element into its proper location on the
# output list. it continues until the input list is empty.

def do_sorting(input_list)
  insertion_sort(input_list)
end

def insertion_sort(input_list)
  output_list = []

  input_list.each_with_index do |element, index|
    output_list.append(element)
    output_list = sort_element_at_index(output_list, element, index)
  end

  output_list
end

def sort_element_at_index(input_list, element, index)
  output_list = input_list
  target_index = index

  while (target_index != 0) && (element < output_list[target_index - 1])
    # swap
    output_list[target_index], output_list[target_index - 1] = \
      output_list[target_index - 1], output_list[target_index]
    target_index -= target_index
  end

  output_list
end

###################
# sort script end #
###################

# 👇🏽 copy pasted helpers

input_file_path = ENV['INPUT_PATH']
input_file = File.readlines(input_file_path)

sorted_data = do_sorting(input_file)

output_file_path = ENV['OUTPUT_PATH']
File.open(output_file_path, 'wb') { |f| f.write(sorted_data.join('')) }