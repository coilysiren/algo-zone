// insertion sort!
//
// docs: https://en.wikipedia.org/wiki/Insertion_sort
//
// Insertion sort steps through an input list, using it to grow an output list.
// On every step, it sorts the current element into its proper location on the
// output list.It continues until the input list is empty.

function doSorting(inputList) {
  return insertionSort(inputList);
}

function insertionSort(inputList) {
  outputList = [];

  inputList.forEach((element, idx) => {
    outputList.push(element);
    outputList = sortElementAtIndex(outputList, element, idx);
  });

  return outputList;
}

function sortElementAtIndex(inputList, element, idx) {
  target_index = idx;
  outputList = inputList;

  while (target_index != 0 && element < outputList[target_index - 1]) {
    swapWithPrevious(outputList, target_index);
    target_index -= 1;
  }

  return outputList;
}

function swapWithPrevious(list, idx) {
  tmp = list[idx - 1];
  list[idx - 1] = list[idx];
  list[idx] = tmp;
  return list;
