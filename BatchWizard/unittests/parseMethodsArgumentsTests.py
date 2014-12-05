import unittests

import parseMethodsArguments

class TestMethodArguments(unittest.TestCase):

    def test_01_parse(self):
        pass
        

suite = unittest.TestLoader().loadTestsFromTestCase(TestMethodArguments)
unittest.TextTestRunner(verbosity=2).run(suite)