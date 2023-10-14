package algozone

import (
	"testing"
)

///////////////////////
// sort script start //
///////////////////////

// insertion sort!
//
// docs: https://en.wikipedia.org/wiki/Insertion_sort
//
// Insertion sort steps through an input list, using it to grow an output list.
// On every step, it sorts the current element into its proper location on the
// output list.It continues until the input list is empty.

func insertionSort(inputList []string) (outputList []string) {

	for idx, element := range inputList {
		outputList = append(outputList, element)
		outputList = sortElementAtIndex(outputList, element, idx)
	}

	return outputList
}

func sortElementAtIndex(inputList []string, element string, idx int) (outputList []string) {
	outputList = inputList
	targetIndex := idx

	for (targetIndex != 0) && (element < outputList[targetIndex-1]) {
		outputList = swapWithPrevious(outputList, targetIndex)
		targetIndex = targetIndex - 1
	}

	return outputList
}

func swapWithPrevious(list []string, idx int) []string {
	list[idx], list[idx-1] = list[idx-1], list[idx]
	return list
}

/////////////////////
// sort script end //
/////////////////////

func TestInsertionSort(t *testing.T) {
	t.Run("test", func(t *testing.T) {
		// setup
		inputList, err := getInputList()
		if err != nil {
			t.Error(err.Error())
		}

		// logic under test
		outputList := insertionSort(inputList)

		// assertions
		err = writeAndCompareOutputList(outputList)
		if err != nil {
			t.Error(err.Error())
		}
	})
}
