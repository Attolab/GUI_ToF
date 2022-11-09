
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


class PlotGroupParameter(pTypes.GroupParameter):
    valueChanging_signal = Signal(object,object)
    removedItem_signal = Signal(object)
    contextMenu_signal = Signal(object)
    duplicatePlot_signal = Signal(object)
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
            menu={'Duplicate':[],'Data Treatment':[{'Filter':[]},{'Smoothing':[]}]})   
        p.sigRemoved.connect(self.removingPlotGroup)
        p.sigContextMenu.connect(self.contextMenuTriggered)      
        self.addChildren(
            [p,])
        print([[childs.name(),childs.value()] for childs in pen_param.childs])



    def contextMenuTriggered(self, parent, action_label):
        if action_label[0] == 'Duplicate':
            self.duplicatePlot_signal.emit(parent)
        elif action_label == 'Filter':            
            print('Filter Data')
            self.contextMenu_signal.emit(action_label)
        elif action_label == 'Smoothing':    
            print('Smoothing Data')
            self.contextMenu_signal.emit(action_label)


    # def activate(self,action):
    #     for childs in self.childs:            
    #         if isinstance(childs, GroupParameter):
    #             childs.setOpts(expanded=action == 'Expand All') 

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
                    'centerX': {
                        'title':'X (horizontal/col)',                                        
                        'type': 'int',
                        'value': 1024,
                        },   
                    'centerY': {
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
                        'value': False,
                        },   
                    'cropX':{
                        'title':'Crop (X/horizontal)',                                        
                        'type': 'slider',
                        'value': 0,
                        'step': 1,
                        'limits':[-2048, 2048],
                        },       
                    'cropY':{
                        'title':'Crop (Y/vertical)',                                        
                        'type': 'slider',
                        'value': 0,
                        'step': 1,
                        'limits':[-2048, 2048],
                        },   
                    'Rmax':{
                        'title':'ROI',                                        
                        'type': 'slider',
                        'value': 1024,
                        'step': 1,
                        'limits':[0, 2048],
                        },                                                                                                                                                               
                        }                                                  

        # params_file = Parameter.create(name='file_parameters',title='File parameters', type='group',expanded = False,children = file_params)
        # params_file = FileParameter(name="file_parameters", title='File parameters', tip='Click to add children',children=[])
        params_image = Parameter.create(name='image_parameters',title='Image parameters', type='group',expanded = False,children = image_parameters)
        params_display = Parameter.create(name='display_parameters',title='Display parameters', type='group',expanded = False,children = 
        [PlotParameter(name='axis',title='Axis'),PlotParameter(name='range',title='Range'),PlotParameter(name='center',title='Center')])
    
        
        self.addChildren(
            [params_image,params_display,])

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

class PlotParameter(pTypes.GroupParameter):
    valueChanging_signal = Signal(object,object)

    def __init__(self, **opts):
        pTypes.GroupParameter.__init__(self, **opts)
        pen_param = Parameter.create(name='pen_param',title='Pen parameters', type='pen',expanded = False)
        show_plot = Parameter.create(name= 'show_plot', title = 'Show',type= 'bool', value= True,expanded = False)
        show_plot.sigValueChanged.connect(self.valueChanging)
        pen_param.sigValueChanging.connect(self.valueChanging)     
        # name = opts.get('name', None)   
        # self.setName(opts.get('name', None))
        # self.setTitle(opts.get('title', None))
        self.addChildren([show_plot,pen_param])
        # p = Parameter.create(name='Axis', type='group', children=[show_plot,pen_param], removable=False, renamable=False)

    def valueChanging(self,param, value):
        self.valueChanging_signal.emit(param, value)   

class FileParameter(pTypes.GroupParameter):
    valueChanging_signal = Signal(object,object)
    def __init__(self, **opts):
        opts['type'] = 'group'
        opts['addText'] = "Add"
        opts['addList'] = ['file']
        pTypes.GroupParameter.__init__(self, **opts)
    def addNew(self, typ):
        file_params =  {
                    'filename':{
                    'title':'Filename',
                    'type': 'file',
                    'value': '',
                    },
                    'select':{
                    'title':'Select',
                    'type': 'bool',
                    'value': True,
                    'readOnly':False,
                    },                    
                    'select':{
                    'title':'Select',
                    'type': 'bool',
                    'value': True,
                    'readOnly':False,
                    },
                    'ImageNumber':{
                    'title': 'Number of images',
                    'type': 'int',
                    'value': 0,
                    'readOnly':True,
                    },                    
        }        
        params = Parameter.create(name="File %d" % (len(self.childs)+1), type='group', removable=True, renamable=True, readOnly = False,children =file_params)
        params.sigTreeStateChanged.connect(self.valueChanging)
        self.addChildren([params,])

    def updateParameter(self,p,q):
        a = 0

    def valueChanging(self,param, value):
        self.valueChanging_signal.emit(param, value)


    # def addROI_linearRegionItem(self,edges,orientation):
    #     # Create ROI item
    #     lr = CustomLinearRegionItem(self.makeInitialShape(edges),orientation=orientation)        
    #     lr.leftDoubleClicked.connect(self.gotLeftDoubleClicked)
    #     lr.singleMiddleClicked.connect(self.gotMiddleSingleClicked)
    #     lr.setZValue(10)
    #     return lr

    # def addROI_infiniteLineItem(self,pos,angle,label):
    #     # self.view_1D.viewRange()[1]
    #     # pos = np.sum(self.view_1D.viewRange()[0])/2
    #     il = pg.InfiniteLine(pos = pos,movable=True, angle=angle, label=label+'={value:0.2f}', 
    #                    labelOpts={'position':0.1, 'color': (200,200,100), 'fill': (200,200,200,50), 'movable': True})
    #     il.setZValue(10)
    #     return il
ROI_NAME_PREFIX = 'ROI_'
ROI2D_TYPES = ['RectROI', 'EllipseROI']

class ROIScalableGroup(GroupParameter):
    def __init__(self, roi_type='1D', **opts):
        opts['type'] = 'group'
        opts['addText'] = "Add"
        self.roi_type = roi_type
        if roi_type != '1D':
            opts['addList'] = ROI2D_TYPES
        super().__init__(**opts)

    def addNew(self, typ=''):
        name_prefix = ROI_NAME_PREFIX
        child_indexes = [int(par.name()[len(name_prefix) + 1:]) for par in self.children()]
        if not child_indexes:
            newindex = 0
        else:
            newindex = max(child_indexes) + 1

        child = {'name': f'{ROI_NAME_PREFIX}{newindex:02d}', 'type': 'group', 'removable': True, 'renamable': False}

        children = [{'name': 'type', 'type': 'str', 'value': self.roi_type, 'readonly': True, 'visible': False}, ]
        if self.roi_type == '2D':
            children.extend([{'title': 'ROI Type', 'name': 'roi_type', 'type': 'str', 'value': typ, 'readonly': True},
                             {'title': 'Use channel', 'name': 'use_channel', 'type': 'list',
                              'limits': ['red', 'green', 'blue', 'spread']}, ])
        else:
            children.append({'title': 'Use channel', 'name': 'use_channel', 'type': 'list'})

        functions = ['Sum', 'Mean', 'half-life', 'expotime']
        children.append({'title': 'Math type:', 'name': 'math_function', 'type': 'list', 'limits': functions,
                         'value': 'Sum', 'visible': self.roi_type == '1D'})
        # children.extend([
        #     {'name': 'Color', 'type': 'color', 'value': list(np.roll(self.color_list, newindex)[0])}, ])
        if self.roi_type == '2D':
            children.extend([{'name': 'position', 'type': 'group', 'children': [
                {'name': 'x', 'type': 'float', 'value': 0, 'step': 1},
                {'name': 'y', 'type': 'float', 'value': 0, 'step': 1}
            ]}, ])
        else:
            children.extend([{'name': 'position', 'type': 'group', 'children': [
                {'name': 'left', 'type': 'float', 'value': 0, 'step': 1},
                {'name': 'right', 'type': 'float', 'value': 10, 'step': 1}
            ]}, ])
        if self.roi_type == '2D':
            children.extend([
                {'name': 'size', 'type': 'group', 'children': [
                    {'name': 'width', 'type': 'float', 'value': 10, 'step': 1},
                    {'name': 'height', 'type': 'float', 'value': 10, 'step': 1}
                ]},
                {'name': 'angle', 'type': 'float', 'value': 0, 'step': 1}])

        child['children'] = children

        self.addChild(child)