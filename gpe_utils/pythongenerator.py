
def generatePython(components):
    all_imports={}
    readers=["timestamp=time.time()"]
    variables=["timestamp"]        
    types=["%f"]
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
                variables.append(curVar)
            if "type" in csvCodes:
                curType=csvCodes["type"]
            if "reader" in csvCodes:
                if curVar==None:
                    print("Missing variable name for component",component)
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
    args={"header":",".join(variables),"readers":"\n    ".join(readers),"formatstr":",".join(types), "variables": ",".join(variables),"imports":"\nimport ".join(all_imports.keys())}
    pythonReturn="""
import time
import %(imports)s

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