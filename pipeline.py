import csv 
import sys

class csv_pipeline():
    """ 
                                                            --- drain0 --> csv-file
                                                            | 
    csv-file -> - init -- preproc0 -- preproc1 -- preprocN -|-- drain1 --> csv-file
                                                            |
                                                            --- drainN --> csv-file
    """
    
    init_args = [
        {
            "name": "fetcher",
            "args": {}
        },
        {
            "name": "decoder",
            "args": {}
        }
    ]
    
    preproc_args = [
        # {
        #     "name": "dummy_preproc",
        #     "args": {}
        # }
    ]
    
    drain_args = [
        # {
        #     "name": "dummy_drain",
        #     "args": {
        #         "outPath": None
        #     }
        # }
    ]
    
    def get_args(self, args, name):
        return [item for item in args if item["name"] == name][0]
    
    def get_args_index(self, args, name):
        return [i for i, item in enumerate(args) if item["name"] == name][0]
    
    def fetcher(self, path):
        with open(path, "r") as file:
            yield file

    def decoder(self, file):
        args = self.get_args(self.init_args, "decoder")
        delimiter = args["args"]["delimiter"]
        dict_reader = csv.DictReader(next(file), delimiter=delimiter)
        for row in dict_reader:
            yield row
    
    def dummy_drain(row_index, data, args):
        return (False, None)
    
    def dummy_preproc(row_index, row, args):
        mod_row = row
        return mod_row

    init = [
        fetcher,
        decoder
    ]
    preproc = [
#        dummy_preproc           
    ]
    drains = [
#        dummy_drain
    ]
 
    def create(self, inPath):
        generator = inPath
        for filter in self.init:
            generator = filter(self, generator)
        return generator
            
    def __init__(self, inPath, buffer=None):
        self.inPath = inPath
        self.pipe = self.create(self.inPath)
        # buffer = default number of rows (N) given to every drain function cycle:
        # the current row + (N-1) past rows
        if buffer:
            self.buffer = buffer
        else:
            self.buffer = 10
            
        # check delimiter in header
        with open(inPath, "r") as file:
            header = file.readline()
            if "," in header:
                self.delimiter = ","
            elif ";" in header:
                self.delimiter = ";"
            else:
                print("Error: No valid delimiter (',' or ';') found in header of file {}...".format(inPath))
                sys.exit(1)

        self.init_args[self.get_args_index(self.init_args, "decoder")]["args"] = {"delimiter": self.delimiter}
    
    def add_preproc(self, func, args):
        self.preproc.append(func)
        self.preproc_args.append(args)
    
    def add_drain(self, func, args):
        self.drains.append(func)
        self.drain_args.append(args)
       
    def run(self):
        writers = [None] * len(self.drains)
        data = [None] * (self.buffer + 1)
        outFiles = []
        for args in self.drain_args:
            outPath = args["args"]["outPath"]
            outFiles.append(open(outPath, "w"))
        
        for row_index, row in enumerate(self.pipe):
            
            # preprocess
            for prep_index, prep in enumerate(self.preproc):
                args = self.preproc_args[prep_index]["args"]
                row = prep(row_index, row, args)
            
            # prepare data -> shift data
            for n in range(self.buffer):
                data[n+1] = data[n]
            data[0] = row
            
            for drain_index, drain in enumerate(self.drains):
                args = self.drain_args[drain_index]["args"]
                (do_write, output) = drain(row_index, data, args)
            
                if output and outFiles[drain_index]:
                    if writers[drain_index]:
                        if do_write:
                            writers[drain_index].writerow(output)
                    else:
                        fieldnames = list(output.keys())
                        writers[drain_index] = csv.DictWriter(outFiles[drain_index], fieldnames=fieldnames, lineterminator="\n")
                        writers[drain_index].writeheader()
                        if do_write:
                            writers[drain_index].writerow(output)