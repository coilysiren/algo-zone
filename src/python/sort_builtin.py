import sys

###################
# read input file #
###################

inputFilePath = sys.argv[1]
with open(inputFilePath, "r") as inputFileObject:
    inputFileData = inputFileObject.readlines()

##############
# sort input #
##############

sortedData = sorted(inputFileData)

#####################
# write output file #
#####################

outputFilePath = sys.argv[2]
with open(outputFilePath, "w") as outputFileObject:
    outputFileObject.writelines(sortedData)
