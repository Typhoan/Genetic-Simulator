'''
Created on Feb 5, 2015
@author: Ian McPherson
@version - 0.5

Last edited: April 9, 2015
Content edited: Broke up matrixToGraph into several private functions that only do a specific function.
'''

import DistancePairs as distPairs
from ete2 import Tree

class Topology:
    
    
    def __init__(self, numSeqs):
        if numSeqs < 2:
            raise ValueError("Topology.__init__:  Invalid number of sequences")
        self.dMatrix = []
        
        for x in range(numSeqs):
            self.dMatrix.append([]) 
        
        self.size = numSeqs
    
    
    '''
    Adds distances from the given list to the distance matrix.
    
    @param - Sequence number (tells where in the list to put it.
    @param - Distance list that contains the number of differences.
    ''' 
    def sequenceToMatrix(self, seqNum, distanceList):
        if seqNum < 0 or seqNum >= self.size:
            raise ValueError("Topology.sequenceToMatrix:  Invalid sequence number")
        if len(distanceList) != self.size or distanceList == []:
            raise ValueError("Topology.sequenceToMatrix:  Invalid distance list")
        counter = 0
        for dist in distanceList:
            self.dMatrix[counter].append(dist)
            counter = counter + 1
    
    '''
    Uses the internal distance matrix and populates a list with distancePairs.
    Using the list of distancePairs, the tree is constructed branch by branch based on the
    distancePair's distance. 
    
    @return - TreeNode containing the topological graph
    '''
    def matrixToGraph(self):
        tree = Tree()
        sequences = self.__fillSequences()
        dPairs = self.__findDistancePairs()     
        dPairs.sort(key=lambda DistancePairs: DistancePairs.distance)
        return self.__generateTree(sequences, dPairs, tree)
    
    
    '''
    Fills a list with integers equal to the number sequences given.
    This list is used to keep track of what sequence has not been used in the tree.
    EX. there are 4 sequences, the list will contain [1,2,3,4].
    
    @return sequences - a list of integers.
    '''
    def __fillSequences(self):
        sequences = []
        
        for x in range(self.size):
            sequences.append(x + 1)
        
        return sequences
    
    '''
    Finds all distance pairs within the distance matrix. 
    This will not produce duplicates or match a sequence with itself.
    
    @return dPairs - a list of distancePairs.
    '''
    def __findDistancePairs(self):
        dPairs = []
        
        for x in range(self.size):
            for y in range(x):
                tmp = distPairs.DistancePairs(self.dMatrix[x][y], x + 1, y + 1)
                dPairs.append(tmp)
        
        return dPairs
    
    '''
    This function is called when both sequences within the distancePair are both in the sequence list.
    This will result in a new branch with two new children added to the tree.
    
    @param sequences - list of integers describing the remaining unused sequences.
    @param tree - root node of the tree.
    @param distancePair - a single distancePairs that contains the two sequences and distance.
    '''
    def __createNewBranch(self, sequences, tree, distancePair):
        nullNode = tree.add_child(name="nullNode{}".format(distancePair.sequence1), support=distancePair.distance)
        nullNode.add_child(name="Sequence:{}".format(distancePair.sequence2))
        nullNode.add_child(name="Sequence:{}".format(distancePair.sequence1))
        sequences.remove(distancePair.sequence1)
        sequences.remove(distancePair.sequence2)

    '''
    This function is called when the first sequences within the distancePair is in the sequence list.
    This will result in a new branch with one new child added to the tree.
    
    @param sequences - list of integers describing the remaining unused sequences.
    @param tree - root node of the tree.
    @param distancePair - a single distancePairs that contains the two sequences and distance.
    @param knownSeq - an integer that lets the code know what sequence is not in sequences.
    '''
    def __addSequenceToTree(self, sequences, tree, distancePair, knownSeq):
        if (knownSeq == 1):
            parentNode = tree.search_nodes(name="Sequence:{}".format(distancePair.sequence1))
        elif (knownSeq == 2):
            parentNode = tree.search_nodes(name="Sequence:{}".format(distancePair.sequence2))

        holderNode = parentNode[0].up
        holderNode.detach()
    
        if (knownSeq == 1):
            nullNode = tree.add_child(support=distancePair.distance)
        elif (knownSeq == 2):
            nullNode = tree.add_child(support=distancePair.distance)
        
        nullNode.add_child(holderNode)
        
        if (knownSeq == 1):
            nullNode.add_child(name="Sequence:{}".format(distancePair.sequence2))
            sequences.remove(distancePair.sequence2)
        elif (knownSeq == 2):
            nullNode.add_child(name="Sequence:{}".format(distancePair.sequence1))
            sequences.remove(distancePair.sequence1)

    '''
    Creates the the tree node by node.
    
    @param sequences - list of integers describing the remaining unused sequences.
    @param tree - root node of the tree.
    @param dPair - list of distancePairs.
    @return tree - The root node of the topological tree.
    '''
    def __generateTree(self, sequences, dPairs, tree):
        counter = 0
        while sequences:
            distancePair = dPairs[counter]
            
            if (distancePair.sequence1 in sequences) and (distancePair.sequence2 in sequences):
                self.__createNewBranch(sequences, tree, distancePair)
                
            elif (distancePair.sequence1 in sequences) and (not distancePair.sequence2 in sequences):
                self.__addSequenceToTree(sequences, tree, distancePair, 2)
                
            elif (distancePair.sequence2 in sequences) and (not distancePair.sequence1 in sequences):
                self.__addSequenceToTree(sequences, tree, distancePair, 1)
                
            counter = counter + 1

        return tree

    '''
    Note: This function is not needed, but will be left for test purposes.
    Takes the distance matrix and calculates the lowest distances to build the tree.
    
    @return - String describing the tree and its pairs.
    '''
    def matrixToString(self):
        sequences = self.__fillSequences()
        dPairs = self.__findDistancePairs()    
        
        dPairs.sort(key=lambda DistancePairs: DistancePairs.distance)
        
        
        treeString = ""
        counter = 0
        
        while sequences:
            
            isPartOfTree = 0
            distancePair = dPairs[counter]
            dPairSeq1 = distancePair.sequence1
            dPairSeq2 = distancePair.sequence2
            
            if dPairSeq1 in sequences:
                isPartOfTree = 1
                sequences.remove(dPairSeq1)
            
            if dPairSeq2 in sequences:
                isPartOfTree = 1
                sequences.remove(dPairSeq2)
            
            if isPartOfTree == 1:
                treeString += 'Distance: {}, Pair: {}, {} \n'.format(distancePair.distance, dPairSeq1, dPairSeq2)
                
            counter = counter + 1
        return treeString

