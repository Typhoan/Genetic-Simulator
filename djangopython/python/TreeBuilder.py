'''
Created on Feb 5, 2015

@author: Ian McPherson
'''


import SequenceAligner as alignment
import Topology as topo
from ete2 import TreeStyle
from time import gmtime, strftime
from djangopython.settings import MEDIA_ROOT

class TreeBuilder:

	def __init__(self, dictionary):
		self.dict = dictionary
	
	def __extractNames(self):
		self.names = self.dict.keys()
		
	def __extractSequences(self):
		self.alignedSequences = []
		for name in self.names:
			self.alignedSequences.append(self.dict.get(name))
			
	def getDistanceMatrix(self):
		self.__extractNames()
		self.__extractSequences()
		
		graph = topo.Topology(len(self.alignedSequences), self.names)
		align = alignment.SequenceAligner()
		for i in range(len(self.alignedSequences)):
			sequences = []
			sequences.append(self.alignedSequences[i])
			
			for seq in self.alignedSequences:
				sequences.append(seq)
				
			distance = align.getDistanceMatrix(sequences)
			graph.sequenceToMatrix(i, distance)
		
		distanceDict = {}
		for i in range(len(self.alignedSequences)):
			distanceDict[self.names[i]] = graph.dMatrix[i]
		
		return distanceDict
		
	
	def getDistanceMatrixAsString(self):
		self.__extractNames()
		self.__extractSequences()
		
		graph = topo.Topology(len(self.alignedSequences), self.names)
		align = alignment.SequenceAligner()
		for i in range(len(self.alignedSequences)):
			sequences = []
			sequences.append(self.alignedSequences[i])
			
			for seq in self.alignedSequences:
				sequences.append(seq)
				
			distance = align.getDistanceMatrix(sequences)
			graph.sequenceToMatrix(i, distance)
			
		matrix = graph.dMatrix
		stringMatrix = ""
		for i in range(len(self.alignedSequences)):
			stringMatrix += "{}:\t\t[ ".format(self.names[i])
			for j in range(len(self.alignedSequences)):
				if j == len(self.alignedSequences)-1:
					stringMatrix += "{} ".format(matrix[i][j])
				else:
					stringMatrix += "{}, ".format(matrix[i][j])
			stringMatrix += "]\n"
		
		return stringMatrix
		
	'''
	Uses functions from SequenceAligner.py and Topology.py to build a topological tree
	
	@return - a string to the directory where the picture is located.
	'''
	def createTree(self, directory = None):
		defaultDir = MEDIA_ROOT+'images/'
		pictureName = 'topology{}'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		if directory != None:
			defaultDir = directory
		
		self.__extractNames()
		self.__extractSequences()
		
		graph = topo.Topology(len(self.alignedSequences), self.names)
		align = alignment.SequenceAligner()
		
		for i in range(len(self.alignedSequences)):
			sequences = []
			sequences.append(self.alignedSequences[i])
			
			for seq in self.alignedSequences:
				sequences.append(seq)
				
			distance = align.getDistanceMatrix(sequences)
			graph.sequenceToMatrix(i, distance)
		
		ts = TreeStyle()
		tree = graph.matrixToGraph()
		ts.show_leaf_name = True
		ts.show_branch_support = True
		ts.show_scale = False
		tree.render("{}{}.png".format(defaultDir, pictureName), units="mm",tree_style=ts)
		#return os.path.abspath("{}{}".format(defaultDir, pictureName))
		return "{}{}".format(defaultDir, pictureName) +'.png'
		
	'''
	Uses functions from SequenceAligner.py and Topology.py to build a topological tree
	
	@return - a string describing the tree. Can be used by ete2 to rebuild the tree.
	'''
	def createTreeString(self):
		self.__extractNames()
		self.__extractSequences()
		
		graph = topo.Topology(len(self.alignedSequences), self.names)
		align = alignment.SequenceAligner()
		
		for i in range(len(self.alignedSequences)):
			sequences = []
			sequences.append(self.alignedSequences[i])
			
			for seq in self.alignedSequences:
				sequences.append(seq)
				
			distance = align.getDistanceMatrix(sequences)
			graph.sequenceToMatrix(i, distance)
		
		ts = TreeStyle()
		tree = graph.matrixToGraph()
		ts.show_leaf_name = True
		ts.show_branch_support = True
		ts.show_scale = False
		return tree.write(features=["name", "support"], outfile=None, format=0, is_leaf_fn=None)
	
