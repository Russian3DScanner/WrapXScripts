import collections
import os

def parseBool(string):
    if string == 'True':
        return True
    if string == 'False':
        return False
    raise Exception("Cannot parse boolean")

def parseArgumentsConfig(fileName, methodsDescription):
    useMethod = {}
    methodsArgs = {}
    with open(fileName) as configFile:
        for line in configFile:
            strippedLine = line.strip()
            if len(strippedLine) == 0 or strippedLine[0] == '#':#empty lines and comments are skipped
                continue
            try:
                argumentName, argumentValue = map(lambda x: x.strip(), strippedLine.split("="))
                parsedArgName = argumentName.split('.')
                methodName = parsedArgName[0]
                if len(parsedArgName) == 1:
                    useMethod[methodName] = parseBool(argumentValue)
                else:
                    arg = parsedArgName[1]                    
                    methodArgs[methodName][arg] = methodsDescription[methodName][arg](argumentValue)
                    
            except Exception as e:
                print 'Cannot parse line'