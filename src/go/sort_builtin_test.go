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
	inputList := getInputList()
	outputList := doBuiltinSort(inputList)
	writeOutputList(outputList, "sorted_by_go_sort_builtin_test")
}

// ☝🏽 per-script helpers
