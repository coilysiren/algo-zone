# frozen_string_literal: true

########################
# business logic start #
########################

def do_sorting(input_list)
  output_list = input_list
  output_list = output_list.sort
  output_list
end

######################
# business logic end #
######################

if __FILE__ == $PROGRAM_NAME
  input_file_path = ENV['INPUT_PATH']
  input_file = File.readlines(input_file_path)

  sorted_data = do_sorting(input_file)

  output_file_path = ENV['OUTPUT_PATH']
  File.open(output_file_path, 'wb') { |f| f.write(sorted_data.join('')) }
end
