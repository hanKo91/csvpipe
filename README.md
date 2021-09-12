# csvpipe

A simple python module to setup a csv data manipulation pipeline

## Installation

There are no dependencies besides the python standard library.
Install with:

```python
# pip = pip3
pip install .
```
## Usage

See example [test.py](./test.py)

In general a pipeline consists of:
* 0 or more preprocessing steps, seriell structure, inclusive (for all drains)
* 1 or more drains, parallel structure, exclusive (for a single drain)

```python
""" 
                                                            --- drain0 --> csv-file
                                                            | 
    csv-file -> - init -- preproc0 -- preproc1 -- preprocN -|-- drain1 --> csv-file
                                                            |
                                                            --- drainN --> csv-file
"""
```
Every preprocess and every drain is given a configuration, which can include preprocess/drain-specific variables:

```python
	<name>_args = [
		# {
		# 	"name": "<name>",
		# 	"args": {}
		# }
	]
```

The only predefined drain argument is "outPath":
```python
    <name>_args = {
        "name": "<name>",
        "args": {
            "outPath": "/path/to/outfile.csv"
        }
    }
```
This writes the values (dictionary with key/value pairs) returned by the drain into a csv file.

## License
[MIT](https://choosealicense.com/licenses/mit/)