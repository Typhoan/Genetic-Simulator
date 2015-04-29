'''
Created on Feb 23, 2015

@author: Jordan Hutcheson
@contact: jmh0049@auburn.edu

@version: 0.1 - First version that is just getting feet wet
'''
import unittest
from src.DNAFileDict import DNAFileDict


class TestDNAFileDictTest(unittest.TestCase):


    def testInitSuccess01(self):
        dict = DNAFileDict("DNA.txt")
        self.assertEqual(dict.fileName, "DNA.txt")
        
    def testCheckNumNamesAndNucleotidesSuccess(self):
        list1 = [1,2,3]
        list2 = [4,5,6]
        dict = DNAFileDict("DNA.txt")
        self.assertEquals(dict.checkNumNamesAndNucleotides(list1, list2), True)
        
    def testCheckNumNamesAndNucleotidesFailure(self):
        list1 = [1,2]
        list2 = [4,5,6]
        dict = DNAFileDict("DNA.txt")
        self.assertEquals(dict.checkNumNamesAndNucleotides(list1, list2), False)
        
    def testCheckCorrectFileFormatSuccess(self):
        dict = DNAFileDict("DNA.txt")
        dict.checkCorrectFileFormat("DNA.txt")
        
    def testCheckCorrectFileFormatFailure(self):
        dict = DNAFileDict("BadDNA.txt")
        self.assertEquals(dict.checkCorrectFileFormat("BadDNA.txt"), False)
    
    def testSetListsBadFile(self):
        dict = DNAFileDict("nope.txt")
        self.assertEquals(dict.setLists(), "IOError: File by that directory not found. Please try again.")
    
    def testSetListsGoodFile(self):
        dict = DNAFileDict("DNA.txt")
        dict.setLists()
        self.assertEquals(dict.objectDict.keys(), ["Pig", "Frog"])
        
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
