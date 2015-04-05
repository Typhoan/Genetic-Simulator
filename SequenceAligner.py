'''

Created on Apr 4, 2015

@author: Alexander Calvert

'''

from subprocess import call
import DNAFileDict

'''
class to perform sequence alignment and related operations
uses Clustal Omega to perform alignment operations
'''
class SequenceAligner:

    def __init(self):
        pass


    '''
    writes a fasta file from a dictionary mapping labels to sequences

    @param fileDict - the label/seq mapping
    @param filename - the path to the fasta file to be written
    '''
    def writeFasta(self, fileDict, filename):
        with open(filename, "w") as f:
            for label, sequence in fileDict.iteritems():
                f.write("> " + label + "\n")
                f.write(sequence + "\n")

    '''
    get a list of distances from sequences to a dominant sequence

    @param alignedSequences - list of sequence for distance calculation, assumed to be already aligned
    @return distanceMatrix - the distance matrix as a Python list
    '''
    def getDistanceMatrix(self, alignedSequences):
        """ get list of distances between dominant and subdominant sequences"""
        if not alignedSequences:
            raise ValueError("alignedSequences must not be empty")
        dominantAlignedSequence = alignedSequences[0]
        subdominantAlignedSequences = alignedSequences[1:]
        distanceMatrix = []
        for subdom in subdominantAlignedSequences:
            i = 0
            distance = 0
            while i < len(dominantAlignedSequence) and i < len(subdom):
                if (dominantAlignedSequence[i] != "-" or subdom[i] != "-") and dominantAlignedSequence[i] != subdom[i]:
                    distance += 1
                i += 1
            distanceMatrix.append(distance)
        return distanceMatrix
		

    '''
    gives a dot matrix (alignment with similar nucleotides replaced with dots)
    
    @param alignedSequences - list of sequence for distance calculation, assumed to be already aligned
    @return dotMatrix - the dot matrix
    '''
    def generateDotMatrix(self, alignedSequences):
        """ generate dot matrix based on already-aligned sequences """
        if not alignedSequences:
            raise ValueError("alignedSequences must not be empty")
        dominantAlignedSequence = alignedSequences[0]
        subdominantAlignedSequences = alignedSequences[1:]
        dotMatrix = []
        for sequence in subdominantAlignedSequences:
            listCopy = list(sequence)
            for i in range(len(sequence)):
                if sequence[i] is not "-" and dominantAlignedSequence[i] is not "-":
                    if sequence[i] == dominantAlignedSequence[i]:
                        listCopy[i] = "."
            dotMatrix.append(''.join(listCopy))
        dotMatrix.insert(0, dominantAlignedSequence)
        return dotMatrix

    '''
    performs a multiple alignment on a list of sequences using Clustal Omega

    @param fastaPathIn - the fasta-formatted file containing sequences to be aligned
    @param fastaPathOut - the fasta file the resulting alignment is outputted to
    @return returns the aligned sequences as a 2d list with gaps
    '''
    def alignSequences(self, fastaPathIn, fastaPathOut="out.fasta"):
        din = DNAFileDict.DNAFileDict(fastaPathIn)
        ret = call(["clustalo", "-i", fastaPathIn, "-o", fastaPathOut, "--outfmt=fasta", "--force"])
        if ret == 0:
            dout = DNAFileDict.DNAFileDict(fastaPathOut)
            dout.setLists()
            return dout.getDNADict().values()
        else:
            raise ValueError

'''
a = SequenceAligner()
seqs = a.alignSequences("in.fa")
for i in a.generateDotMatrix(seqs): print i
'''
