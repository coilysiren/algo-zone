var fs = require('fs');

///////////////////////
// sort script start //
///////////////////////

// selection sort!
//
// docs: https://en.wikipedia.org/wiki/Selection_sort
//
// Selection sort looks through every element an input list, and finds the
// smallest element. That element is then appended to the end of an output list.
// When it reaches the end of the input list, all of the output elements will
// be sorted.

function doSorting(inputList) {
  return selectionSort(inputList);
}

function selectionSort(inputList) {
  sortedElements = [];
  unsortedElements = inputList;
  inputListLength = inputList.length;

  for (let index = 0; index < inputListLength; index++) {
    // console.log("--- for (let index = 0; index < inputList.length; index++) { ---");
    // console.log("unsortedElements => " + unsortedElements);
    // console.log("sortedElements => " + sortedElements);

    smallestIndex = findSmallestIndex(unsortedElements);
    smallestElement = unsortedElements[smallestIndex];
    sortedElements.push(smallestElement);
    unsortedElements.splice(smallestIndex, 1);

    // console.log("smallestIndex => " + smallestIndex);
    // console.log("smallestElement => " + smallestElement);
    // console.log("unsortedElements => " + unsortedElements);
    // console.log("sortedElements => " + sortedElements);
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

/////////////////////
// sort script end //
/////////////////////

// 👇🏽 copy pasted helpers

// read input file
let inputFilePath = process.env.INPUT_PATH;
let inputString = fs.readFileSync(inputFilePath, 'utf8');
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
