import sys, os
import collections

def parseConfig(configFileName, defaultSettingsFileName = None):

    #if os.path.basename(configFileName) == "defaultSettings.txt":
    #    raise Exception("'%s' is not config file" % os.path.basename(configFileName))


    directory = os.path.dirname(configFileName)
    scansDirectory = os.path.join(directory,"Scans+Textures")
    basemeshesDirectory = os.path.join(directory,"Basemeshes")
    wrappedResultsDirectory = os.path.join(directory,"Results_Wrapped")
    postprocResultsDirectory = os.path.join(directory,"Results_PostProcessed")


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

        wrappedResultFileName = os.path.join(wrappedResultsDirectory,scanShortName)
        postprocResultFileName = os.path.join(postprocResultsDirectory,scanShortName)

        if not os.path.exists(scanFileName):
            print "No such file: %s, ignoring" % scanFileName
            continue

        if not os.path.exists(scanFileName):
            print "No such file: %s, ignoring" % basemesFileName
            continue

        task = {
            'scanFileName': scanFileName,
            'basemeshFileName': basemeshFileName,
            'wrappedResultFileName': wrappedResultFileName,
            'postprocResultFileName': postprocResultFileName,
#            'scansDirectory': scansDirectory,
#            'basemeshesDirectory': basemeshesDirectory,
#            'resultsDirectory': resultsDirectory,
        }

        # search textures
        textureExtensions = [".jpg",".JPG",".png",".PNG"]

        for extension in textureExtensions:
            textureFileName = os.path.join(os.path.splitext(scanFileName)[0]+extension)
            postprocResultTextureFileName = os.path.join(postprocResultsDirectory,os.path.splitext(scanShortName)[0]+extension)

            if os.path.exists(textureFileName):
                task['textureFileName'] = textureFileName
                task['postprocResultTextureFileName'] = postprocResultTextureFileName
                break

        for extension in textureExtensions:
            basemeshTextureFileName = os.path.join(os.path.splitext(basemeshFileName)[0]+extension)

            if os.path.exists(basemeshTextureFileName):
                task['basemeshTextureFileName'] = basemeshTextureFileName
                break

        if defaultSettingsFileName:
            # search config for optional args
            task['defaultSettingsFileName'] = defaultSettingsFileName
            task['customSettingsFileName'] = os.path.join(scansDirectory,os.path.splitext(scanShortName)[0] + '_args.txt')

            if os.path.exists(task['customSettingsFileName']):
                task['usedSettingsFileName'] = task['customSettingsFileName']
            else:
                task['usedSettingsFileName'] = task['defaultSettingsFileName']

            task['useMethods'], task['methodsSettings'] = parseMethodsArgumentsConfig(task['usedSettingsFileName'], getOptionalMethodsDescForParse())


        # filenames of contol points                            
        task['scanPointsFileName'] = os.path.join(scansDirectory, scanShortName + "_Points.txt")
        task['basemeshPointsFileName'] = os.path.join(basemeshesDirectory, basemeshShortName + "_Points.txt")

        tasks.append(task)
        #import pprint
        #pprint.pprint(task)


    if not tasks:
        raise Exception("'%s' contatins no tasks, maybe you selected wrong filename?" % os.path.filename(configFileName))

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
    methodsSettings = collections.defaultdict(lambda: {})

    with open(fileName) as configFile:
        for line in configFile:
            strippedLine = line.strip()

            #empty lines and comments are skipped
            if len(strippedLine) == 0 or strippedLine[0] == '#':
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
                methodsSettings[methodName][arg] = methodsDescription[methodName][arg](argumentValue)

    return useMethods, methodsSettings

