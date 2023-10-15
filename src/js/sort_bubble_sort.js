var fs = require("fs");

//////////////////////////
// business logic start //
//////////////////////////

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

////////////////////////
// business logic end //
////////////////////////

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
