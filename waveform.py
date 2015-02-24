# Initial commit				Alexander Calvert, 2/19/2015
# documentation added				Alesander Calvert, 2/24/2015
# 
# 

import random
import matplotlib.pyplot as plt

def generateWaveform(sequence):
	""" 
	returns four lists of values representing the y-values of LCMM waveforms, 
	each corresponding to a different nucleotide
	"""
	random.seed()
	waveA = []
	waveT = []
	waveG = []
	waveC = []
	for nucleotide in sequence:
		if nucleotide is "A":
			waveA.extend([0.2, 0.45, 0.7, 1 + ((random.random() - 0.5)/4), 0.7, 0.45, 0.2])
			waveT.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
			waveG.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
			waveC.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
		if nucleotide is "T":
			waveA.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
			waveT.extend([0.2, 0.45, 0.7, 1 + ((random.random() - 0.5)/4), 0.7, 0.45, 0.2])
			waveG.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
			waveC.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
		if nucleotide is "G":
			waveA.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
			waveT.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
			waveG.extend([0.2, 0.45, 0.7, 1 + ((random.random() - 0.5)/4), 0.7, 0.45, 0.2])
			waveC.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
		if nucleotide is "C":
			waveA.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
			waveT.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
			waveG.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
			waveC.extend([0.2, 0.45, 0.7, 1 + ((random.random() - 0.5)/4), 0.7, 0.45, 0.2])
	return [waveA, waveT, waveG, waveC]
	
	
#testing stuff
seq = "ATCAGGCGAGAGAGTGCTGATTAGGCGTCTCTCTAGATCGGGGGGCTTATATGCTTTTATGAGATCATATAGCTA"
wave = generateWaveform(seq)
import sys
for i in range(0, len(wave)):
	plt.plot(wave[i])
plt.show()




	
