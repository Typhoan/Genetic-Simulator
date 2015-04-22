import unittest
import os
import random
import time
import SequenceAligner as sa

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

class SequenceAlignerConstructorTest(unittest.TestCase):
# __init__
    #should only run if path the script is running in contains libalign.so
    @unittest.skipUnless(os.path.isfile("libalign.so"), "default path intentionally incorrect - only run when correct")
    def test100_100_ShouldCreateObjectNoPathGiven(self):
        self.assertIsInstance(sa.SequenceAligner(), sa.SequenceAligner)

    #should only run if the given path contains libalign.so
    @unittest.skipUnless(os.path.isfile("/home/alexander/Desktop/libs/libalign.so"), "given path intentionally incorrect - only run when correct")
    def test101_100_ShouldCreateObjectPathGiven(self):
        self.assertIsInstance(sa.SequenceAligner("/home/alexander/Desktop/libs/libalign.so"), sa.SequenceAligner)

    #should only run if the path the script is running in does not contain libalign.so - expect failure
    @unittest.skipUnless(not os.path.isfile("libalign.so"), "default path intentionally correct - only run when incorrect")
    def test102_900_ShouldFailNoPathGiven(self):
        self.assertRaises(ValueError, sa.SequenceAligner)

    #should only run if the given path does not contain libalign.so - expect failure
    @unittest.skipUnless(not os.path.isfile("/home/alexander/Desktop/libs/libalign.so"), "given path intentionally correct - only run when incorrect")
    def test103_900_ShouldFailPathGiven(self):
        self.assertRaises(ValueError, sa.SequenceAligner, "/home/alexander/Desktop/libs/libalign.so")

@unittest.skipUnless(os.path.isfile("libalign.so"), "default path intentionally incorrect - only run when correct")
class SequenceAlignerTest(unittest.TestCase):

# alignSequencesUngapped    
    def test201_100_ShouldFailDominantNotPresent(self):
        aligner = sa.SequenceAligner()
	self.assertRaises(ValueError, aligner.alignSequencesUngapped, "s3", {"s1":"AGTC", "s2":"ATGC"})

    def test202_100_ShouldReturnGoodMatrixBorder1(self):
        aligner = sa.SequenceAligner()
        domIn = "s1"
        seqmatIn = {"s1":"A"}
        out = {"s1":"A"}
	self.assertEquals(aligner.alignSequencesUngapped(domIn, seqmatIn), out)

    def test203_100_ShouldReturnGoodMatrixBorder2(self):
        aligner = sa.SequenceAligner()
        domIn = "s1"
        seqmatIn = {"s1":"A", "s2":"ATGCT"}
        out = { "s1":"A----", 
                "s2":"ATGCT" }
	self.assertEquals(aligner.alignSequencesUngapped(domIn, seqmatIn), out)

    def test204_100_ShouldReturnGoodMatrixBorder3(self):
        aligner = sa.SequenceAligner()
        domIn = "s1"
        seqmatIn = {"s1":"A", "s2":"A", "s3":"A", "s4":"A", "s5":"A"}
        out = { "s1":"A", 
                "s2":"A", 
                "s3":"A",
                "s4":"A",
                "s5":"A" }
	self.assertEquals(aligner.alignSequencesUngapped(domIn, seqmatIn), out)

    def test205_100_ShouldReturnGoodMatrixBorder4(self):
        aligner = sa.SequenceAligner()
        domIn = "s1"
        seqmatIn = {"s1":"ATCGT", "s2":"G"}
        out = { "s1":"ATCGT", 
                "s2":"---G-" }
	self.assertEquals(aligner.alignSequencesUngapped(domIn, seqmatIn), out)

    def test206_100_ShouldReturnGoodMatrixBorder5(self):
        aligner = sa.SequenceAligner()
        domIn = "s1"
        seqmatIn = {"s1":"A", "s2":"ATGCT", "s3":"TGACG", "s4":"GGTAC", "s5":"AGTCC", "s6":"AGTCC"}
        out = { "s1":"---A----", 
                "s2":"---ATGCT",
                "s3":"-TGACG--", 
                "s4":"GGTAC---", 
                "s5":"---AGTCC", 
                "s6":"---AGTCC"}
        #for k, v in out.iteritems(): print k, v
        #for k, v in aligner.alignSequencesUngapped(domIn, seqmatIn).iteritems(): print k, v
	self.assertEquals(aligner.alignSequencesUngapped(domIn, seqmatIn), out)

    def test207_100_ShouldReturnGoodMatrixBorder6(self):
        aligner = sa.SequenceAligner()
        domIn = "s1"
        seqmatIn = {"s1":"ATGGC", "s2":"TTGCA"}
        out = { "s1":"ATGGC-", 
                "s2":"-TTGCA" }
	self.assertEquals(aligner.alignSequencesUngapped(domIn, seqmatIn), out)

    def test208_100_ShouldReturnGoodMatrixBorder7(self):
        aligner = sa.SequenceAligner()
        domIn = "s1"
        seqmatIn = {"s1":"GATCC", "s2":"A", "s3":"G", "s4":"A", "s5":"T", "s6":"A"}
        out = { "s1":"GATCC", 
                "s2":"-A---", 
                "s3":"G----", 
                "s4":"-A---", 
                "s5":"--T--", 
                "s6":"-A---" }
	self.assertEquals(aligner.alignSequencesUngapped(domIn, seqmatIn), out)

    def test209_100_ShouldReturnGoodMatrixBorder8(self):
        aligner = sa.SequenceAligner()
        domIn = "s1"
        seqmatIn = {"s1":"GATCCC", 
                    "s2":"AGTCC", 
                    "s3":"GTCAA", 
                    "s4":"ATACG", 
                    "s5":"TATCT", 
                    "s6":"AGAAA"}
        out = { "s1":"-GATCCC", 
                "s2":"-AGTCC-", 
                "s3":"--GTCAA", 
                "s4":"--ATACG", 
                "s5":"-TATCT-", 
                "s6":"AGAAA--" }
	self.assertEquals(aligner.alignSequencesUngapped(domIn, seqmatIn), out)

    def test210_100_ShouldNotTakeMoreThanTwelveSecondsToRunOnLargeInput(self):
        aligner = sa.SequenceAligner()
	seqmatIn = dict()
	for i in range(16):
		seqmatIn["s"+ str(i)] = createSequence(5000)
	start = time.time()
	aligner.alignSequencesUngapped("s0", seqmatIn)
	total = time.time() - start
	self.assertLessEqual(total, 12)
   
# getDistanceMatrix
    def test300_900_ShouldFailOnEmptySequenceMatrix(self):
        aligner = sa.SequenceAligner()
        self.assertRaises(ValueError, aligner.getDistanceMatrix, [])

    def test301_100_ShouldReturnEmptyList(self):
        aligner = sa.SequenceAligner()
        seqmatIn = ["AGTCA"]
        out = []
        self.assertEquals(aligner.getDistanceMatrix(seqmatIn), out)

    def test302_100_ShouldReturnGoodDistanceMatrixBorder1(self):
        aligner = sa.SequenceAligner()
        seqmatIn = ["A",
                    "A" ]
        out = [0]
        self.assertEquals(aligner.getDistanceMatrix(seqmatIn), out)

    def test303_100_ShouldReturnGoodDistanceMatrixBorder2(self):
        aligner = sa.SequenceAligner()
        seqmatIn = ["---ATGCAT-",
                    "--AAAGCA--" ]
        out = [3]
        self.assertEquals(aligner.getDistanceMatrix(seqmatIn), out)

    def test304_100_ShouldReturnGoodDistanceMatrixBorder3(self):
        aligner = sa.SequenceAligner()
        seqmatIn = ["---ATGCAT-",
                    "--AAAGCA--", 
                    "--CGATTGC-",
                    "-----GGGGG",
                    "AAATAAATAA" ]
        out = [3, 7, 6, 10]
        self.assertEquals(aligner.getDistanceMatrix(seqmatIn), out)

# generateDotMatrix
    def test401_100_ShouldFailOnDominantNotPresent(self):
        aligner = sa.SequenceAligner()
        self.assertRaises(ValueError, aligner.generateDotMatrix, "s3", {"s1":"AGTC", "s2":"ATGC"})

    def test402_100_ShouldReturnGoodDotMatrixBorder1(self):
        aligner = sa.SequenceAligner()
        domIn = "s1"
        seqmatIn = {"s1":"A",
                    "s2":"A"}
        out = {"s1":"A",
               "s2":"."}
        self.assertEquals(aligner.generateDotMatrix(domIn, seqmatIn), out)

    def test403_100_ShouldReturnGoodDotMatrixBorder2(self):
        aligner = sa.SequenceAligner()
        domIn = "s1"
        seqmatIn = {"s1":"-ATGCAT",
                    "s2":"AAAGCA-" }
        out = {"s1":"-ATGCAT", 
               "s2":"A.A...-" }
        self.assertEquals(aligner.generateDotMatrix(domIn, seqmatIn), out)

    def test404_100_ShouldReturnGoodDotMatrixBorder3(self):
        aligner = sa.SequenceAligner()
        domIn = "s1"
        seqmatIn = {"s1":"---ATGCAT-",
                    "s2":"--AAAGCA--", 
                    "s3":"--CGATTGC-",
                    "s4":"-----GGGGG",
                    "s5":"AAAATGCATA" }
        out = {"s1":"---ATGCAT-",
               "s2":"--A.A...--", 
               "s3":"--CGATTGC-",
               "s4":"-----.GGGG",
               "s5":"AAA......A" }
        self.assertEquals(aligner.generateDotMatrix(domIn, seqmatIn), out)

    def test405_100_ShouldReturnGoodDotMatrixAminoAcids(self):
        aligner = sa.SequenceAligner()
        domIn = "s1"
        seqmatIn = {"s1":"FLMV*AASTPPL",
                    "s2":"FL*VVASSTAPL",
                    "s3":"LLLLLLSSSSSS",
                    "s4":"SLSL*AALSAM*",
                    "s5":"MM**M*VVVLLA" }
        out = {"s1":"FLMV*AASTPPL",
               "s2":"..*.V.S..A..",
               "s3":"L.LLLLS.SSSS",
               "s4":"S.SL...LSAM*",
               "s5":"MM**M*VVVLLA" }
        self.assertEquals(aligner.generateDotMatrix(domIn, seqmatIn), out)

#alignSequences
    def test500_900_ShouldFailOnEmptySequenceMatrix(self):
        aligner = sa.SequenceAligner()
        self.assertRaises(sa.ClustalOmegaError, aligner.alignSequences, dict())

    def test501_900_ShouldFailOnOnlyOneSequence(self):
        aligner = sa.SequenceAligner()
        seqmatIn = {"s1":"A"}
        self.assertRaises(sa.ClustalOmegaError, aligner.alignSequences, seqmatIn)        

    def test502_100_ShouldAlignSequencesBorder1(self):
        aligner = sa.SequenceAligner()
        seqmatIn = {"s1":"A", 
                    "s2":"T", 
                    "s3":"T", 
                    "s4":"A", 
                    "s5":"G"}
        out = {"s1":"A", 
               "s2":"T", 
               "s3":"T", 
               "s4":"A", 
               "s5":"G"}
        self.assertEquals(aligner.alignSequences(seqmatIn), out)

    def test503_100_ShouldAlignSequencesBorder2(self):
        aligner = sa.SequenceAligner()
        seqmatIn = {"s1":"AAGGTTTAAAC", 
                    "s2":"TTTTCTTTAAT", 
                    "s3":"TGCTTGGGGGG", 
                    "s4":"AGGGGTAGGAA", 
                    "s5":"GGGAGCCCATG"}
        out = {"s1":"-AAGGTTTAAAC-", 
               "s2":"TTTTCTTTAAT--", 
               "s3":"--TGCTTGGGGGG", 
               "s4":"--AGGGGTAGGAA", 
               "s5":"-GGGAGCCCATG-"}
        self.assertEquals(aligner.alignSequences(seqmatIn), out)

if __name__ == '__main__':
    unittest.main()


