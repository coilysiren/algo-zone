package algozone

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

type sortFunc func([]string) []string

var inputPath = os.Getenv("INPUT_PATH")
var outputPath = os.Getenv("OUTPUT_PATH")

func getInputList() (inputList []string, err error) {
	// read input file
	fileBytes, err := os.ReadFile(filepath.Join("..", "..", inputPath))
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
	filePath := filepath.Join("..", "..", outputPath, "..", filename+".txt")

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
	err = os.WriteFile(filePath, outputBytes, 0644)
	if err != nil {
		err = fmt.Errorf("error writing output: %w", err)
		return err
	}

	return nil
}
