'''
Created on Feb 21, 2015

@author: Ian McPherson
'''

import unittest
import src.DistancePairs as distPairs


class distancePairsTest(unittest.TestCase):
    
    def test01InitializeDistancePairs(self):
        self.assertIsInstance(distPairs.DistancePairs(1,1,2), distPairs.DistancePairs)
    
    def test02FailToInstatiateDuplicateSequences(self):
        expectedString = "DistancePairs.__init__:  Duplicate sequences"
        try:
            testInstance01 = distPairs.DistancePairs(1,1,1)
            self.fail("ValueError exception was not raised")
        except ValueError as raisedException:
            raisedString = raisedException.args[0]
            self.assertEquals(expectedString, raisedString[0:len(expectedString)])
        except:
            self.fail("Incorrect exception was raised")
    
    def test03FailToInstatiateInvalidSequenceNumber(self):
        expectedString = "DistancePairs.__init__:  Invalid sequence number"
        try:
            testInstance01 = distPairs.DistancePairs(1,1,-1)
            self.fail("ValueError exception was not raised")
        except ValueError as raisedException:
            raisedString = raisedException.args[0]
            self.assertEquals(expectedString, raisedString[0:len(expectedString)])
        except:
            self.fail("Incorrect exception was raised")
    
    def test04FailToInstatiateInvalidParameters(self):
        expectedString = "DistancePairs.__init__:  invalid parameters"
        try:
            testInstance01 = distPairs.DistancePairs(None,None,None)
            self.fail("ValueError exception was not raised")
        except ValueError as raisedException:
            raisedString = raisedException.args[0]
            self.assertEquals(expectedString, raisedString[0:len(expectedString)])
        except:
            self.fail("Incorrect exception was raised")