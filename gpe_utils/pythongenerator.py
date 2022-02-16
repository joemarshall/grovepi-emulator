
def generatePython(components):
    all_imports={}
    readers=["timestamp=time.time()"]
    variables=["timestamp"]        
    types=["%f"]
    pin_mappings=[]
    for component in components:
        if hasattr(component,"getCSVCode"):
            csvCodes=component.getCSVCode()
            curVar=None
            curType="%d"
            if "imports" in csvCodes:
                for moduleName in csvCodes["imports"]:
                    all_imports[moduleName]=1
            if "variables" in csvCodes:
                for var in csvCodes["variables"]:
                    variables.append(var)
            if "variable" in csvCodes:
                curVar=csvCodes["variable"]
                if type(curVar)==type([]):
                    variables.extend(curVar)
                else:
                    variables.append(curVar)
            if "type" in csvCodes:
                curType=csvCodes["type"]
            if "pin_mappings" in csvCodes:
                pin_mappings.extend(csvCodes["pin_mappings"])
            if "reader" in csvCodes:
                if curVar==None:
                    print(("Missing variable name for component",component))
                else:
                    if type(curVar)==type([]):
                        if len(curVar)!=len(csvCodes["reader"]):
                            print("Wrong number of readers or variables for component",component)
                        else:
                            for var,code in zip(curVar,csvCodes["reader"]):                            
                                readers.append(var+"="+code)
                                types.append(curType)
                    else:                          
                        readers.append(curVar+"="+csvCodes["reader"])
                        types.append(curType)
            if "readall" in csvCodes:
                readers.append(csvCodes["readall"])
                if "types" in csvCodes:
                    types.extend(csvCodes["types"])
                else:
                    for c in range(len(csvCodes["readall"])):
                        types.append("%d")
    args={"header":",".join(variables),"pin_mappings":",\n    ".join(pin_mappings),"readers":"\n    ".join(readers),"formatstr":",".join(types), "variables": ",".join(variables),"imports":"\nimport ".join(list(all_imports.keys()))}
    pythonReturn="""
import time
import sensors
import %(imports)s

pin_mappings={%(pin_mappings)s}
sensors.set_pins(pin_mappings)

# show a header line so that this is a readable CSV
print("%(header)s")

while True:
    # read all the sensors
    %(readers)s
    
    # output a line of text, separated by commas
    print("%(formatstr)s"%%(%(variables)s))
    
    # wait for 1 second - change this to alter how quickly
    # sensor data is collected
    time.sleep(1)
"""%args
    return pythonReturn