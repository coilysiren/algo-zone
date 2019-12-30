package main

import (
	"io/ioutil"
	"log"
	"os"
	"sort"
	"strings"
)

func main() {

	/////////////////////
	// read input file //
	/////////////////////

	inputFilePath := os.Args[1]
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
	ouputFilePath := os.Args[2]
	err = ioutil.WriteFile(ouputFilePath, outputBytes, 0644)
	if err != nil {
		log.Fatal(err)
	}
}
