# insertion sort - https://en.wikipedia.org/wiki/Insertion_sort
# steps through the input, inserting each element into its place in the output list

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
  output_list = input_list
  target_index = idx

  while (target_index != 0) && (element < output_list[target_index - 1])
    output_list.swap(target_index)
    target_index -= 1
  end

  output_list
end

# add swap method to array
class Array
  def swap(idx)
    self[idx], self[idx - 1] = self[idx - 1], self[idx]
  end
end
