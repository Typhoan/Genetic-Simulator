
class SequenceAligner():

	def __init__(self):
		pass

	def _getLongestLength(self, listOfLists):
		""" gets length of longest list from a list of lists """
		maxVal = -1
		for alist in listOfLists:
			if len(alist) > maxVal:
				maxVal = len(alist)
		return maxVal
		
	def _advanceList(self, insertedList):
		""" shifts all non-dash characters to the right by one, overwriting dash characters if necessary """
		newList = ["-"] * len(insertedList)
		for i in range(len(insertedList) - 1):
			newList[i + 1] = insertedList[i]
		return newList
		
	def _getNumberOfAlignedNucleotides(self, dominant, subdominant):
		""" gets the number of aligned nucleotides in two already-aligned sequences """
		numAligned = 0
		for i in range(len(dominant)):
			if dominant[i] is not "-" and subdominant[i] is not "-":
				if dominant[i] == subdominant[i]:
					numAligned += 1
		return numAligned
	
	def alignSequences(self, dominantSequenceIn, sequenceMatrixIn):
		"""
			takes a dominant sequence as a string and sequences to be aligned with it
			as a list of strings and returns a list of strings, having the dominant 
			sequence (with dashes) in position 0 and the aligned other sequences (with dashes)
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
		dominantSeq = ["-"] * (2*longestSubdominantSequenceLength + dominantSequenceLength - 2)
		subdominantSequences = []
		for i in range(len(sequenceMatrix)):
			subdominantSequences.append(["-"] * (2*longestSubdominantSequenceLength + dominantSequenceLength - 2))
		# copy the sequences into the lists appropriately
		for i in range(longestSubdominantSequenceLength - 1, longestSubdominantSequenceLength - 1 + dominantSequenceLength - 1):
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
	
	def _getNumberOfDashes(self, string):
		num = 0
		for char in string:
			if char is "-":
				num += 1
		return num
	
	def getDistanceMatrix(self, alignedSequences):
		dominantAlignedSequence = alignedSequences[0]
		subdominantAlignedSequences = alignedSequences[1:]
		distanceMatrix = []
		for seq in subdominantAlignedSequences:
			distanceMatrix.append(len(seq) - self._getNumberOfDashes(seq) - self._getNumberOfAlignedNucleotides(dominantAlignedSequence, seq))
		return distanceMatrix
		
	def generateDotMatrix(self, alignedSequences):
		dominantAlignedSequence = alignedSequences[0]
		subdominantAlignedSequences = alignedSequences[1:]
		dotMatrix = []
		for sequence in subdominantAlignedSequences:
			listCopy = list(sequence)
			for i in range(len(sequence)):
				if not sequence[i] == "-" and not dominantAlignedSequence[i] == "-":
					if sequence[i] == dominantAlignedSequence[i]:
						listCopy[i] = "."
				else:
					listCopy[i] = "-"
			dotMatrix.append(''.join(listCopy))
		dotMatrix.insert(0, dominantAlignedSequence)
		return dotMatrix
	
	
# aligner = SequenceAligner()
	
# majorSample = "TAGCTGATGCTGACTAGAAAGCTTGC"
# sample = []
# sample.append("TGGCTGTAGCTGTAATAAAATGTTTG")
# sample.append("AGGGCTGTATTATATATGATTAAGTA")
# sample.append("TTATCCGCGTCGTATCTTTTTAGTAG")
# sample.append("GATCTGTGTGTGSAATATATATAAAA")
# sample.append("GGATTACCTCGCGGAGACTAGCTCGT")
# sample.append("GGATCATCGTATCGTGATCGTCTAGC")
# seqs = aligner.alignSequences(majorSample, sample)
# for seq in seqs:
	# print seq
# print aligner.getDistanceMatrix(seqs)
# seqs = aligner.generateDotMatrix(seqs)
# for seq in seqs:
	# print seq
