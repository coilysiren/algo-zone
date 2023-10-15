# frozen_string_literal: true

########################
# business logic start #
########################

# insertion sort!
#
# docs: https://en.wikipedia.org/wiki/Insertion_sort
#
# Insertion sort steps through an input list, using it to grow an output list.
# On every step, it sorts the current element into its proper location on the
# output list. It continues until the input list is empty.

def do_sorting(input_list)
  insertion_sort(input_list)
end

def insertion_sort(input_list)
  output_list = []

  input_list.each_with_index do |element, idx|
    output_list.append(element)
    output_list = sort_element_at_index(output_list, element, idx)
  end

  output_list
end

def sort_element_at_index(input_list, element, idx)
  # puts '--- sort_element_at_index ---'
  # puts "element => #{element}"
  # puts "index => #{idx}"
  output_list = input_list
  target_index = idx

  while (target_index != 0) && (element < output_list[target_index - 1])
    output_list.swap(target_index)
    target_index -= 1
    # puts "\ttarget_index => #{target_index}"
    # puts "\toutput_list => #{output_list}"
  end

  output_list
end

# add swap method to array
class Array
  def swap(idx)
    self[idx], self[idx - 1] = self[idx - 1], self[idx]
  end
end

######################
# business logic end #
######################

# 👇🏽 copy pasted helpers

input_file_path = ENV['INPUT_PATH']
input_file = File.readlines(input_file_path)

sorted_data = do_sorting(input_file)

output_file_path = ENV['OUTPUT_PATH']
File.open(output_file_path, 'wb') { |f| f.write(sorted_data.join('')) }
