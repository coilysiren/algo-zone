// selection sort - https://en.wikipedia.org/wiki/Selection_sort
// repeatedly find the smallest unsorted element and append it to the output list

function doSorting(inputList) {
  return selectionSort(inputList);
}

function selectionSort(inputList) {
  sortedElements = [];
  unsortedElements = inputList;
  inputListLength = inputList.length;

  for (let index = 0; index < inputListLength; index++) {
    smallestIndex = findSmallestIndex(unsortedElements);
    smallestElement = unsortedElements[smallestIndex];
    sortedElements.push(smallestElement);
    unsortedElements.splice(smallestIndex, 1);
  }

  return sortedElements;
}

function findSmallestIndex(inputList) {
  smallestIndex = 0;

  inputList.forEach((element, index) => {
    if (element < inputList[smallestIndex]) {
      smallestIndex = index;
    }
  });

  return smallestIndex;
}
