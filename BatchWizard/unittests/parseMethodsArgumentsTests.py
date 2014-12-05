import unittest
import os, sys
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), '..'))

from ParseConfig import parseMethodsArgumentsConfig, parseBool, parseString

class TestMethodArguments(unittest.TestCase):

    def test_01_parse(self):
        testFileName = 'testConfigFile1.txt'
        methodsDescriptions = {
            "nonRigidAligment": {
                "someUsefullArgument": parseString,
                "someUsefullArgumentInt": int,
                "someUsefullArgumentFloat": float,
                "uselessParam": parseBool
            },
            "rigidAligment": {
                "yetAnotherUsefullParametr": int,
                "yetAnotherUsefullParametrBool01": parseBool,
                "yetAnotherUsefullParametrBool02": parseBool
            }
        }
        usages, args = parseMethodsArgumentsConfig(testFileName, methodsDescriptions)
        
        self.assertEquals(len(usages), 1)
        self.assertEquals(usages["rigidAligment"], False)
        
        self.assertEquals(len(args), 2)
        self.assertEquals(len(args["rigidAligment"]), 3)
        self.assertEquals(args["rigidAligment"]["yetAnotherUsefullParametr"], -1)
        self.assertEquals(args["rigidAligment"]["yetAnotherUsefullParametrBool01"], True)
        self.assertEquals(args["rigidAligment"]["yetAnotherUsefullParametrBool02"], False)
        
        self.assertEquals(len(args["nonRigidAligment"]), 3)
        self.assertEquals(args["nonRigidAligment"]["someUsefullArgument"], 'My own argument!')
        self.assertEquals(args["nonRigidAligment"]["someUsefullArgumentInt"], 42)
        self.assertEquals(args["nonRigidAligment"]["someUsefullArgumentFloat"], 3.14)

    def test_02_parse_exeptions(self):
        testFileName = 'testConfigFile1Bad.txt'
        self.assertRaises(Exception, parseMethodsArgumentsConfig, testFileName, {})
        testFileName = 'testConfigFile2Bad.txt'
        self.assertRaises(Exception, parseMethodsArgumentsConfig, testFileName, {})
        testFileName = 'testConfigFile3Bad.txt'
        self.assertRaises(Exception, parseMethodsArgumentsConfig, testFileName, {
            "yetAnotherMethod":{
                'goodArg': parseBool,
                'badArg': int
            }
        })
        
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestMethodArguments)
unittest.TextTestRunner(verbosity=2).run(suite)