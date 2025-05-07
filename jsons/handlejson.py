import numpy as np
import json
import os
#in-progress standardized format for the animations.
def export(
        filename: str,
        ID: int,
        template:str,
        total_cells: int,
        cell_id:int,
):
    cols={"ID":ID,
          "template":template,
          "total_cells":total_cells,
          "cell_id":cell_id
          }
    with open(filename,'w') as json_file:
        json.dump(cols,json_file)       #dumps all data to json with filename.
def importjson(filename):
    with open(filename, 'r') as file:
        data=json.load(file)
        return data

def main():
    export("Test.json",1,"BSD",100,2)
if __name__=='__main__':
    main()