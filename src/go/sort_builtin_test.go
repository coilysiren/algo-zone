package algozone

import (
	"sort"
	"testing"
)

///////////////////////
// sort script start //
///////////////////////

func doBuiltinSort(inputList []string) (outputList []string) {
	outputList = inputList
	sort.Strings(outputList)
	return outputList
}

/////////////////////
// sort script end //
/////////////////////

func TestBuiltinSort(t *testing.T) {
	testName := "sorted_by_go_sort_builtin_test"
	t.Run(testName, func(t *testing.T) {
		inputList, err := getInputList()
		if err != nil {
			t.Error(err.Error())
		}

		outputList := insertionSort(inputList)

		err = writeAndCompareOutputList(outputList, testName)
		if err != nil {
			t.Error(err.Error())
		}
	})
}

// ☝🏽 per-script helpers
