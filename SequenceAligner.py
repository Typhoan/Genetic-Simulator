'''

Created on Apr 4, 2015

@author: Alexander Calvert

'''
import os
import DNAFileDict
import tempfile
from ctypes import *
from subprocess import *

'''
custom exception for Clustal Omega failures
'''
class ClustalOmegaError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)  

'''
class to perform sequence alignment and related operations
'''
class SequenceAligner:

    '''
    constructor
    note: either libalign.so must be in the same directory as this file, or libalign.so's path must
    be passed as an argument to __init__
    '''
    def __init__(self, libAbsPath=None):
        self._lib = None
        if libAbsPath == None:
            try:
                self._lib = CDLL(os.path.join(os.path.abspath(os.path.dirname(__file__)), "libalign.so"))
            except:
                raise ValueError("could not find libalign.so in current directory " + os.path.join(os.path.abspath(os.path.dirname(__file__))))
        else:
            try:
                self._lib = CDLL(libAbsPath)
            except:
                raise ValueError("could not find libalign.so in " + libAbsPath)

    '''
    get a list of distances from sequences to a dominant sequence

    @param alignedSequences - list of sequence for distance calculation, assumed to be already aligned
    @return distanceMatrix - the distance matrix as a Python list
    '''
    def getDistanceMatrix(self, alignedSequences):
        ''' get list of distances between dominant and subdominant sequences'''
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
        if domName not in alignedSeqs.keys():
            raise ValueError("dominant sequence is not in the sequence matrix")
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
    private method to get the length of the longest string in a list of strings
    
    @param listOfLists - list of strings (or lists, actually) to search
    @return the longest length
    '''
    def _getLongestLength(self, listOfLists):
        ''' gets length of longest list from a list of lists '''
        max = -1
        for list in listOfLists:
            if len(list) > max:
                max = len(list)
        return max
    '''
    private method use to convert values returned form libalign into a dict

    @param domName - name of the dominant sequence
    @param seqMatrix - the unaligned sequences as a name->seq dict
    @numbers - the numbers returned by libalign for the given sequence matrix
    '''
    def _getAlignmentsFromAlignmentNumbers(self, domName, seqMatrix, numbers):
        ''' convert returned number from libalign.so function to a list of aligned sequences '''
        seqs =  dict()
        domSeq = seqMatrix[domName]
        subdomSeqs = dict(seqMatrix)
        del subdomSeqs[domName]

        longestSubLen = self._getLongestLength(subdomSeqs.values())
        numStartDashes = longestSubLen - 1
        numEndDashes = longestSubLen - 1

        dom = ["-"] * (2*longestSubLen + len(domSeq) - 2)
        dom[longestSubLen-1:longestSubLen+len(domSeq)-1] = domSeq
        seqs[domName] = ''.join(dom)

        for name, seq in subdomSeqs.iteritems():
            s = ["-"] * (2*longestSubLen + len(domSeq) - 2)
            s[longestSubLen-len(seq)+numbers[name]:longestSubLen+numbers[name]] = seq
            seqs[name] = ''.join(s)
            if(longestSubLen-len(seq)+numbers[name] < numStartDashes):
                numStartDashes = longestSubLen-len(seq)+numbers[name]
            if((longestSubLen+len(domSeq)-2-numbers[name]) < numEndDashes):
                numEndDashes = longestSubLen+len(domSeq)-2-numbers[name]
        return {name:seq[numStartDashes:len(seq)-numEndDashes] for name, seq in seqs.iteritems()}

    '''
    old alignment algorithm - essentially repeated pairwise alignment with no gaps breaking up sequences
    
    @param domName - the name of the dominant sequence
    @param seqMatrix - the sequence matrix as a name->seq dict
    @returns a name->seq dict of the aligned sequences
    '''
    def alignSequencesUngapped(self, domName, seqMatrix):
        ''' use libalign.so to align sequences to a dominant sequence '''
        if domName not in seqMatrix.keys():
            raise ValueError("dominant sequence is not in the sequence matrix")
        nums = dict()
        domSeq = seqMatrix[domName]
        for name, seq in seqMatrix.iteritems():
            nums[name] = self._lib.alignSequencePair(c_char_p(domSeq), c_char_p(seq))
        alignment = self._getAlignmentsFromAlignmentNumbers(domName, seqMatrix, nums)
        return alignment


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
            try:
                output = check_output(["clustalo", "-i", fastaIn.name, "--outfmt=fasta"])
            except CalledProcessError:
                raise ClustalOmegaError("Clustal Omega returned non-zero status")
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


sample = dict()
sample["s1"] = "AAGAGACACACGGATTATAGAC"
sample["s2"] = "TTTGGGGGGGGCCCTTTATAAT"
sample["s3"] = "GGGTAAACCACACACATGTGTT"
sample["s4"] = "ATTTTGGGGTATATACCCCCCC"
sample["s5"] = "GGGGGGGGGGGCCCTTATTTAG"
a = SequenceAligner()
seqs = a.alignSequencesUngapped("s1", sample)
for n, s in seqs.iteritems(): print n, s
'''


