# Class to extract and initialize relevant values from QWidget according to given list
from os import set_inheritable
from variable_panel import VariableItemTable
from file_manager import FileManager


class WidgetData(object):
        def __init__(self, parent = None, dataExtractionParameters = None, variableItemParameters = None  ):
            self.parent = parent
            try:
                if self.parent:
                    self.keys = self.parent.fileReader.keys
                    self.fileName = self.parent.fileReader.keys
            except:
                pass

            if dataExtractionParameters:
                self.dataExtraction = WidgetDataExtraction(parent = self.parent, list_QWidget = dataExtractionParameters)
            if variableItemParameters:
                self.widgetVariableItem = VariableItemObject(parent = self, input = self.parent.fileReader.keys)

        def get_WidgetVariableItem(self):
            return self.widgetVariableItem.get_VariableItemTable()

        # def make_list_widget


class WidgetDataExtraction(object):

    def __init__(self, parent = None ,list_QWidget = []):
        self.list_QWidget = list_QWidget #List of relevant QWidget (given as list of string) in parent QWidget
        self.parent = parent
    
    def extractValues(self):        
        return dict([self._extractValuesfromWidget(getattr(self.parent,element)) for element in self.list_QWidget])

    def initializeValues(self,item_list):        
        [self._settingValuesOnWidget(getattr(self.parent, item),item_list[item]) for item in item_list]        

    def _settingValuesOnWidget(self,widget,input):
        widgetType = widget.__class__.__name__              
        if widgetType == 'QComboBox':                    
            widget.setCurrentIndex(input)
        elif widgetType == 'QLineEdit':
            widget.setText(str(input))                
        elif widgetType == 'QSpinBox':
            widget.setValue(input)
        elif widgetType == 'QDoubleSpinBox':
            widget.setValue(input)

    def _extractValuesfromWidget(self,widget):
        widgetType = widget.__class__.__name__
        name = widget.objectName()
        if widgetType == 'QComboBox':
            value = widget.currentIndex()
            return (name,value)            
        elif widgetType == 'QLineEdit':
            value = widget.text()
            return (name,value)
        elif widgetType == 'QSpinBox':
            value = int(widget.value())
            return (name,value)
        elif widgetType == 'QDoubleSpinBox':
            value = float(widget.value())
            return (name,value)                        
        elif widgetType == 'QCheckBox':
            value = widget.isChecked()                  
            return (name,value)    
        elif widgetType == 'QTableWidget':
            value =[]
            L_row = range(widget.rowCount())
            L_col = range(widget.columnCount())
            # for row in L_row:
            value = [[widget.item(row,i).text() for i in L_col if widget.item(row,i)] for row in L_row]
            return (name,value)


class VariableItemObject(object):
    def __init__(self, parent = None, file_reader = None ):
        self.widget = VariableItemTable()
        self.parent = parent   
        if file_reader:
            self.file_reader = file_reader
            self.setup_TableWidget()

    def setup_TableWidget(self): 
        self.keys = self.file_reader.keys
        self.filename = self.file_reader.filename
        self.widget.set_numberofRows(len(self.keys))        
        [self.setup_TableWidgetItem(row) for row in range(self.widget.get_numberofRows())]

    def setup_TableWidgetItem(self,row): 
        key = [self.keys[row]]   
        self.widget.set_item(row,0,self.convertInput(key)[0])
        self.widget.set_item(row,1,self.file_reader.extractShape(self.filename,key)[0])
        self.widget.set_item(row,2,self.file_reader.extractType(self.filename,key)[0])
        self.widget.set_item(row,3,self.file_reader.extractValues(self.filename,key)[0])                

    def convertInput(self,inputs):
        return [input.decode('ISO-8859-1)') if input[0] == 80 else input for input in inputs]

    def get_VariableItemTable(self):
        return self.widget.get_TableWidget()

class MousePressEvent(object):

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            print("Left Button Clicked")
        elif QMouseEvent.button() == Qt.RightButton:
            #do what you want here
            print("Right Button Clicked")
    