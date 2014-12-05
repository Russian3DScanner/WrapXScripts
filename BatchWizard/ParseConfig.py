import sys, os
import collections

def parseConfig(configFileName):

    directory = os.path.dirname(configFileName)

    tasks = []
    lines = open(configFileName).readlines()
    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith('#'):
            continue

        (scanRelativeFileName, basemeshRelativeFileName) = line.split()

        scanFileName = os.path.join(directory,'Scans+Textures',scanRelativeFileName)
        basemeshFileName = os.path.join(directory,'Basemeshes',basemeshRelativeFileName)
        resultFileName = os.path.join(directory,'Results',scanRelativeFileName)

        if not os.path.exists(scanFileName):
            print "No such file: %s, ignoring" % scanFileName
            continue

        if not os.path.exists(scanFileName):
            print "No such file: %s, ignoring" % basemesFileName
            continue
        task = {
            'scanFileName': scanFileName,
            'basemeshFileName': basemeshFileName,
            'resultFileName': resultFileName,
        }

        # search textures
        textureExtensions = [".jpg",".png"]
        for extension in textureExtensions:
            textureFileName = os.path.join(directory,'Scans+Textures',os.path.splitext(scanRelativeFileName)[0]+extension)
            resultTextureFileName = os.path.join(directory,'Results',os.path.splitext(scanRelativeFileName)[0]+extension)

            if os.path.exists(textureFileName):
                task['textureFileName'] = textureFileName
                task['resultTextureFileName'] = resultTextureFileName
                break

        # search config for optional args
        argsFileName = os.path.join(directory,'Scans+Textures',os.path.splitext(scanRelativeFileName)[0] + '_args.txt')
        if os.path.exists(argsFileName):
            task['useMethods'], task['methodsArgs'] = parseMethodsArgumentsConfig(argsFileName, getOptionalMethodsDescForParse())
        else:
            task['useMethods'], task['methodsArgs'] = collections.defaultdict(lambda: {}), collections.defaultdict(lambda: {})
        # filenames of contol points                            
        task['scanAlignPointsFileName'] = scanFileName + "_alignPoints.txt"
        task['basemeshAlignPointsFileName'] = basemeshFileName + "_alignPoints.txt"

        task['scanWrapPointsFileName'] = scanFileName + "_wrapPoints.txt"
        task['basemeshWrapPointsFileName'] = basemeshFileName + "_wrapPoints.txt"

        tasks.append(task)

    return tasks

def parseBool(string):
    if string == 'True':
        return True
    if string == 'False':
        return False
    raise Exception("Cannot parse boolean %s" % string)

def parseString(string):
    if len(string) < 2 or string[0] != string[-1] or string[0] not in ['"', "'"]:
        raise Exception("Cannot parse string: %s" % string)
    return string[1:-1]
    
def getOptionalMethodsDescForParse():
    return {
        "rigidAlignment": {
            "matchScale": parseBool
        },
        "nonRigidRegistration": {
            "initialRadiusMultiplier": float,
            "radiusMultiplier": float,
            "minNodes": int,
            "smoothnessInitial": float,
            "smoothnessFinal": float,
            "multiplierControlPoints": float,
            "maxIterations": int,
            "mu": float,
            "subdivisionPercentage": float
        },
        "subdivide": {
            "nSubdivisions": int
        },
        "projectMesh": {
            "maxRelativeDist": float,
            "checkNormalsCompatibility": parseBool
        },
        "transferTexture": {
            "maxRelativeDist": float
        }
    }
    
def parseMethodsArgumentsConfig(fileName, methodsDescription):
    useMethods = {}
    methodsArgs = collections.defaultdict(lambda: {})
    
    with open(fileName) as configFile:
        for line in configFile:
            strippedLine = line.strip()
            
            if len(strippedLine) == 0 or strippedLine[0] == '#':#empty lines and comments are skipped
                continue
                        
            argumentName, argumentValue = map(lambda x: x.strip(), strippedLine.split("="))
            parsedArgName = argumentName.split('.')
            methodName = parsedArgName[0]
            if len(parsedArgName) == 1:
                useMethods[methodName] = parseBool(argumentValue)
            else:
                arg = parsedArgName[1]        
                if arg not in methodsDescription[methodName]:
                    raise Exception("Bad arg name %s " % arg)
                methodsArgs[methodName][arg] = methodsDescription[methodName][arg](argumentValue)
                                   
    return useMethods, methodsArgs    
    