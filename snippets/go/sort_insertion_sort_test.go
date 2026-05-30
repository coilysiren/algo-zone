// insertion sort - https://en.wikipedia.org/wiki/Insertion_sort
// steps through the input, growing a sorted output by inserting each element.

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
