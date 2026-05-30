# selection sort - https://en.wikipedia.org/wiki/Selection_sort
# repeatedly pick the smallest remaining element and append it to the output

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
    # ruby `pop` DOES NOT work the same as python `pop`
    # for python `pop` in ruby, use `delete_at`
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
