# Initial commit 						Alexander Calvert, 2/19/2015
# documentation added 					Alexander Calvert, 2/24/2015
# added exportWaveformImage function	Alexander Calvert, 2/26/2015
# 

import sys
import os
import random
import math
import matplotlib.pylab as pylab
import matplotlib.pyplot as pyplot
#from scipy import interpolate
import numpy as np

def generateWaveform(sequence):
	""" generate LCMM waveforms for A/T/G/C nucleotides and return as list of floats """
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
			waveG.extend([0.2, 0.45, 0.7, 1.1 + ((random.random() - 0.5)/4), 0.7, 0.45, 0.2])
			waveC.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
		if nucleotide is "C":
			waveA.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
			waveT.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
			waveG.extend([(random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10), (random.random()/10)])
			waveC.extend([0.2, 0.45, 0.7, 1 + ((random.random() - 0.5)/4), 0.7, 0.45, 0.2])
	return (waveA, waveT, waveG, waveC)
	
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
	return list

def exportWaveformImage(sequence, filename, colorA, colorT, colorG, colorC):
	""" 
	generate waveform and export it as an image; if sequence length > 500, export multiple
	images to accommodate large size
	"""
	maxSeqLen = 500
	colors = {
		"A" : colorA,
		"T" : colorT,
		"G" : colorG,
		"C" : colorC,
	}
	if len(sequence) <= maxSeqLen:
		wave = generateWaveform(sequence)
		pyplot.plot(wave[0], color=colors.get("A"))
		pyplot.plot(wave[1], color=colors.get("T"))
		pyplot.plot(wave[2], color=colors.get("G"))
		pyplot.plot(wave[3], color=colors.get("C"))
		pyplot.axis("off")
		pylab.xlim([0, len(sequence)*7])
		for i, txt in enumerate(sequence):
			pyplot.text(7*i+2, 1.5, txt, color=colors.get(txt, "black"))
		fig = pyplot.gcf()
		fig.set_size_inches(0.5*len(sequence), 2.0)
		fig.savefig(filename, bbox_inches="tight")
	else:
		for i in range(0, len(sequence), maxSeqLen): 
			print i, str(i)
			wave = generateWaveform(sequence[i:i+maxSeqLen])
			pyplot.plot(wave[0], color=colors.get("A"))
			pyplot.plot(wave[1], color=colors.get("T"))
			pyplot.plot(wave[2], color=colors.get("G"))
			pyplot.plot(wave[3], color=colors.get("C"))
			pyplot.axis("off")
			pylab.xlim([0, len(sequence[i:i+maxSeqLen])*7])
			for j, txt in enumerate(sequence[i:i+maxSeqLen]):
				pyplot.text(7*j+2, 1.5, txt, color=colors.get(txt, "black"))
			fig = pyplot.gcf()
			fig.set_size_inches(0.5*len(sequence[i:i+maxSeqLen]), 2.0)
			name, ext = os.path.splitext(filename)
			fig.savefig(name + '-' + str((i/maxSeqLen)+1).zfill(2) + ext, bbox_inches="tight")
			pyplot.clf()
	
	
#seq = "ATCAGGCGAGAGAGTGCTGATTAGGCGTCTCTCTAGATCGGGGGGCTTATATGCTTTTATGAGATCATATAGCTA"
seq = createSequence(1000)
exportWaveformImage(seq, "test.svg", "cyan", "magenta", "yellow", "black")




