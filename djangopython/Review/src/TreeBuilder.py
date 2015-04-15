'''
Created on Feb 5, 2015

@author: Ian McPherson
'''


import Review.src.SequenceAligner as alignment
import Review.src.Topology as topo
import os
from ete2 import Tree
from ete2 import TreeStyle
from datetime import datetime

'''
Uses functions from SequenceAligner.py and Topology.py to build a topological tree

@return - a string to the directory where the picture is located.
'''
def createTree(alignedSequences, directory = None):
	defaultDir = 'test-output/'
	pictureName = 'topology'+unicode(datetime.now())
	if directory != None:
		defaultDir = directory
		
	graph = topo.Topology(len(alignedSequences))
	align = alignment.SequenceAligner()
	
	for i in range(len(alignedSequences)):
		sequences = []
		sequences.append(alignedSequences[i])
		
		for seq in alignedSequences:
			sequences.append(seq)
			
		distance = align.getDistanceMatrix(sequences)
		graph.sequenceToMatrix(i, distance)
	
	ts = TreeStyle()
	tree = graph.matrixToGraph()
	ts.show_leaf_name = True
	ts.show_branch_support = True
	ts.show_scale = False
	tree.render("{}{}.png".format(defaultDir, pictureName), units="mm",tree_style=ts )
	
	return os.path.abspath("{}{}".format(defaultDir, pictureName))


sample = []
sample.append("AAAAAAAAAAAAAAAAAAAAAAAAA")
sample.append("CCCCAAAAAAAAAAAAAAAAAAAAA")
sample.append("AATTTTTTTAAAAAAAAAAAAAAAA")
sample.append("CCTTTCCCCCCCCCCCCAAAAAAAA")
sample.append("CCTTTTCCCCCCCCTCCCAAAAAAA")
sample.append("AATTTAAAAAAAAAATCCAAAAAAA")

tree = createTree(sample)
print tree
