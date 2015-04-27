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



# alignSequences

    def test200_900_ShouldFailEmptyDominant(self):

        aligner = sa.SequenceAligner()

	self.assertRaises(ValueError, aligner.alignSequences, "", ["ATGCC", "GTACA"])

    

    def test201_100_ShouldReturnListOfOnlyDominant(self):

        aligner = sa.SequenceAligner()

        domIn = "ATGCA"

        seqmatIn = []

        out = ["ATGCA"]

	self.assertEquals(aligner.alignSequences(domIn, seqmatIn), out)



    def test202_100_ShouldReturnGoodMatrixBorder1(self):

        aligner = sa.SequenceAligner()

        domIn = "A"

        seqmatIn = ["A"]

        out = ["A", "A"]

	self.assertEquals(aligner.alignSequences(domIn, seqmatIn), out)



    def test203_100_ShouldReturnGoodMatrixBorder2(self):

        aligner = sa.SequenceAligner()

        domIn = "A"

        seqmatIn = ["ATGCT"]

        out = [ "A    ", 

                "ATGCT" ]

	self.assertEquals(aligner.alignSequences(domIn, seqmatIn), out)



    def test204_100_ShouldReturnGoodMatrixBorder3(self):

        aligner = sa.SequenceAligner()

        domIn = "A"

        seqmatIn = ["A", "A", "A", "A", "A"]

        out = [ "A", 

                "A", 

                "A",

                "A",

                "A",

                "A" ]

	self.assertEquals(aligner.alignSequences(domIn, seqmatIn), out)



    def test205_100_ShouldReturnGoodMatrixBorder4(self):

        aligner = sa.SequenceAligner()

        domIn = "ATCGT"

        seqmatIn = ["G"]

        out = [ "ATCGT", 

                "   G " ]

	self.assertEquals(aligner.alignSequences(domIn, seqmatIn), out)



    def test206_100_ShouldReturnGoodMatrixBorder5(self):

        aligner = sa.SequenceAligner()

        domIn = "A"

        seqmatIn = ["ATGCT", "TGACG", "GGTAC", "AGTCC", "AGTCC"]

        out = [ "   A    ", 

                "   ATGCT",

                " TGACG  ", 

                "GGTAC   ", 

                "   AGTCC", 

                "   AGTCC"]

	self.assertEquals(aligner.alignSequences(domIn, seqmatIn), out)



    def test207_100_ShouldReturnGoodMatrixBorder6(self):

        aligner = sa.SequenceAligner()

        domIn = "ATGGC"

        seqmatIn = ["TTGCA"]

        out = [ "ATGGC ", 

                " TTGCA" ]

	self.assertEquals(aligner.alignSequences(domIn, seqmatIn), out)



    def test208_100_ShouldReturnGoodMatrixBorder7(self):

        aligner = sa.SequenceAligner()

        domIn = "GATCC"

        seqmatIn = ["A", "G", "A", "T", "A"]

        out = [ "GATCC", 

                " A   ", 

                "G    ", 

                " A   ", 

                "  T  ", 

                " A   " ]

	self.assertEquals(aligner.alignSequences(domIn, seqmatIn), out)



    def test209_100_ShouldReturnGoodMatrixBorder8(self):

        aligner = sa.SequenceAligner()

        domIn = "GATCC"

        seqmatIn = ["AGTCC", "GTCAA", "ATACG", "TATCT", "AGAAA"]

        out = [ " GATCC ", 

                " AGTCC ", 

                "  GTCAA", 

                "  ATACG", 

                " TATCT ", 

                "AGAAA  " ]

	self.assertEquals(aligner.alignSequences(domIn, seqmatIn), out)



    def test210_100_ShouldNotTakeMoreThanTwelveSecondsToRunOnLargeInput(self):

        aligner = sa.SequenceAligner()

	domIn = createSequence(5000)

	seqmatIn = []

	for i in range(15):

		seqmatIn.append(createSequence(5000))

	start = time.time()

	aligner.alignSequences(domIn, seqmatIn)

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

        seqmatIn = ["   ATGCAT ",

                    "  AAAGCA  " ]

        out = [2]

        self.assertEquals(aligner.getDistanceMatrix(seqmatIn), out)



    def test304_100_ShouldReturnGoodDistanceMatrixBorder3(self):

        aligner = sa.SequenceAligner()

        seqmatIn = ["   ATGCAT ",

                    "  AAAGCA  ", 

                    "  CGATTGC ",

                    "     GGGGG",

                    "AAATAAATAA" ]

        out = [2, 7, 4, 10]

        self.assertEquals(aligner.getDistanceMatrix(seqmatIn), out)



# generateDotMatrix

    def test400_900_ShouldFailOnEmptySequenceMatrix(self):

        aligner = sa.SequenceAligner()

        self.assertRaises(ValueError, aligner.generateDotMatrix, [])



    def test401_100_ShouldReturnListEqualToInput(self):

        aligner = sa.SequenceAligner()

        seqmatIn = ["AGTCA"]

        out = ["AGTCA"]

        self.assertEquals(aligner.generateDotMatrix(seqmatIn), out)



    def test402_100_ShouldReturnGoodDotMatrixBorder1(self):

        aligner = sa.SequenceAligner()

        seqmatIn = ["A",

                    "A" ]

        out = ["A",

               "."]

        self.assertEquals(aligner.generateDotMatrix(seqmatIn), out)



    def test403_100_ShouldReturnGoodDotMatrixBorder2(self):

        aligner = sa.SequenceAligner()

        seqmatIn = [" ATGCAT",

                    "AAAGCA " ]

        out = [" ATGCAT", 

               "A.A... " ]

        self.assertEquals(aligner.generateDotMatrix(seqmatIn), out)



    def test404_100_ShouldReturnGoodDotMatrixBorder3(self):

        aligner = sa.SequenceAligner()

        seqmatIn = ["   ATGCAT ",

                    "  AAAGCA  ", 

                    "  CGATTGC ",

                    "     GGGGG",

                    "AAAATGCATA" ]

        out = ["   ATGCAT ",

               "  A.A...  ", 

               "  CGATTGC ",

               "     .GGGG",

               "AAA......A" ]

        self.assertEquals(aligner.generateDotMatrix(seqmatIn), out)



    def test405_100_ShouldReturnGoodDotMatrixAminoAcids(self):

        aligner = sa.SequenceAligner()

        seqmatIn = ["FLMV*AASTPPL",

                    "FL*VVASSTAPL",

                    "LLLLLLSSSSSS",

                    "SLSL*AALSAM*",

                    "MM**M*VVVLLA" ]

        out = ["FLMV*AASTPPL",

               "..*.V.S..A..",

               "L.LLLLS.SSSS",

               "S.SL...LSAM*",

               "MM**M*VVVLLA" ]

        self.assertEquals(aligner.generateDotMatrix(seqmatIn), out)



if __name__ == '__main__':

    unittest.main()





