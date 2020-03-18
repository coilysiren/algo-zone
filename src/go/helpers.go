package algozone

import (
	"fmt"
	"io/ioutil"
	"log"
	"path"
	"strings"
)

const randomizedDataPath = "./../../data/randomized.txt"
const sortedDataPath = "./../../data/sorted.txt"

func getInputList() (inputList []string) {
	// read input file
	fileBytes, err := ioutil.ReadFile(randomizedDataPath)
	if err != nil {
		err = fmt.Errorf("error reading input file path: %w", err)
		log.Fatal(err)
	}
	fileSlice := strings.Split(string(fileBytes), "\n")

	// clean input data
	if fileSlice[len(fileSlice)-1] == "" {
		fileSlice = fileSlice[:len(fileSlice)]
	}

	return fileSlice
}

func writeOutputList(outputList []string, filename string) {
	// setup
	filePath := path.Join(sortedDataPath, "..", filename+".txt")

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
	err := ioutil.WriteFile(filePath, outputBytes, 0644)
	if err != nil {
		err = fmt.Errorf("error writing output: %w", err)
		log.Fatal(err)
	}
}
