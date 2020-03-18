package algozone

import (
	"fmt"
	"io/ioutil"
	"path"
	"strings"
	"testing"
)

type sortFunc func([]string) []string

const randomizedDataPath = "./../../data/randomized.txt"
const sortedDataPath = "./../../data/sorted.txt"

func getInputList() (inputList []string, err error) {
	// read input file
	fileBytes, err := ioutil.ReadFile(randomizedDataPath)
	if err != nil {
		err = fmt.Errorf("error reading input file path: %w", err)
		return nil, err
	}
	fileSlice := strings.Split(string(fileBytes), "\n")

	// clean input data
	if fileSlice[len(fileSlice)-1] == "" {
		fileSlice = fileSlice[:len(fileSlice)]
	}

	return fileSlice, nil
}

func writeAndCompareOutputList(outputList []string, filename string) (err error) {
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
	err = ioutil.WriteFile(filePath, outputBytes, 0644)
	if err != nil {
		err = fmt.Errorf("error writing output: %w", err)
		return err
	}

	return nil
}

func runTest(t *testing.T, testName string, sortFunc sortFunc) {
	t.Run(testName, func(t *testing.T) {
		inputList, err := getInputList()
		if err != nil {
			t.Error(err.Error())
		}

		outputList := sortFunc(inputList)

		err = writeAndCompareOutputList(outputList, testName)
		if err != nil {
			t.Error(err.Error())
		}
	})
}
