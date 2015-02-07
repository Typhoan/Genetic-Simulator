
class SequenceAligner():

	def __init__(self):
		pass

	def _getLongestLength(self, listOfLists):
		""" gets length of longest list from a list of lists """
		max = -1
		for list in listOfLists:
			if len(list) > max:
				max = len(list)
		return max
		
	def _advanceList(self, list):
		""" shifts all non-dash characters to the right by one, overwriting dash characters if necessary """
		newList = ["-"] * len(list)
		for i in range(len(list) - 1):
			newList[i + 1] = list[i]
		return newList
		
	def _getNumberOfAlignedNucleotides(self, dominant, subdominant):
		""" gets the number of aligned nucleotides geven to already-aligned sequences """
		numAligned = 0
		for i in range(len(dominant)):
			if dominant[i] is not "-" and subdominant[i] is not "-":
				if dominant[i] == subdominant[i]:
					numAligned += 1
		return numAligned
	
	def alignSequences(self, dominantSequenceIn, sequenceMatrixIn):
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
	
	def _getNumberOfDashes(self, str):
		num = 0
		for char in str:
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
				if sequence[i] is not "-" and dominantAlignedSequence[i] is not "-":
					if sequence[i] == dominantAlignedSequence[i]:
						listCopy[i] = "."
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
