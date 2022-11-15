 # Custom class to handle data and store them in a similar pattern as the nodes structure in editableTreeModel
import numpy as np

class DataContainer():

    def __init__(self,data=None) -> None:        
        self._data = {}
        if data:
            self.addData(data)
        
    def data(self,key=None):
        if key:
            return self._data[key]
        return self._data.values()

    def keys(self):
        return self._data.keys()

    def addEntry(self,data,key):
        if key not in self._data.keys():
            self._data[key] = data
            return print(f'Adding Variable: {key}')

    def removeEntry(self,key):
        if key in self._data.keys():
            self._data.pop(key)
            return print(f'Removing Variable: {key}')    

    def updateEntry(self,keys):
        self._data[keys[1]] = self._data.pop(keys[0])
        return print(f'Variable: {keys[0]} ======> Variable: {keys[1]}')    

    def setData(self,data):
        self._data = {}
        self.addData(data)

    def addData(self,dic,path =()):
        for k,v in dic.items():
            if type(v) is dict:
                self.addData(v,path + (k,))
            else:
                self.addEntry(v,path + (k,))

    def clearData(self,):
        self._data.clear()
    
    def getDic(dic,key):
        return dic[key]

    def makeDicFromKey(self,key_tuple,key_pos):
        # Function to get similar input for data until some changes are made on the editable tree model
        tree_dict = self._data[key_tuple]
        i = 0
        for key in reversed(key_tuple):
            if i < key_pos:            
                i+=1
                tree_dict = {key: tree_dict}                        
        return tree_dict
        

def main():
    import numpy as np
    data = {'Type':{"Project A": np.ones((5,1)),
            "Project B": np.zeros((5,1)),
            "Project C": np.ones((5,1))}}    
    import sys
    data2 = {'test':data}
    D = DataContainer()
    D.setData(data2)
    print(D._data)
    D.addData(data)
    print(D._data)
    D.setData(data)
    print(D._data)
    D.makeDicFromKey( ('Type', 'Project A'),0)
    A = 1
if __name__=="__main__":
    main()
