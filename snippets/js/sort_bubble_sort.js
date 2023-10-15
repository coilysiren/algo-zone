function doSorting(inputList) {
  return bubbleSort(inputList);
}

function bubbleSort(inputList) {
  outputList = inputList;
  isSorted = false;

  while (isSorted === false) {
    outputList, (isSorted = doSortingRound(outputList));
  }

  return outputList;
}

function doSortingRound(inputList) {
  outputList = [];
  isSorted = true;

  inputList.forEach((element, index) => {
    if (index === 0) {
      outputList.push(element);
    } else if (element < outputList[index - 1]) {
      previousElement = outputList[index - 1];
      outputList.pop();
      outputList.push(element);
      outputList.push(previousElement);
      isSorted = false;
    } else {
      outputList.push(element);
    }
  });

  return outputList, isSorted;
}
