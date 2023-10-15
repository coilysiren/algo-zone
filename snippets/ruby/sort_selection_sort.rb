# selection sort!
#
# docs: https://en.wikipedia.org/wiki/Selection_sort
#
# Selection sort looks through every element an input list, and finds the
# smallest element. That element is then appended to the end of an output list.
# When it reaches the end of the input list, all of the output elements will
# be sorted.

def do_sorting(input_list)
  selection_sort(input_list)
end

def selection_sort(input_list)
  sorted_elements = []
  unsorted_elements = input_list

  (0..unsorted_elements.length).each do |_|
    # puts '--- (0..unsorted_elements.length).each do |_| ---'
    # puts "unsorted_elements #{unsorted_elements}"
    # puts "sorted_elements #{sorted_elements}"

    smallest_index = find_smallest_index(unsorted_elements)
    smallest_element = unsorted_elements[smallest_index]
    sorted_elements.append(smallest_element)
    # ruby `pop` DOES NOT work the same as python `pop`
    # for python `pop` in ruby, use `delete_at`
    unsorted_elements.delete_at(smallest_index)

    # puts "smallest_index #{smallest_index}"
    # puts "smallest_element #{smallest_element}"
    # puts "unsorted_elements #{unsorted_elements}"
    # puts "sorted_elements #{sorted_elements}"
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
