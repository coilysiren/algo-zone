package algozone

import (
	"testing"
)

///////////////////////
// sort script start //
///////////////////////

// bubble sort!
//
// docs: https://en.wikipedia.org/wiki/Bubble_sort
//
// bubble sort steps through a list, comparing adjacent elements and swapping them if they
// are in the wrong order. it passes through the list repeatedly until the list is sorted

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

/////////////////////
// sort script end //
/////////////////////

func TestBubbleSort(t *testing.T) {
	inputList := getInputList()
	outputList := bubbleSort(inputList)
	testName := "sorted_by_go_sort_bubble_sort_test"
	t.Run(testName, func(t *testing.T) {
		writeOutputList(outputList, testName)
	})
}

// ☝🏽 per-script helpers
