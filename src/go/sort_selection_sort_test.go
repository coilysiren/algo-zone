package algozone

import (
	"testing"
)

// business logic start //

// selection sort - repeatedly pick the smallest remaining element to build the output
// https://en.wikipedia.org/wiki/Selection_sort

func selectionSort(inputList []string) (sortedList []string) {
	unsortedList := inputList
	inputListLength := len(inputList)

	for i := 0; i < inputListLength; i++ {
		smallestIndex := findSmallestIndex(unsortedList)
		smallestElement := unsortedList[smallestIndex]
		sortedList = append(sortedList, smallestElement)
		unsortedList = removeIndex(unsortedList, smallestIndex)
	}

	return sortedList
}

func findSmallestIndex(inputList []string) (smallestIndex int) {
	for index, element := range inputList {
		if element < inputList[smallestIndex] {
			smallestIndex = index
		}
	}

	return smallestIndex
}

func removeIndex(inputList []string, index int) (outputList []string) {
	outputList = append(inputList[:index], inputList[index+1:]...)
	return outputList
}

// business logic end //

func TestSelectionSort(t *testing.T) {
	t.Run("test", func(t *testing.T) {
		// setup
		inputList, err := getInputList()
		if err != nil {
			t.Error(err.Error())
		}

		// logic under test
		outputList := selectionSort(inputList)

		// assertions
		err = writeAndCompareOutputList(outputList)
		if err != nil {
			t.Error(err.Error())
		}
	})
}
