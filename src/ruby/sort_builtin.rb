###################
# read input file #
###################

input_file_path = ENV["INPUT_PATH"]
input_file = File.readlines(input_file_path)

##############
# sort input #
##############

input_file = input_file.sort

#####################
# write output file #
#####################

output_file_path = ENV["OUTPUT_PATH"]
File.open(output_file_path, "wb") { |f| f.write(input_file.join("")) }
