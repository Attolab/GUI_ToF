
"""
This example demonstrates the use of pyqtgraph's parametertree system. This provides
a simple way to generate user interfaces that control sets of parameters. The example
demonstrates a variety of different parameter types (int, float, list, etc.)
as well as some customized parameter types
"""

# `makeAllParamTypes` creates several parameters from a dictionary of config specs.
# This contains information about the options for each parameter so they can be directly
# inserted into the example parameter tree. To create your own parameters, simply follow
# the guidelines demonstrated by other parameters created here.

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from PySide6.QtCore import Signal,SIGNAL,Qt
from PySide6.QtWidgets import QAbstractItemView,QTreeWidgetItemIterator,QTreeWidget
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter,ParameterTree
from pyqtgraph.parametertree.parameterTypes import GroupParameter
import numpy as np

# app = pg.mkQApp("Parameter Tree Example")
class CustomParameterTree(ParameterTree):
    removeItem_signal = Signal(int)
    itemSelected_signal = Signal(int,str)
    def __init__(self,parent=None):
        super(CustomParameterTree, self).__init__(parent)
        self.connectSignals()
        self.isNotUpdating = True
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.connect(self,SIGNAL("customContextMenuRequested(QPoint)" ), self.parameterTreeRightClicked)    
    def connectSignals(self):
        # Table connection              
        self.itemSelectionChanged.connect(self.changeItemSelection)
        self.setHeaderHidden(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDrop) #Internal move

    def get_selectedRows(self):
        return np.flip(np.unique([self.indexFromItem(item).row() for item in self.selectedItems() if item.param.type() == 'group']))
    
    def changeItemSelection(self):
        if self.isNotUpdating:
            self.isNotUpdating = False
            row_sel = self.get_selectedRows()
            count = len(self.plot_list)                    
            for row in np.arange(count):
                if row in row_sel:
                    self.itemSelected_signal.emit(row,'selected')
                else:
                    self.itemSelected_signal.emit(row,'unselected')
            self.isNotUpdating = True

    def contextMenuEvent(self, ev):
        # if len(self.selectedItems()) > 1:            
        item = self.currentItem()
        if hasattr(item, 'contextMenuEvent'):
            item.contextMenuEvent(ev)     
        else:
            print('Got clicked')

                
    def parameterTreeRightClicked(self):
        print('Got clicked')
    # def checkPlotSelection(self,item):
    #     return (item.param.name() != 'Plot List') & (item.param.type() == 'group')            
    # def count_PlotTerm(self):
    #     count = 0
    #     iterator = QTreeWidgetItemIterator(self) # pass your treewidget as arg
    #     while iterator.value():
    #         # print(type(iterator.value()).__name__)
    #         if self.checkPlotSelection(iterator.value()):
    #             count +=1        
    #         iterator += 1
    #     return count

class PlotGroupParameter(pTypes.GroupParameter):
    valueChanging_signal = Signal(object,object)
    removedItem_signal = Signal(object)
    contextMenu_signal = Signal(object)
    def __init__(self, **opts):
        # opts['type'] = 'group'
        pTypes.GroupParameter.__init__(self, **opts)
        # self.sigContextMenu.connect(self.contextMenuEvent)
        # super().__init__(self, **opts)
    def addNew(self, **opts):
        parameters = opts.get('parameters', None)
        name = opts.get('name', None)
        if name:
            name = self.makeNextNameEntry(name)
        else:
            name = self.makeNextNameEntry()
        pen_param = Parameter.create(name='pen_param',title='Pen parameters', type='pen',expanded = False)
        if parameters:
            pen_param.updateFromPen(pen_param,parameters)
        show_plot = Parameter.create(name= 'show_plot', title = 'Show',type= 'bool', value= True,expanded = False)
        show_plot.sigValueChanged.connect(self.valueChanging)
        pen_param.sigValueChanging.connect(self.valueChanging)
        p = Parameter.create(name=name, type='group', children=[show_plot,pen_param], removable=True, renamable=True,
            menu={'Data Treatment':[{'Filter':[]},{'Smoothing':[]}]})   
        p.sigRemoved.connect(self.removingPlotGroup)
        p.sigContextMenu.connect(self.contextMenuTriggered)
        # for child in p.children():
        #         child.sigValueChanging.connect(self.valueChanging)        
        self.addChildren(
            [p,])
        print([[childs.name(),childs.value()] for childs in pen_param.childs])



    def contextMenuTriggered(self, parent, action_label):
        if action_label == 'Filter':            
            print('Filter Data')
            self.contextMenu_signal.emit(action_label)
        elif action_label == 'Smoothing':    
            print('Smoothing Data')
            self.contextMenu_signal.emit(action_label)




    def activate(self,action):
        for childs in self.childs:            
            if isinstance(childs, GroupParameter):
                childs.setOpts(expanded=action == 'Expand All') 

    def makeNextNameEntry(self,baseName='Plot'):
        hasFoundName = False
        i = 0
        while not hasFoundName:
            name = baseName+"_%d" % i
            if not(np.any([name == child.name() for child in self.childs])):
                hasFoundName=True
                return name
            i = i+1


    def valueChanging(self,param, value):
        self.valueChanging_signal.emit(param, value)

    def removingPlotGroup(self,param,):
        self.removedItem_signal.emit(param,)





class Viewer1DGroupParameter(pTypes.GroupParameter):
    valueChanging_signal = Signal(object,object)
    removedItem_signal = Signal(object)

    def __init__(self, **opts):
        pTypes.GroupParameter.__init__(self, **opts)
        title_params =  {
                    'name': 'title',
                    'title':'Plot title',
                    'type': 'str',
                    'value': 'Viewer 1D'
        }

        grid_params =  {
                    'x_grid': {
                        'title':'x',                                        
                        'type': 'bool',
                        'value': True,
                        },   
                    'y_grid': {
                        'title':'y',                                        
                        'type': 'bool',
                        'value': True,
                        },    
                    'alpha_grid': {
                        'title':'alpha',                                        
                        'type': 'slider',
                        'span': np.linspace(0,1.0,11),
                        'value': 0.3,
                        },                            
                }                      
        xAxis_params =  {
                'x_label': {
                    'title':'label',
                    'type': 'str',
                    'value': '{x axis title}'
                    },
                'x_flipped': {
                    'title':'flipped'                    ,
                    'type': 'bool',
                    'value': True
                    },
                    
                'x_autorange': {
                    'title':'autorange',                                        
                    'type': 'bool',
                    'value': True,
                    'enabled': False
                    },                        
        }
        yAxis_params =  {
                'y_label': {
                    'title':'label',
                    'type': 'str',
                    'value': '{y axis title}'
                    },
                'y_flipped': {
                    'title':'flipped',                                        
                    'type': 'bool',
                    'value': True
                    },               
                'y_autorange': {
                    'title':'autorange',                                        
                    'type': 'bool',
                    'value': True,
                    'enabled': False
                    },                    
        }

        params_title = Parameter.create(**title_params)
        params_x = Parameter.create(name='x_axis',title='x-axis', type='group',expanded = False,children = xAxis_params)
        params_y = Parameter.create(name='y_axis',title='y-axis', type='group',expanded = False,children = yAxis_params)
        params_grid = Parameter.create(name='grid',title='Grid', type='group',expanded = False,children = grid_params)

        self.addChildren(
            [params_title,params_grid,params_x,params_y])

        self.sigTreeStateChanged.connect(self.valueChanging)
        # self.connectSignal(self.childs)



    def connectSignal(self,childs):
        for child in childs:
            if child.childs:
                self.connectSignal(child)
            else:
                child.sigValueChanged.connect(self.valueChanging)        
    def valueChanging(self,param, value):
        self.valueChanging_signal.emit(param, value)    



class Viewer2DGroupParameter(pTypes.GroupParameter):
    valueChanging_signal = Signal(object,object)

    def __init__(self, **opts):
        pTypes.GroupParameter.__init__(self, **opts)
        
        title_params =  {
                    'name': 'title',
                    'title':'Plot title',
                    'type': 'str',
                    'value': 'Viewer 2D'
        }                           
        xAxis_params =  {
                'x_label': {
                    'title':'label',
                    'type': 'str',
                    'value': '{x axis title}'
                    },
                'x_flipped': {
                    'title':'flipped'                    ,
                    'type': 'bool',
                    'value': True
                    },
                    
                'x_autorange': {
                    'title':'autorange',                                        
                    'type': 'bool',
                    'value': True,
                    'enabled': False
                    },                        
        }
        yAxis_params =  {
                'y_label': {
                    'title':'label',
                    'type': 'str',
                    'value': '{y axis title}'
                    },
                'y_flipped': {
                    'title':'flipped',                                        
                    'type': 'bool',
                    'value': True
                    },               
                'y_autorange': {
                    'title':'autorange',                                        
                    'type': 'bool',
                    'value': True,
                    'enabled': False
                    },                    
        }

        params_title = Parameter.create(**title_params)
        params_x = Parameter.create(name='x_axis',title='x-axis', type='group',expanded = False,children = xAxis_params)
        params_y = Parameter.create(name='y_axis',title='y-axis', type='group',expanded = False,children = yAxis_params)

        self.addChildren(
            [params_title,params_x,params_y])

        self.sigTreeStateChanged.connect(self.valueChanging)
        # self.connectSignal(self.childs)



    def connectSignal(self,childs):
        for child in childs:
            if child.childs:
                self.connectSignal(child)
            else:
                child.sigValueChanged.connect(self.valueChanging)        
    def valueChanging(self,param, value):
        self.valueChanging_signal.emit(param, value)    






class VMIParameter(pTypes.GroupParameter):
    valueChanging_signal = Signal(object,object)
    removedItem_signal = Signal(object)

    def __init__(self, **opts):
        pTypes.GroupParameter.__init__(self, **opts)
        file_params =  {
                    'filename':{
                    'title':'',
                    'type': 'str',
                    'value': '',
                    'readOnly':True,
                    },
                    'ImageNumber':{
                    'title': 'Number of images',
                    'type': 'int',
                    'value': 0,
                    'readOnly':True,
                    },                    
        }
        image_parameters = {
                    'center_x': {
                        'title':'X (horizontal/col)',                                        
                        'type': 'int',
                        'value': 1024,
                        },   
                    'center_y': {
                        'title':'Y (vertical/row)',                                        
                        'type': 'int',
                        'value': 1024,
                        },                                                   
                    'theta': {
                        'title':'Angle (rotation)',                                        
                        'type': 'float',
                        'value': 0,
                        },     
                    'transpose': {
                        'title':'isTransposed',                                        
                        'type': 'bool',
                        'value': True,
                        },                                                                                                 
                        }                                                  
        display_parameters =  {
                    'show_axis': {
                        'title':'Show Axis',                                        
                        'type': 'bool',
                        'value': True,
                        },   
                    'show_center': {
                        'title':'Show Center',                                        
                        'type': 'bool',
                        'value': True,
                        },    
                    'show_range': {
                        'title':'Show Range',                                        
                        'type': 'bool',
                        'value': True,
                        },                          
                }                      

        params_file = Parameter.create(name='file_parameters',title='File parameters', type='group',expanded = False,children = file_params)

        params_image = Parameter.create(name='image_parameters',title='Image parameters', type='group',expanded = False,children = image_parameters)
        params_display = Parameter.create(name='display_parameters',title='Display parameters', type='group',expanded = False,children = display_parameters)
    

        self.addChildren(
            [params_file,params_image,params_display])

        self.sigTreeStateChanged.connect(self.valueChanging)

    def updateFileParameters(self,params):
        a=1
        # self.insertChild()
        # self.removeChild()

    def connectSignal(self,childs):
        for child in childs:
            if child.childs:
                self.connectSignal(child)
            else:
                child.sigValueChanged.connect(self.valueChanging)        
    def valueChanging(self,param, value):
        self.valueChanging_signal.emit(param, value)    