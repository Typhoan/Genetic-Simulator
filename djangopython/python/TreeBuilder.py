'''
Created on Feb 5, 2015

@author: Ian McPherson
'''


import SequenceAligner as alignment
import Topology as topo

'''
Uses functions from alignment.py and Topology.py to build a topological tree

@return - a string describing the tree
'''
def createTree(sequences):
	
	graph = topo.Topology(len(sequences))
				
	for i in range(len(sequences)):
		dominantSeq = sequences[i]
		align = alignment.SequenceAligner()
		aligned = []
		distance = []
		
		aligned = align.alignSequences(dominantSeq, sequences)
		distance = align.getDistanceMatrix(aligned)
		graph.sequenceToMatrix(i, distance)
	
	treeString = graph.matrixToGraph()
	return treeString

'''
sample = []
sample.append("TGGCTGTAGCTGTAATAAAATGTTTG")
sample.append("AGGGCTGTATTATATATGATTAAGTA")
sample.append("TTATCCGCGTCGTATCTTTTTAGTAG")
sample.append("GATCTGTGTGTGSAATATATATAAAA")
sample.append("GGATTACCTCGCGGAGACTAGCTCGT")
sample.append("GGATCATCGTATCGTGATCGTCTAGC")

d1 = [0,0,0,0,0,0]
d2 = [4,0,0,0,0,0]
d3 = [7,9,0,0,0,0]
d4 = [17,15,14,0,0,0]
d5 = [18,16,14,3,0,0]
d6 = [6,8,7,14,12,0]

testDistanceToMatrix = topo.Topology(6)
testDistanceToMatrix.sequenceToMatrix(0, d1)
testDistanceToMatrix.sequenceToMatrix(1, d2)
testDistanceToMatrix.sequenceToMatrix(2, d3)
testDistanceToMatrix.sequenceToMatrix(3, d4)
testDistanceToMatrix.sequenceToMatrix(4, d5)
testDistanceToMatrix.sequenceToMatrix(5, d6)

distanceTree = ''
distanceTree = testDistanceToMatrix.matrixToGraph()
print distanceTree

# expect to see
# Distance: 3, Pair: 5, 4 
# Distance: 4, Pair: 2, 1 
# Distance: 6, Pair: 6, 1 
# Distance: 7, Pair: 3, 1 

tree = ''
tree = createTree(sample)
print tree
'''
