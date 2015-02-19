import random

def generateWaveform(sequence):
	random.seed()
	waveA = []
	waveT = []
	waveG = []
	waveC = []
	for nucleotide in sequence:
		if nucleotide is "A":
			waveA.extend([0.2, 0.45, 0.7, 1 + ((random.random() - 0.5)/4), 0.7, 0.45, 0.2])
			waveT.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
			waveG.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
			waveC.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
		if nucleotide is "T":
			waveA.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
			waveT.extend([0.2, 0.45, 0.7, 1 + ((random.random() - 0.5)/4), 0.7, 0.45, 0.2])
			waveG.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
			waveC.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
		if nucleotide is "G":
			waveA.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
			waveT.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
			waveG.extend([0.2, 0.45, 0.7, 1 + ((random.random() - 0.5)/4), 0.7, 0.45, 0.2])
			waveC.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
		if nucleotide is "C":
			waveA.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
			waveT.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
			waveG.extend([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
			waveC.extend([0.2, 0.45, 0.7, 1 + ((random.random() - 0.5)/4), 0.7, 0.45, 0.2])
	return [waveA, waveT, waveG, waveC]
	
seq = "ATCAGGCGAGAGA"
wave = generateWaveform(seq)
import sys
for i in range(0, len(wave)):
	for j in range(0, 20):
		sys.stdout.write(str(round(wave[i][j], 1)) + " "),
	print ''
	
