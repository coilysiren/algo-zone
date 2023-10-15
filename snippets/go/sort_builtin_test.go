func builtinSort(inputList []string) (outputList []string) {
	outputList = inputList
	sort.Strings(outputList)
	return outputList
