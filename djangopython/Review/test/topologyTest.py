'''
Created on Feb 21, 2015

@author: Ian McPherson
'''

import unittest
import src.Topology as topo
from graphviz import Digraph

class topologyTest(unittest.TestCase):
    
    def test01InstantiateTopology(self):
        self.assertIsInstance(topo.Topology(4), topo.Topology)
    
    def test02FailToInstatiateInvalidNumber(self):
        expectedString = "Topology.__init__:  Invalid number of sequences"
        try:
            testInstance01 = topo.Topology(1)
            self.fail("ValueError exception was not raised")
        except ValueError as raisedException:
            raisedString = raisedException.args[0]
            self.assertEquals(expectedString, raisedString[0:len(expectedString)])
        except:
            self.fail("Incorrect exception was raised")
    
    def test03SequenceToMatrix(self):
        testInstance01 = topo.Topology(4)
        distanceList = [0,1,2,3]
        testInstance01.sequenceToMatrix(0, distanceList)
        self.assertEquals(testInstance01.dMatrix[0][0], 0)
        self.assertEquals(testInstance01.dMatrix[1][0], 1)
        self.assertEquals(testInstance01.dMatrix[2][0], 2)
        self.assertEquals(testInstance01.dMatrix[3][0], 3)
    
    def test04SequenceToMatrixNegativeSeqNum(self):
        expectedString = "Topology.sequenceToMatrix:  Invalid sequence number"
        try:
            testInstance01 = topo.Topology(4)
            distanceList = [0,1,2,3]
            testInstance01.sequenceToMatrix(-1, distanceList)
            self.fail("ValueError exception was not raised")
        except ValueError as raisedException:
            raisedString = raisedException.args[0]
            self.assertEquals(expectedString, raisedString[0:len(expectedString)])
        except:
            self.fail("Incorrect exception was raised")
    
    def test05SequenceToMatrixInvalidSeqNum(self):
        expectedString = "Topology.sequenceToMatrix:  Invalid sequence number"
        try:
            testInstance01 = topo.Topology(4)
            distanceList = [0,1,2,3]
            testInstance01.sequenceToMatrix(4, distanceList)
            self.fail("ValueError exception was not raised")
        except ValueError as raisedException:
            raisedString = raisedException.args[0]
            self.assertEquals(expectedString, raisedString[0:len(expectedString)])
        except:
            self.fail("Incorrect exception was raised")
    
    def test06SequenceToMatrixNullDistanceList(self):
        expectedString = "Topology.sequenceToMatrix:  Invalid distance list"
        try:
            testInstance01 = topo.Topology(4)
            distanceList = []
            testInstance01.sequenceToMatrix(0, distanceList)
            self.fail("ValueError exception was not raised")
        except ValueError as raisedException:
            raisedString = raisedException.args[0]
            self.assertEquals(expectedString, raisedString[0:len(expectedString)])
        except:
            self.fail("Incorrect exception was raised")
    
    def test07SequenceToMatrixTooLargeDistanceList(self):
        expectedString = "Topology.sequenceToMatrix:  Invalid distance list"
        try:
            testInstance01 = topo.Topology(4)
            distanceList = [0,1,2,3,4]
            testInstance01.sequenceToMatrix(0, distanceList)
            self.fail("ValueError exception was not raised")
        except ValueError as raisedException:
            raisedString = raisedException.args[0]
            self.assertEquals(expectedString, raisedString[0:len(expectedString)])
        except:
            self.fail("Incorrect exception was raised")
    
    def test08SequenceToMatrixTooSmallDistanceList(self):
        expectedString = "Topology.sequenceToMatrix:  Invalid distance list"
        try:
            testInstance01 = topo.Topology(4)
            distanceList = [0,1,2]
            testInstance01.sequenceToMatrix(0, distanceList)
            self.fail("ValueError exception was not raised")
        except ValueError as raisedException:
            raisedString = raisedException.args[0]
            self.assertEquals(expectedString, raisedString[0:len(expectedString)])
        except:
            self.fail("Incorrect exception was raised")
            
    def test09MatrixToGraph(self):
        testInstance01 = topo.Topology(6)
        distanceList1 = [0,4,7,17,18,6]
        distanceList2 = [0,0,9,15,16,8]
        distanceList3 = [0,0,0,14,14,7]
        distanceList4 = [0,0,0,0,3,14]
        distanceList5 = [0,0,0,0,0,12]
        distanceList6 = [0,0,0,0,0,0]
        testInstance01.sequenceToMatrix(0, distanceList1)
        testInstance01.sequenceToMatrix(1, distanceList2)
        testInstance01.sequenceToMatrix(2, distanceList3)
        testInstance01.sequenceToMatrix(3, distanceList4)
        testInstance01.sequenceToMatrix(4, distanceList5)
        testInstance01.sequenceToMatrix(5, distanceList6)
        
        tree = Digraph(comment='Phenograph')
        tree.node("0", "Phenograph")
        tree.node("4", "Sequence:\\n4")
        tree.node("5", "Sequence:\\n5")
        tree.edge("0", "4")
        tree.edge("4", "5", "3")
        tree.node("1", "Sequence:\\n1")
        tree.node("2", "Sequence:\\n2")
        tree.edge("0", "1")
        tree.edge("1", "2", "4")
        tree.node("6", "Sequence:\\n6")
        tree.edge("1", "6", "6")
        tree.node("3", "Sequence:\\n3")
        tree.edge("1", "3", "7")
        
        self.assertEquals(testInstance01.matrixToGraph().source, tree.source)