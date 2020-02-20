#####################
# sort script start #
#####################

def do_sorting(input_list)
  output_list = input_list
  output_list = output_list.sort
  output_list
end

###################
# sort script end #
###################

# 👇🏽 copy pasted helpers

input_file_path = ENV["INPUT_PATH"]
input_file = File.readlines(input_file_path)

sorted_data = do_sorting(input_file)

output_file_path = ENV["OUTPUT_PATH"]
File.open(output_file_path, "wb") { |f| f.write(sorted_data.join("")) }
