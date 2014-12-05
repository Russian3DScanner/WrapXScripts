import collections
import os

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
    
def parseArgumentsConfig(fileName, methodsDescription):
    useMethod = {}
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
                useMethod[methodName] = parseBool(argumentValue)
            else:
                arg = parsedArgName[1]                    
                methodsArgs[methodName][arg] = methodsDescription[methodName][arg](argumentValue)
                    
            
    
    return useMethod, methodsArgs