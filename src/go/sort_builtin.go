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

	var outputString string
	for _, line := range inputFileStringSlice[1:] {
		outputString += line
		outputString += "\n"
	}
	outputBytes := []byte(outputString)
	ouputFilePath := os.Args[2]
	err = ioutil.WriteFile(ouputFilePath, outputBytes, 0644)
	if err != nil {
		log.Fatal(err)
	}
}
