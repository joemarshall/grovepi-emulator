""" This module allows you to draw basic line graphs on the LCD screen
"""

import grovelcd

_rows=1
_cols=1
_graph_styles={}
_graph_values={}

GRAPH_BUFFER_SIZE=128

def set_style(graphName,colour,minVal,maxVal,subgraph_x=None,subgraph_y=None):
    """ Set the style of a named graph in the output box.

    Parameters
    ----------
    graphName: str
        The name of the graph, used to send values to it, and displayed on screen
    colour: str
        The colour of the line, can be in the format "rgb(0,255,0)" or "red", "blue" etc.
    minVal: float
        The value of the bottom of the graph
    maxVal: float
        The value of the top of the graph
    subgraph_x: int, optional
        If you set x subgraphs, the graph window will be split horizontally from 0 to the maximum subgraph you set.    
    subgraph_y: int, optional
        If you set y subgraphs, the graph window will be split vertically from 0 to the maximum subgraph you set.    
    """
    global _rows,_cols,_graph_styles,_graph_values
    if subgraph_x>=2 or subgraph_y>=2:
        print("Only 2x2 graphs are supported on raspberry pi")
    if subgraph_x!=None:
        _cols=max(_cols,subgraph_x+1)
    else:
        subgraph_x=0
    if subgraph_y!=None:
        _rows=max(_rows,subgraph_y+1)
    else:
        subgraph_y=0
    graph_style={"min":minVal,"max":maxVal,"x":subgraph_x,"y":subgraph_y}
    _graph_styles[graphName]=graph_style
    _graph_values[graphName]=[0]*GRAPH_BUFFER_SIZE
    
    
    
def on_value(graphName,value):
    """ Add a value to a named graph in the output box

    Parameters
    ----------
    graphName: str
        The name of the graph, which should be the same as passed to set_graph_style
    value: float
        The value you want to add to the graph. If you add None, it doesn't change the graph, 
        this allows you to directly pass in the output of a \`BlockAverageFilter\` or similar 
        which return None when there is no new value.
    """
    global _rows,_cols,_graph_styles,_graph_values
    # ignore None values as block based filters output them when
    # no value is ready
    if value!=None:
        if graphName not in _graph_values:
            _graph_values[graphName]=[0]*GRAPH_BUFFER_SIZE
        if graphName not in _graph_styles:
            graph_style={"min":0,"max":1,"x":0,"y":0}
            _graph_styles[graphName]= graph_style
        graph_style=_graph_styles[graphName]
        if graph_style["min"]!=None and graph_style["max"]!=None:
            value-=graph_style["min"]
            value/=(graph_style["max"]-graph_style["min"])
        _graph_values[graphName]=_graph_values[graphName][1:]+[value]
        grovelcd.addGraphData(_graph_values[graphName],graph_style["x"],graph_style["y"],_cols,_rows)
        
if __name__=="__main__":
    import time,math
    set_style("sin","ff0000",-1,1,0,0)
    STEP=0.05
    for c in range(1000):
        on_value("sin",math.sin(c*STEP))
        time.sleep(0.01)
    set_style("tan","ff0000",-1,1,1,0)
    for c in range(1000):
        on_value("sin",math.sin(c*STEP))
        on_value("tan",math.tan(c*STEP))
        time.sleep(0.01)


    set_style("cos","ff0000",-1,1,0,1)
    set_style("coss","ff0000",0,1,1,1)
    for c in range(4000):
        on_value("sin",math.sin(c*STEP))
        on_value("tan",math.tan(c*STEP))        
        on_value("cos",math.cos(c*STEP))
        on_value("coss",math.cos(c*STEP)**2)        
        time.sleep(0.01)

