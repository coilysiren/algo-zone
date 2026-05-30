// selection sort - https://en.wikipedia.org/wiki/Selection_sort
// repeatedly find the smallest element and append it to the sorted output list.

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
