import sys, os
import collections

def parseConfig(configFileName):

    directory = os.path.dirname(configFileName)
    scansDirectory = os.path.join(directory,"Scans+Textures")
    basemeshesDirectory = os.path.join(directory,"Basemeshes")
    resultsDirectory = os.path.join(directory,"Results")


    tasks = []
    lines = open(configFileName).readlines()
    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith('#'):
            continue

        (scanFileName, basemeshFileName) = line.split()
        scanShortName = os.path.split(scanFileName)[1]
        basemeshShortName = os.path.split(basemeshFileName)[1]
        
        if not os.path.isabs(scanFileName):
            scanFileName = os.path.join(scansDirectory,scanShortName)

        if not os.path.isabs(basemeshFileName):
            basemeshFileName = os.path.join(basemeshesDirectory,basemeshShortName)
            
        resultFileName = os.path.join(resultsDirectory,scanShortName)

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
#            'scansDirectory': scansDirectory,
#            'basemeshesDirectory': basemeshesDirectory,
#            'resultsDirectory': resultsDirectory,
        }

        # search textures
        textureExtensions = [".jpg",".JPG",".png",".PNG"]
        for extension in textureExtensions:
            textureFileName = os.path.join(os.path.splitext(scanFileName)[0]+extension)
            resultTextureFileName = os.path.join(resultsDirectory,os.path.splitext(scanShortName)[0]+extension)
            basemeshTextureFileName = os.path.join(os.path.splitext(basemeshFileName)[0]+extension)
            

            if os.path.exists(textureFileName):
                task['textureFileName'] = textureFileName
                task['resultTextureFileName'] = resultTextureFileName
            break
        
        for extension in textureExtensions:
            if os.path.exists(basemeshTextureFileName):
                task['basemeshTextureFileName'] = basemeshTextureFileName
                break
                
            

        # search config for optional args
        argsFileName = os.path.join(scansDirectory,os.path.splitext(scanShortName)[0] + '_args.txt')
        task['argsFileName'] = argsFileName
        if os.path.exists(argsFileName):
            task['useMethods'], task['methodsArgs'] = parseMethodsArgumentsConfig(argsFileName, getOptionalMethodsDescForParse())
        else:
            task['useMethods'], task['methodsArgs'] = collections.defaultdict(lambda: {}), collections.defaultdict(lambda: {})
            
        # filenames of contol points                            
        task['scanAlignPointsFileName'] = os.path.join(scansDirectory, scanShortName + "_alignPoints.txt")
        task['basemeshAlignPointsFileName'] = os.path.join(basemeshesDirectory, basemeshShortName + "_alignPoints.txt")

        task['scanWrapPointsFileName'] = os.path.join(scansDirectory, scanShortName + "_wrapPoints.txt")
        task['basemeshWrapPointsFileName'] = os.path.join(basemeshesDirectory, basemeshShortName + "_wrapPoints.txt")

        tasks.append(task)
        #import pprint
        #pprint.pprint(task)

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
    