def do_sorting(input_list)
  bubble_sort(input_list)
end

def bubble_sort(input_list)
  output_list = input_list
  is_sorted = false

  while is_sorted == false
    output_list, is_sorted = do_sorting_round(output_list)
  end

  output_list
end

def do_sorting_round(input_list)
  output_list = []
  is_sorted = true

  input_list.each_with_index do |element, index|
    if index.zero?
      output_list.append(element)
    elsif element < output_list[index - 1]
      previous_element = output_list[index - 1]
      output_list.pop
      output_list.append(element)
      output_list.append(previous_element)
      is_sorted = false
    else
      output_list.append(element)
    end
  end

  [output_list, is_sorted]
end
