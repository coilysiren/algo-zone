// bubble sort!
//
// docs: https://en.wikipedia.org/wiki/Bubble_sort
//
// bubble sort steps through a list, comparing adjacent elements and swapping them if they are in the wrong order
// it passes through the list repeatedly until the list is sorted

package algozone

import (
	"io/ioutil"
	"log"
	"os"
	"path"
	"strings"
	"testing"
)

// bubble_sort is the top level function responsible for ... bubble sorting!
func bubbleSort(inputList []string) (outputList []string) {
	// setup defaults
	outputList = inputList
	isSorted := false

	// continuously do sorting rounds as long as the list remains unsorted
	for isSorted == false {
		outputList, isSorted = doSortingRound(outputList)
	}

	return outputList
}

// doSortingRound does the "actual sorting"
func doSortingRound(inputList []string) (outputList []string, isSorted bool) {
	isSorted = true

	for index, element := range inputList {
		if index == 0 {
			// we compare (index VS index - 1) so theres
			// nothing to compare when looking at the 0th index
			outputList = []string{element}
		} else if element < outputList[index-1] {
			// if this element is less than the previous element then swap their order
			visitedElements := outputList[:index-1]
			previousElement := outputList[index-1]
			// append a list of
			//	- all the list elements we've visited already
			//	- the current element
			//	- the previous element
			// which has the effect of swapping the order of the current and previous
			// elements, while also keeping all of the visited elements in place
			outputList = append(visitedElements, element, previousElement)
			isSorted = false
		} else {
			// otherwise append
			outputList = append(outputList, element)
		}
	}

	return outputList, isSorted
}

func TestBubbleSort(t *testing.T) {

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
	// drop the trailing newline, so that it doesn't get included in the sort
	if inputFileStringSlice[len(inputFileStringSlice)-1] == "" {
		inputFileStringSlice = inputFileStringSlice[:len(inputFileStringSlice)]
	}

	////////////////
	// sort input //
	////////////////

	sortedSlice := bubbleSort(inputFileStringSlice)

	///////////////////////
	// write output file //
	///////////////////////

	outputString := strings.Join(sortedSlice, "\n")
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
