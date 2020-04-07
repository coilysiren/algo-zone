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

	doMergeOutput, _ := mergeSortRound(doMergeInput, 0)
	sortedList = doMergeOutput[0]

	return sortedList
}

func mergeSortRound(inputList [][]string, inputRound int) (outputList [][]string, outputRound int) {

	// "round" is used for debugging
	outputRound = inputRound + 1

	// merge each pair, ignoring potential odd items
	for i := 0; i < len(inputList)/2*2; i += 2 {
		outputList = append(
			outputList,
			merge(inputList[i], inputList[i+1]),
		)
	}

	// handle odd items
	if len(inputList)%2 == 1 {
		outputList = append(outputList, inputList[len(inputList)-1])
	}

	// recurse!
	if len(outputList) != 1 {
		return mergeSortRound(outputList, outputRound)
	}

	return outputList, outputRound
}

func merge(left []string, right []string) (result []string) {
	leftIndex, rightIndex := 0, 0

	for (leftIndex < len(left)) || (rightIndex < len(right)) {

		if leftIndex == len(left) {
			// boundary check on first list, append from second list
			result = append(result, right[rightIndex])
			rightIndex++
		} else if rightIndex == len(right) {
			// boundary check on second list, append from first list
			result = append(result, left[leftIndex])
			leftIndex++
		} else if left[leftIndex] < right[rightIndex] {
			// comparison check, append from first list
			// fmt.Printf("putting item one \n")
			result = append(result, left[leftIndex])
			leftIndex++
		} else {
			// implicit comparison check, append from second list
			// fmt.Printf("putting item two \n")
			result = append(result, right[rightIndex])
			rightIndex++
		}
	}

	// fmt.Printf("\tfirst  list index is %d \n", leftIndex)
	// fmt.Printf("\tsecond list index is %d \n", rightIndex)
	// fmt.Printf("\tcondition one is %t \n", (leftIndex < len(left)))
	// fmt.Printf("\tcondition two is %t \n", (rightIndex < len(right)))
	// fmt.Printf("\tpair condition is is %t \n", (leftIndex < len(left)) && (rightIndex < len(right)))
	// fmt.Printf("pair size is %d \n", len(result))

	return result
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
