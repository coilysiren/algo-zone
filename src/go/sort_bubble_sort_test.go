package algozone

import (
	"testing"
)

// business logic start //

// bubble sort - https://en.wikipedia.org/wiki/Bubble_sort
// steps through the list, swapping adjacent out-of-order pairs, repeating until sorted

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
			// rebuild as visited + current + previous, swapping the pair
			// while keeping the already-visited elements in place
			outputList = append(visitedElements, element, previousElement)
			isSorted = false
		} else {
			// otherwise append
			outputList = append(outputList, element)
		}
	}

	return outputList, isSorted
}

// business logic end //

func TestBubbleSort(t *testing.T) {
	t.Run("test", func(t *testing.T) {
		// setup
		inputList, err := getInputList()
		if err != nil {
			t.Error(err.Error())
		}

		// logic under test
		outputList := bubbleSort(inputList)

		// assertions
		err = writeAndCompareOutputList(outputList)
		if err != nil {
			t.Error(err.Error())
		}
	})
}
