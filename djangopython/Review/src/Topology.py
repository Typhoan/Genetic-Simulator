'''
Created on Feb 5, 2015

@author: Ian McPherson
'''

from Review.src import DistancePairs as distPairs
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
    Takes the distance matrix and calculates the lowest distances to build the tree.
    
    @return - String describing all distance pairs
    '''
    def matrixToString(self):
        dPairs = []
        sequences = []
        
        for x in range(self.size):
            sequences.append(x+1)
       
        
        for x in range(self.size):
            for y in range(x):
                
                tmp = distPairs.DistancePairs(self.dMatrix[x][y], x+1, y+1)
                dPairs.append(tmp)
                
        
        dPairs.sort(key=lambda DistancePairs: DistancePairs.distance)
        
        
        treeString = ""
        counter = 0
        
        while sequences:
            
            isPartOfTree = 0
            tmp = dPairs[counter]
            tmpSeq1 = tmp.sequence1
            tmpSeq2 = tmp.sequence2
            
            if tmpSeq1 in sequences:
                isPartOfTree = 1
                sequences.remove(tmpSeq1)
            
            if tmpSeq2 in sequences:
                isPartOfTree = 1
                sequences.remove(tmpSeq2)
            
            if isPartOfTree == 1:
                treeString += 'Distance: {}, Pair: {}, {} \n'.format(tmp.distance, tmpSeq1, tmpSeq2)
                
            counter = counter + 1
        return treeString
    
    '''
    Takes the distance matrix and calculates the lowest distances to build the tree.
    
    @return - TreeNode containing the topological graph
    '''
    
    def matrixToGraph(self):
        dPairs = []
        sequences = []
        
        for x in range(self.size):
            sequences.append(x+1)
       
        
        for x in range(self.size):
            for y in range(x):
                
                tmp = distPairs.DistancePairs(self.dMatrix[x][y], x+1, y+1)
                dPairs.append(tmp)
                
        
        dPairs.sort(key=lambda DistancePairs: DistancePairs.distance)
        
        tree = Tree()
        counter = 0
        branch = []
        while sequences:
            tmp = dPairs[counter]
            tmpSeq1 = tmp.sequence1
            tmpSeq2 = tmp.sequence2
            
            if (tmpSeq1 in sequences) and (tmpSeq2 in sequences):
                hNode = tree.add_child(name = "nullNode{}".format(tmpSeq2), support=tmp.distance)
                pNode = hNode.add_child(name="Sequence:{}".format(tmpSeq2))
                cNode = hNode.add_child(name="Sequence:{}".format(tmpSeq1))
                sequences.remove(tmpSeq1)
                sequences.remove(tmpSeq2)
                
            elif (tmpSeq1 in sequences) and (not tmpSeq2 in sequences):
                pNode = tree.search_nodes(name="nullNode{}".format(tmpSeq2))
                holderNode = pNode[0]
                holderNode.name = "null"
                holderNode.detach()
                nullNode = tree.add_child(name="nullNode{}".format(tmpSeq2), support=tmp.distance)
                nullNode.add_child(holderNode)
                nullNode.add_child(name="Sequence:{}".format(tmpSeq1))
                sequences.remove(tmpSeq1)
                
            elif (tmpSeq2 in sequences) and (not tmpSeq1 in sequences):
                pNode = tree.search_nodes(name="nullNode{}".format(tmpSeq1))
                holderNode = pNode[0]
                holderNode.name = "null"
                holderNode.detach()
                nullNode = tree.add_child(name="nullNode{}".format(tmpSeq1), support=tmp.distance)
                nullNode.add_child(holderNode)
                nullNode.add_child(name="Sequence:{}".format(tmpSeq2))
                sequences.remove(tmpSeq2)
                      
            counter = counter +1
        return tree
