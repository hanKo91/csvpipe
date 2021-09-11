# csvpipe

A simple python module to setup a csv data manipulation pipeline

## Installation

There are no dependencies besides the python standard library

## Usage

See [test.py](./test.py)

```python
""" 
                                                            --- drain0 --> csv-file
                                                            | 
    csv-file -> - init -- preproc0 -- preproc1 -- preprocN -|-- drain1 --> csv-file
                                                            |
                                                            --- drainN --> csv-file
"""
```

## License
[MIT](https://choosealicense.com/licenses/mit/)