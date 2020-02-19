var fs = require('fs');

/////////////////////
// read input file //
/////////////////////

let inputFilePath = process.env.INPUT_PATH;
let inputString = fs.readFileSync(inputFilePath, 'utf8');
let inputStringSplit = inputString.split(/\n/);

////////////////
// sort input //
////////////////

// drop the trailing newline, so that it doesn't get included in the sort
if (inputStringSplit[inputStringSplit.length - 1] == "") {
  inputStringSplit = inputStringSplit.slice(0, inputStringSplit.length - 1);
}
inputStringSplit.sort();

///////////////////////
// write output file //
///////////////////////

let outputFilePath = process.env.OUTPUT_PATH;
let outputString = inputStringSplit.join("\n");
outputString += "\n"; // trailing newline
fs.writeFileSync(outputFilePath, outputString);
