'''

Created on Apr 4, 2015

@author: Alexander Calvert

'''

from subprocess import check_output
import DNAFileDict
import tempfile

'''
class to perform sequence alignment and related operations
'''
class SequenceAligner:

    def __init__(self):
        pass

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
    def generateDotMatrix_old(self, alignedSequences):
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
    gives a dot matrix (alignment with similar nucleotides replaced with dots)
    
    @param alignedSequences - list of sequence for distance calculation, assumed to be already aligned
    @return dotMatrix - the dot matrix
    '''
    def generateDotMatrix(self, dominantAlignedSequence, subdominantAlignedSequences):
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

    @param seqMatrix - the sequence matrix containing all of the sequences to be aligned
    @return returns the aligned sequences as a 2d list with gaps
    '''
    def alignSequences(self, seqMatrix):
        fastaIn = tempfile.NamedTemporaryFile()
        fastaOut = tempfile.NamedTemporaryFile()
        with tempfile.NamedTemporaryFile() as fastaIn, tempfile.NamedTemporaryFile() as fastaOut:
            for i in range(len(seqMatrix)):
                fastaIn.write(">" + str(i) + "\n")
                fastaIn.write(seqMatrix[i] + "\n")
            fastaIn.seek(0)
            output = check_output(["clustalo", "-i", fastaIn.name, "--outfmt=fasta"])
            fastaOut.write(output)
            fastaOut.seek(0)
            dout = DNAFileDict.DNAFileDict(fastaOut.name)
            dout.setLists()
            return dout.getDNADict().values()
           
'''
sample = []
sample.append("AGCTAGATTATAATTTCGGGCGATAGCTAGATCGATAGC")
sample.append("GCTAGCCCCCTTTATAGGCTATATATAGATATCGCTGCT")
sample.append("AGGGCTATCATCGACGTATCATATATACGCGATCGGTTA")
a = SequenceAligner()
seqs = a.alignSequences(sample)
for s in seqs: print s
print ""
for s in a.generateDotMatrix(seqs.pop(), seqs): print s
'''
