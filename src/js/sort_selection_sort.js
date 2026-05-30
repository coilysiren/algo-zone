var fs = require("fs");

// business logic start //

// selection sort - repeatedly pick the smallest remaining element into the output
// https://en.wikipedia.org/wiki/Selection_sort

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
