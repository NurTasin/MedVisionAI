import json

class DBMS:
    def __init__(self,fpath):
        self.filepath=fpath
    
    def read(self):
        with open(self.filepath,"r") as fp:
            return json.load(fp)
    
    def write(self,data):
        with open(self.filepath,"w") as fp:
            json.dump(data,fp,indent=2)