package algozone

import (
	"testing"
)

///////////////////////
// sort script start //
///////////////////////

// merge sort!
//
// docs: https://leetcode.com/explore/learn/card/recursion-ii/470/divide-and-conquer/2868/

func MergeSort(inputList []string) (sortedList []string) {

	var doMergeInput [][]string
	for _, item := range inputList {
		doMergeInput = append(doMergeInput, []string{item})
	}

	doMergeOutput, _ := doMerge(doMergeInput, 0)
	sortedList = doMergeOutput[0]

	return sortedList
}

func doMerge(inputList [][]string, inputRound int) (outputList [][]string, outputRound int) {

	// "round" is used for debugging
	outputRound = inputRound + 1

	// compare each pair, ignoring potential odd items
	for i := 0; i < len(inputList)/2*2; i += 2 {

		var sortedPair []string
		itemOneIndex, itemTwoIndex := 0, 0

		// fmt.Printf("first  list size is %d \n", len(inputList[i]))
		// fmt.Printf("second list size is %d \n", len(inputList[i+1]))

		for (itemOneIndex < len(inputList[i])) || (itemTwoIndex < len(inputList[i+1])) {

			// fmt.Printf("\tfirst  list index is %d \n", itemOneIndex)
			// fmt.Printf("\tsecond list index is %d \n", itemTwoIndex)

			if itemOneIndex == len(inputList[i]) {
				// boundary check on first list, append from second list
				sortedPair = append(sortedPair, inputList[i+1][itemTwoIndex])
				itemTwoIndex++
			} else if itemTwoIndex == len(inputList[i+1]) {
				// boundary check on second list, append from first list
				sortedPair = append(sortedPair, inputList[i][itemOneIndex])
				itemOneIndex++
			} else if inputList[i][itemOneIndex] < inputList[i+1][itemTwoIndex] {
				// comparison check, append from first list
				// fmt.Printf("putting item one \n")
				sortedPair = append(sortedPair, inputList[i][itemOneIndex])
				itemOneIndex++
			} else {
				// implicit comparison check, append from second list
				// fmt.Printf("putting item two \n")
				sortedPair = append(sortedPair, inputList[i+1][itemTwoIndex])
				itemTwoIndex++
			}
		}

		// fmt.Printf("\tfirst  list index is %d \n", itemOneIndex)
		// fmt.Printf("\tsecond list index is %d \n", itemTwoIndex)
		// fmt.Printf("\tcondition one is %t \n", (itemOneIndex < len(inputList[i])))
		// fmt.Printf("\tcondition two is %t \n", (itemTwoIndex < len(inputList[i+1])))
		// fmt.Printf("\tpair condition is is %t \n", (itemOneIndex < len(inputList[i])) && (itemTwoIndex < len(inputList[i+1])))
		// fmt.Printf("pair size is %d \n", len(sortedPair))

		outputList = append(outputList, sortedPair)
	}

	// handle odd items
	if len(inputList)%2 == 1 {
		outputList = append(outputList, inputList[len(inputList)-1])
	}

	// fmt.Printf("round is %d \n", outputRound)
	// fmt.Printf("operating on %d un-merged lists \n", len(inputList))
	// fmt.Printf("outputing on %d merged lists \n", len(outputList))

	// recurse!
	if len(outputList) != 1 {
		return doMerge(outputList, outputRound)
	}

	return outputList, outputRound
}

/////////////////////
// sort script end //
/////////////////////

func TestMergeSort(t *testing.T) {
	testData := []struct {
		name     string
		sortFunc sortFunc
	}{
		{
			name:     "sorted_by_go_sort_merge_sort_test",
			sortFunc: MergeSort,
		},
	}
	for _, test := range testData {
		t.Run(test.name, func(t *testing.T) {
			// setup
			inputList, err := getInputList()
			if err != nil {
				t.Error(err.Error())
			}

			// logic under test
			outputList := test.sortFunc(inputList)

			// assertions
			err = writeAndCompareOutputList(outputList, test.name)
			if err != nil {
				t.Error(err.Error())
			}
		})
	}
}

// ☝🏽 per-script helpers
