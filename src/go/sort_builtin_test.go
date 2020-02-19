package algozone

import (
	"io/ioutil"
	"log"
	"os"
	"path"
	"sort"
	"strings"
	"testing"
)

///////////////////////
// sort script start //
///////////////////////

func doBuiltinSort(inputList []string) (outputList []string) {
	outputList = inputList
	sort.Strings(outputList)
	return outputList
}

func TestBuiltinSort(t *testing.T) {
	inputList := getInputList()
	outputList := doBuiltinSort(inputList)
	writeOutputList(outputList)
}

/////////////////////
// sort script end //
/////////////////////

func getInputList() (inputList []string) {
	// setup
	workingDirectory, err := os.Getwd()
	if err != nil {
		log.Fatal(err)
	}
	inputFilePath := path.Join(workingDirectory, "../../", os.Getenv("INPUT_PATH"))

	// read input file
	inputFileBytes, err := ioutil.ReadFile(inputFilePath)
	if err != nil {
		log.Fatal(err)
	}
	inputFileString := string(inputFileBytes)
	inputFileStringSlice := strings.Split(inputFileString, "\n")

	// clean input data
	if inputFileStringSlice[len(inputFileStringSlice)-1] == "" {
		inputFileStringSlice = inputFileStringSlice[:len(inputFileStringSlice)]
	}

	return inputFileStringSlice
}

func writeOutputList(outputList []string) {
	// setup
	workingDirectory, err := os.Getwd()
	if err != nil {
		log.Fatal(err)
	}
	ouputFilePath := path.Join(workingDirectory, "../../", os.Getenv("OUTPUT_PATH"))

	// clean data
	outputString := strings.Join(outputList, "\n")
	// join adds a leading \n entry, which needs to be removed
	if outputString[0:1] == "\n" {
		outputString = outputString[1:]
	}
	// add trailing \n
	outputString += "\n"
	outputBytes := []byte(outputString)
	// write file finally
	err = ioutil.WriteFile(ouputFilePath, outputBytes, 0644)
	if err != nil {
		log.Fatal(err)
	}
}
