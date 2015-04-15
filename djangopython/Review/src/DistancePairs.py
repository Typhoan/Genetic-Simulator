'''
Created on Feb 5, 2015

@author: Ian McPherson
'''
class DistancePairs:
    distance = -1
    sequence1 = -1
    sequence2 = -1
    
    def __init__(self, dist, seq1, seq2):
        if dist == None or seq1 == None or seq2 == None:
            raise ValueError("DistancePairs.__init__:  invalid parameters")
        if seq1 == seq2:
            raise ValueError("DistancePairs.__init__:  Duplicate sequences")
        if seq1 < 0 or seq2 < 0:
            raise ValueError("DistancePairs.__init__:  Invalid sequence number")
        self.distance = dist
        self.sequence1 = seq1
        self.sequence2 = seq2
        
    def printDP(self):
        print str(self.distance) + ' ' + str(self.sequence1) + ' ' + str(self.sequence2)