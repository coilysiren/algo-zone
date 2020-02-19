import os
import sys

###################
# read input file #
###################

inputFilePath = os.getenv("INPUT_PATH")
with open(inputFilePath, "r") as inputFileObject:
    inputFileData = inputFileObject.readlines()

##############
# sort input #
##############

sortedData = sorted(inputFileData)

#####################
# write output file #
#####################

outputFilePath = os.getenv("OUTPUT_PATH")
with open(outputFilePath, "w") as outputFileObject:
    outputFileObject.writelines(sortedData)
