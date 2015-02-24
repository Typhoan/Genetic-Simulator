# Initial commit				Alexander Calvert, 2/2/2015
# added documentation				Alexander Calvert, 2/24/2015
# 
# 
# 
# 
# 

import random
import time
import os
from ctypes import *

class SequenceAligner():
"""
class to provide methods for aligning sequences, getting distance matrices, and getting dot matrices
"""
	def __init__(self, libAbsPath=None):
		"""
		constructor
		note: either libalign.so must be in the same directory as this file, or libalign.so's path must
		be passed as an argument to __init__
		"""
		self._lib = None
		if libAbsPath == None:
			self._lib = CDLL(os.path.join(os.path.abspath(os.path.dirname(__file__)), "libalign.so"))
		else:
			self._lib = CDLL(libAbsPath)

	def _getLongestLength(self, listOfLists):
		""" gets length of longest list from a list of lists """
		max = -1
		for list in listOfLists:
			if len(list) > max:
				max = len(list)
		return max
		
	def _advanceList(self, list):
		""" shifts all non-dash characters to the right by one, overwriting dash characters if necessary """
		newList = [" "] * len(list)
		for i in range(len(list) - 1):
			newList[i + 1] = list[i]
		return newList
		
	def _getNumberOfAlignedNucleotides(self, dominant, subdominant):
		""" gets the number of aligned nucleotides geven to already-aligned sequences """
		numAligned = 0
		for i in range(len(dominant)):
			if dominant[i] is not " " and subdominant[i] is not " ":
				if dominant[i] == subdominant[i]:
					numAligned += 1
		return numAligned
	
	def alignSequences_deprecated(self, dominantSequenceIn, sequenceMatrixIn):
		"""
			takes a dominant sequence as a string and sequences to be aligned with it
			as a list of strings and returns a list of of strings with the dominant 
			sequence (with gaps) in position 0 and the aligned other sequences (with gaps)
			in the other positions
		"""
		# get lists from sequence strings
		dominantSequence = list(dominantSequenceIn)
		sequenceMatrix = []
		for seq in sequenceMatrixIn:
			sequenceMatrix.append(list(seq))
		maxNumAligned = -1
		# prepare the empty lists
		longestSubdominantSequenceLength = self._getLongestLength(sequenceMatrix)
		dominantSequenceLength = len(dominantSequence)
		dominantSeq = [" "] * (2*longestSubdominantSequenceLength + dominantSequenceLength - 2)
		subdominantSequences = []
		for i in range(len(sequenceMatrix)):
			subdominantSequences.append([" "] * (2*longestSubdominantSequenceLength + dominantSequenceLength - 2))
		# copy the sequences into the lists appropriately
		for i in range(longestSubdominantSequenceLength - 1, longestSubdominantSequenceLength + dominantSequenceLength - 1):
			dominantSeq[i] = dominantSequence[i - (longestSubdominantSequenceLength - 1)]
		for i in range(len(subdominantSequences)):
			for j in range(len(sequenceMatrix[i])):
				subdominantSequences[i][j] = sequenceMatrix[i][j]

				
		for i in range(len(subdominantSequences)):
			maxNumAligned = -1
			numAligned = -1
			alignedSequence = []
			for j in range(dominantSequenceLength + longestSubdominantSequenceLength - 1):
				numAligned = self._getNumberOfAlignedNucleotides(dominantSeq, subdominantSequences[i])
				if numAligned > maxNumAligned:	
					maxNumAligned = numAligned
					alignedSequence = list(subdominantSequences[i])
				subdominantSequences[i] = self._advanceList(subdominantSequences[i])
			subdominantSequences[i] = list(alignedSequence)
		subdominantSequences.insert(0, dominantSeq)
		allSequences = []
		for seq in subdominantSequences:
			allSequences.append(''.join(seq))
		return allSequences
	
	def _getNumberOfSpaces(self, str):
		""" gets the number of space characters in a string """
		num = 0
		for char in str:
			if char is " ":
				num += 1
		return num
	
	def getDistanceMatrix(self, alignedSequences):
		""" get list of distances between dominant and subdominant sequences"""
		dominantAlignedSequence = alignedSequences[0]
		subdominantAlignedSequences = alignedSequences[1:]
		distanceMatrix = []
		for seq in subdominantAlignedSequences:
			distanceMatrix.append(len(seq) - self._getNumberOfSpaces(seq) - self._getNumberOfAlignedNucleotides(dominantAlignedSequence, seq))
		return distanceMatrix
		
	def generateDotMatrix(self, alignedSequences):
		""" generate dot matrix based on already-aligned sequences """
		dominantAlignedSequence = alignedSequences[0]
		subdominantAlignedSequences = alignedSequences[1:]
		dotMatrix = []
		for sequence in subdominantAlignedSequences:
			listCopy = list(sequence)
			for i in range(len(sequence)):
				if sequence[i] is not " " and dominantAlignedSequence[i] is not " ":
					if sequence[i] == dominantAlignedSequence[i]:
						listCopy[i] = "."
			dotMatrix.append(''.join(listCopy))
		dotMatrix.insert(0, dominantAlignedSequence)
		return dotMatrix

	def _getAlignmentsFromAlignmentNumbers(self, domSeq, subdomSeqs, numbers):
		""" convert returned number from libalign.so function to a list of aligned sequences """
		longestSubLen = self._getLongestLength(subdomSeqs)
		seqs = 	[]
		dom = [" "] * (2*longestSubLen + len(domSeq) - 2)
		dom[longestSubLen-1:longestSubLen+len(domSeq)-1] = domSeq
		seqs.append(''.join(dom))
		numStartDashes = longestSubLen - 1
		numEndDashes = longestSubLen - 1
		for i in range(len(subdomSeqs)):
			s = [" "] * (2*longestSubLen + len(domSeq) - 2)
			s[longestSubLen-len(subdomSeqs[i])+numbers[i]:longestSubLen+numbers[i]] = subdomSeqs[i]
			seqs.append(''.join(s))
			if(longestSubLen-len(subdomSeqs[i])+numbers[i] < numStartDashes):
				numStartDashes = longestSubLen-len(subdomSeqs[i])+numbers[i]
			if((longestSubLen+len(domSeq)-2-numbers[i]) < numEndDashes):
				numEndDashes = longestSubLen+len(domSeq)-2-numbers[i]
		return [s[numStartDashes:len(s)-numEndDashes] for s in seqs]
		
	def alignSequences(self, dominantSeq, seqMatrix):
		""" use libalign.so to align sequences to a dominant sequence """
		nums = []
		for seq in seqMatrix:
			nums.append(self._lib.alignSequencePair(dominantSeq, seq))
		alignment = self._getAlignmentsFromAlignmentNumbers(dominantSeq, seqMatrix, nums)
		return alignment

#testing stuff
def createSequence(len):
	random.seed()
	list = []
	for i in range(0, len):
		rand = random.random();
		if rand < .25:
			list.append("A")
		elif rand < .50:
			list.append("T")
		elif rand < .75:
			list.append("G")
		else:
			list.append("C")
	return ''.join(list)
	
aligner = SequenceAligner()
	
sample = []
#sample.append("GATCGTAGCTGATGCTGTAGTATGCTATCTCGCTTATATAGCTAGCTAGTTAGGC")
#sample.append("AGTCGATTATATTAGCTTAGTCGGCTA")
#sample.append("AGAGCTTTTCTATATTATATAGCTAGCTTATATAGATATATCGGCGCGATGTGTGG")
#sample.append("CGCTCTCGCTCTCGCTCGAGATATACGCGAAATAGCTGATAATCGTCGCC")

for i in range(10):
	sample.append(createSequence(5000))	

#a = aligner.alignSequences_deprecated(sample[0], sample[1:])
#for s in a:
#	print s
#print ""

a = aligner.alignSequences(sample[0], sample[1:])
#print aligner.getDistanceMatrix(a)
for s in a:
	print s


# print aligner.getDistanceMatrix(seqs)
# seqs = aligner.generateDotMatrix(seqs)
# for seq in seqs:
	# print seq
