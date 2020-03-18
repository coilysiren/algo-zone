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
	testData := []struct {
		name     string
		sortFunc sortFunc
	}{
		{
			name:     "sorted_by_go_sort_builtin_test",
			sortFunc: doBuiltinSort,
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
