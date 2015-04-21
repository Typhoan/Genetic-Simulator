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
    
    @param dominantName - the name of the dominant sequence
    @param alignedSequences - the aligned sequences as a name->seq dict
    @return dotMatrix - the dot matrix as a name->seq dict
    '''
    def generateDotMatrix(self, domName, alignedSeqs):
        dotMatrix = dict()

        #get copy of the alignment and remove dominant sequence from it
        alignedCopy = dict(alignedSeqs)
        del alignedCopy[domName]
        domSeq = alignedSeqs[domName]

        #get the dotted string for each subdominant sequence and add it to the dot matrix dict by name
        for name, seq in alignedCopy.iteritems():
            seqList = list(seq)
            for i in range(len(seq)):
                if seqList[i] != "-" and domSeq[i] != "-" and seqList[i] == domSeq[i]:
                    seqList[i] = "."
            dotMatrix[name] = ''.join(seqList)

        #be sure dominant is in dot matrix and return
        dotMatrix[domName] = domSeq
        return dotMatrix


    '''
    performs a multiple alignment on a list of sequences using Clustal Omega

    @param seqMatrix - the sequence matrix (a name->seq dict) containing all of the sequences to be aligned
    @return returns the aligned sequences as a name->seq dict with gaps
    '''
    def alignSequences(self, seqMatrix):
        fastaIn = tempfile.NamedTemporaryFile()
        fastaOut = tempfile.NamedTemporaryFile()
        with tempfile.NamedTemporaryFile() as fastaIn, tempfile.NamedTemporaryFile() as fastaOut:
            for name, seq in seqMatrix.iteritems():
                fastaIn.write(">" + name + "\n")
                fastaIn.write(seq + "\n")
            fastaIn.seek(0)
            output = check_output(["clustalo", "-i", fastaIn.name, "--outfmt=fasta"])
            fastaOut.write(output)
            fastaOut.seek(0)
            dout = DNAFileDict.DNAFileDict(fastaOut.name)
            dout.setLists()
            return dout.getDNADict()
           
'''
sample = dict()
sample["s1"] = "TTTTTTTT"
sample["s2"] = "TTTTTTTTTTT"
sample["s3"] = "TTTTTTGGGTT"
a = SequenceAligner()
seqs = a.alignSequences(sample)
for k, v in seqs.iteritems(): print k, v
print ""
seqs = a.generateDotMatrix("s1", seqs)
for k, v in seqs.iteritems(): print k, v
'''

