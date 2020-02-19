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

func TestBuiltinSort(t *testing.T) {

	// setup
	workingDirectory, err := os.Getwd()
	if err != nil {
		log.Fatal(err)
	}
	inputFilePath := path.Join(workingDirectory, "../../", os.Getenv("INPUT_PATH"))
	ouputFilePath := path.Join(workingDirectory, "../../", os.Getenv("OUTPUT_PATH"))

	/////////////////////
	// read input file //
	/////////////////////

	inputFileBytes, err := ioutil.ReadFile(inputFilePath)
	if err != nil {
		log.Fatal(err)
	}
	inputFileString := string(inputFileBytes)
	inputFileStringSlice := strings.Split(inputFileString, "\n")

	////////////////
	// sort input //
	////////////////

	// drop the trailing newline, so that it doesn't get included in the sort
	if inputFileStringSlice[len(inputFileStringSlice)-1] == "" {
		inputFileStringSlice = inputFileStringSlice[:len(inputFileStringSlice)]
	}
	sort.Strings(inputFileStringSlice)

	///////////////////////
	// write output file //
	///////////////////////

	outputString := strings.Join(inputFileStringSlice, "\n")
	// join adds a leading \n entry, which needs to be removed
	if outputString[0:1] == "\n" {
		outputString = outputString[1:]
	}
	// add trailing \n
	outputString += "\n"
	outputBytes := []byte(outputString)

	err = ioutil.WriteFile(ouputFilePath, outputBytes, 0644)
	if err != nil {
		log.Fatal(err)
	}

}
