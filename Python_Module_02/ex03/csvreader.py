import sys
sys.tracebacklimit = 0

class CsvReader():
    def __init__(self, filename=None, sep=', ', header=False, skip_top=0, skip_bottom=0):
        if not filename:
            raise ValueError("No filename given")
        if not isinstance(skip_top, int) or skip_top < 0:
            raise ValueError("Invalid skip_top value")
        if not isinstance(skip_bottom, int) or skip_bottom < 0:
            raise ValueError("Invalid skip_bottom value")
        self.filename = filename
        self.sep = sep
        self.header = header
        self.skip_top = skip_top
        self.skip_bottom = skip_bottom
        self.file_obj = None
        self.fulldata = []
    
    def __enter__(self):
        self.file_obj = open(self.filename, mode="r", encoding="utf-8")
        for line in self.file_obj:
            self.fulldata.append(list(map(str.strip, line.split(self.sep))))
        if all(len(elem) == len(self.fulldata[0]) for elem in self.fulldata):
            return self
        else:
            return None
        
    def __exit__(self, type, value, traceback):
        self.fulldata = []
        self.file_obj.close()
    
    def getdata(self):
        start = self.skip_top
        end = len(self.fulldata) - self.skip_bottom
        if self.header:
            return self.fulldata[start + 1 : end]
        else:
            return self.fulldata[start : end]
    
    def getheader(self):
        if self.header:
            return self.fulldata[0]
        else:
            return None