'''
Created on Feb 21, 2015

@author: Ian McPherson
'''
import src.SequenceTranslation as seqTrans
import unittest

class SequenceTranslationTest(unittest.TestCase):
    
    def test01DNAToRNA(self):
        expectedString = "UUUAAAGGGCCC"
        seq = "AAATTTCCCGGG"
        self.assertEquals(expectedString, seqTrans.DNAToRNA(seq))
    
    def test02DNAToRNAInvalidSequence(self):
        expectedString = "DNAToRNA:  Invalid nucleotide"
        try:
            seq = "AAATTTCCCGUG"
            rna = seqTrans.DNAToRNA(seq)
            self.fail("ValueError exception was not raised")
        except ValueError as raisedException:
            raisedString = raisedException.args[0]
            self.assertEquals(expectedString, raisedString[0:len(expectedString)])
        except:
            self.fail("Incorrect exception was raised")
    
    def test03RNAToDNA(self):
        seq = "UUUAAAGGGCCC"
        expectedString = "AAATTTCCCGGG"
        self.assertEquals(expectedString, seqTrans.RNAToDNA(seq))
    
    def test04RNAToDNAInvalidSequence(self):
        expectedString = "RNAToDNA:  Invalid nucleotide"
        try:
            seq = "UTUAAAGGGCCC"
            rna = seqTrans.RNAToDNA(seq)
            self.fail("ValueError exception was not raised")
        except ValueError as raisedException:
            raisedString = raisedException.args[0]
            self.assertEquals(expectedString, raisedString[0:len(expectedString)])
        except:
            self.fail("Incorrect exception was raised")
    
    def test05RNAToProtien(self):
        seq = "UUUAAAGGGCCC"
        expectedString = "FKGP"
        self.assertEquals(expectedString, seqTrans.RNAToProtien(seq))
    
    def test06RNAToProteinInvalidSequence(self):
        expectedString = "RNAToProtien:  Invalid codon"
        try:
            seq = "UKUAAAGGGCCC"
            protien = seqTrans.RNAToProtien(seq)
            self.fail("ValueError exception was not raised")
        except ValueError as raisedException:
            raisedString = raisedException.args[0]
            self.assertEquals(expectedString, raisedString[0:len(expectedString)])
        except:
            self.fail("Incorrect exception was raised")
            
    def test07ReverseDNA(self):
        seq = "TTTAAAGGGCCC"
        expectedString = "AAATTTCCCGGG"
        self.assertEquals(expectedString, seqTrans.reverseDNA(seq))
