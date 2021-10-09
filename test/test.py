from pipe.pipe import csv_pipeline

def to_float(row_index, row, args):
	for column_name in list(row.keys()):
		row[column_name] = float(row[column_name])
	return row
	
def pass_through(row_index, data, args):
   return (True, data[0])

def every_fifth_row(row_index, data, args):
	if (row_index % 5) == 0:
		return (True, data[0])
	else:
		return (False, None)

def only_first_column(row_index, data, args):
	header = list(data[0].keys())
	first_col_name = header[0]
	first_col_data = data[0][first_col_name]
	out = {first_col_name: first_col_data}
	return (True, out)

def only_first_column_divby2(row_index, data, args):
	header = list(data[0].keys())
	first_col_name = header[0]
	first_col_data = data[0][first_col_name]
	res = first_col_data / 2
	return (True, {"{}-divby2".format(first_col_name): res})

to_float_args = {
	"name": "to_float",
	"args": {}
}

pass_through_args = {
	"name": "pass_through",
	"args": {
		"outPath": "./pass_through.csv"
	}
}

every_fifth_row_args = {
	"name": "every_fifth_row",
	"args": {
		"outPath": "./every_fifth_row.csv"
	}
}

only_first_column_args = {
	"name": "only_first_column",
	"args": {
		"outPath": "./only_first_column.csv"
	}
}

only_first_column_divby2_args = {
	"name": "only_first_column_divby2",
	"args": {
		"outPath": "./only_first_column_divby2.csv"
	}
}

pipe = csv_pipeline(inPath="../data/ref.csv", buffer=4)

pipe.add_preproc(to_float, to_float_args)

pipe.add_drain(pass_through, args=pass_through_args)
pipe.add_drain(every_fifth_row, args=every_fifth_row_args)
pipe.add_drain(only_first_column, args=only_first_column_args)
pipe.add_drain(only_first_column_divby2, args=only_first_column_divby2_args)

pipe.run()