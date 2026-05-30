var fs = require("fs");

// business logic start //

// insertion sort - https://en.wikipedia.org/wiki/Insertion_sort
// Steps through the input, growing a sorted output by inserting each element in place.

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
}

// business logic end //

// 👇🏽 copy pasted helpers

// read input file
let inputFilePath = process.env.INPUT_PATH;
let inputString = fs.readFileSync(inputFilePath, "utf8");
let inputStringSplit = inputString.split(/\n/);

// clean input data
if (inputStringSplit[inputStringSplit.length - 1] === "") {
  inputStringSplit = inputStringSplit.slice(0, inputStringSplit.length - 1);
}

// do sorting
sortedData = doSorting(inputStringSplit);

// write output file
let outputFilePath = process.env.OUTPUT_PATH;
let outputString = sortedData.join("\n");
outputString += "\n"; // trailing newline
fs.writeFileSync(outputFilePath, outputString);
