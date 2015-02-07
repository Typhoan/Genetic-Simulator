'''
Created on Feb 5, 2015

@author: Ian McPherson
'''

import DistancePairs as distPairs

class Topology:
    
    
    def __init__(self, numSeqs):
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
        for x in range(len(distanceList)):
            self.dMatrix[seqNum].append(distanceList[x])
    
    '''
    Takes the distance matrix and calculates the lowest distances to build the tree.
    
    @return - String describing all distance pairs
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
