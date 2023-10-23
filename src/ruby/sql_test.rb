# frozen_string_literal: true

require 'json'

########################
# business logic start #
########################

class SQLState
  attr_reader :state

  def initialize(state = {})
    @state = state
  end

  def read_table_meta(table_name)
    @state[table_name] ? @state[table_name]['metadata'] || {} : {}
  end

  def read_table_rows(table_name)
    @state[table_name] ? @state[table_name]['rows'] || [] : []
  end

  def read_information_schema
    @state.values.map { |data| data['metadata'] }
  end

  def write_table_meta(table_name, data)
    @state[table_name] ||= {}
    @state[table_name]['metadata'] ||= {}
    @state[table_name]['metadata'].merge!(data)
    self.class.new(@state)
  end

  def write_table_rows(table_name, data)
    @state[table_name] ||= {}
    @state[table_name]['rows'] ||= []
    @state[table_name]['rows'] << data
    self.class.new(@state)
  end
end

module SQLType
  def self.varchar(data)
    data.to_s.strip.sub(/^['"]/, '').sub(/['"]$/, '')
  end

  def self.int(data)
    data.to_i
  end
end

module SQLFunctions
  def self.create_table(state, *args, table_schema: 'public')
    output = []
    table_name = args[2]

    columns = {}
    columns_str = args[3..].join(' ').gsub(/[()]/, '').strip
    unless columns_str.empty?
      columns = Hash[columns_str.split(',').map { |column| column.strip.split(' ') }]
    end

    if state.read_table_meta(table_name).empty?
      metadata = {
        'table_name' => table_name,
        'table_schema' => table_schema,
        'columns' => columns
      }
      state = state.write_table_meta(table_name, metadata)
    end

    [output, state]
  end

  def self.insert_into(state, *args)
    output = []
    table_name = args[2]

    sql_type_map = {
      'VARCHAR' => SQLType.method(:varchar),
      'INT' => SQLType.method(:int)
    }

    values_index = args.index('VALUES')
    raise 'VALUES not found' if values_index.nil?

    keys = args[3...values_index].join(' ').gsub(/[()]/, '').split(',').map(&:strip)
    values = args[values_index + 1..].join(' ').gsub(/[()]/, '').split(',').map(&:strip)
    key_value_map = Hash[keys.zip(values)]

    metadata = state.read_table_meta(table_name)
    row = {}
    key_value_map.each do |key, value|
      row[key] = sql_type_map[metadata['columns'][key]].call(value)
    end
    state = state.write_table_rows(table_name, row)

    [output, state]
  end

  def self.select(state, *args)
    output = []

    from_index = args.index('FROM')
    # where_index = args.index('WHERE')

    raise 'FROM not found' if from_index.nil?

    select_keys = args[1...from_index].join(' ').split(',').map {|s| s.gsub(/[()]/, '')}.map(&:strip)
    from_value = args[from_index + 1]

    data = if from_value == 'information_schema.tables'
             state.read_information_schema
           else
             state.read_table_rows(from_value)
           end

    data.each do |datum|
      output << select_keys.map { |key| [key, datum[key]] }.to_h
    end

    [output, state]
  end
end

def run_sql(input_sql)
  output = []
  state = SQLState.new

  input_sql = input_sql.map(&:strip).reject { |line| line.start_with?('--') }
  input_sql = input_sql.join(' ').split(';')

  sql_function_map = {
    'CREATE TABLE' => SQLFunctions.method(:create_table),
    'SELECT' => SQLFunctions.method(:select),
    'INSERT INTO' => SQLFunctions.method(:insert_into)
  }

  input_sql.each do |line|
    words = line.split(' ')
    words.each_index do |i|
      key = words[0..i].join(' ').strip
      if sql_function_map.key?(key)
        output, state = sql_function_map[key].call(state, *words.reject(&:empty?))
        break
      end
    end
  end

  [output.to_json]
end

######################
# business logic end #
######################

if __FILE__ == $PROGRAM_NAME
  input_file_path = ENV['INPUT_PATH']
  input_file = File.readlines(input_file_path)

  sorted_data = run_sql(input_file)

  output_file_path = ENV['OUTPUT_PATH']
  File.open(output_file_path, 'wb') { |f| f.write(sorted_data.join('')) }
end
