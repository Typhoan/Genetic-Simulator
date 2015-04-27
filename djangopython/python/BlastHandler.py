'''
Created on Feb 16, 2015

@author: donovan
@author Jordan Hutcheson
@contact email: jhutchesonau9@gmail.com

This class was created to add a little extra, possibly helpful functionality to the DNAStudios
website and to assist with Dr. Wooten's labs. It's purpose is to work as a handler to be able
to recieve from Blast a list of the top alignments with their best hsp's. The handler takes
this and takes the top result of those results and prints it for the user along with a little
extra information that Dr. Wooten wanted. In summary, it returns blast results like Dr. Wooten
would want but from our website instead of having to use Blast.
'''

from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from string import upper
from urllib2 import URLError

class BlastHandler(object):
    '''
    Constructor for the class.
    
    @author: Donovan Jordan
    @author: Jordan Hutcheson
    @param seq: The dna sequence to be referenced against Blast.
    @var seq: The sequence the class holds.
    @var blastRecord: The Record of the entire blast result.
    @var bestHsp: The best hsp from the entire blast result.
    @var blastAnswer: The title of the best match.
    '''
    def __init__(self, seq):
        
        self.seq = upper(seq)
        self.blastRecord = None
        self.bestHsp = None
        self.blastAnswer = None
        self.blastString = None

    '''
    Sends a sequence off to the Blast server and gets the result back. Now has additional
    timeout signal sending and handling to raise an error whenever the function goes past
    the allotted time.
     
    @author: Jordan Hutcheson
    @author: Donovan Jordan
    @var resultHandler: The returned results from Blast.
    '''
    def blastSendNucleotide(self):
        
        if not self.isAGoodSeq():
            return False
        
        #Here we try to get results back from blast. If it doesn't come in 5 minutes
        #we raise an exception.
        try:
            resultHandler = NCBIWWW.qblast("blastn", "nt", self.seq)#problem child
        except URLError:
            raise URLError("No connection to blast made")
        
        if resultHandler:
            self.blastRecord = NCBIXML.read(resultHandler)
            resultHandler.close()
            return True
        
        return False
    '''
    This parses the results we retrieved from blast and isolates the top Hsp from all the
    results. This way we can get the top result from Blast, as Dr. Wooten requested.
    It additionally assigns extra material needed for properly printing the result.
    
    @author: Donovan Jordan
    @author: Jordan Hutcheson
    @var bestHitID: The best HSP's ID.
    @var bestHitDef: The best HSp's Def.
    @var bestAlignementLength: The best Alignment's length
    @var bestHSPGaps: Gaps in the best HSP result
    @var bestHSPIdentities: Best HSP identities
    @return: True if success False if it didn't return correctly.
    '''
    def blastRecordParse(self):
        
        smallestEValue = 999999
        
        if not (self.blastRecord == None):
            for alignment in self.blastRecord.alignments:
                for hsp in alignment.hsps:
                    if hsp.expect < smallestEValue:
                        smallestEValue = hsp.expect
                        self.bestHsp = hsp
                        self.blastAnswer = alignment.title
                        self.bestHitID = alignment.hit_id
                        self.bestHitDef = alignment.hit_def
                        self.bestAlignmentLength = alignment.length
                        self.bestHSPGaps = hsp.gaps
                        self.bestHSPIdentities = hsp.identities
            self._formBlastStringResult()
            return True
        
        return False
    '''
    A function that checks if the initial sequence is good or not. 
    A sequence must be a dna sequence. Also, if the sequence doesn't have all letter,
    is None, or the length of the sequence is zero, the function will return zero.
    Otherwise the function is true.
    
    @author: Donovan Jordan
    @var allLetters: All letters that are not valid for the DNA sequence.
    @var letter: Each individual letter in AllLetters
    @return True if it is a good sequence and false otherwise
    '''
    def isAGoodSeq(self):
        
        if self.seq == None or len(self.seq) == 0:
            return False
        
        if not self.seq.isalpha():
            return False
        
        allLetters = ['B', 'D', 'E', 'F', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'U', 'V', 'W', 'X', 'Y', 'Z']
        for letter in allLetters:
            if letter in self.seq:
                return False
            
        return True
    '''
    Prints the Blast Record. Not what we finally want but is a useful testing method.
    
    @author: Donovan Jordan
    @var alignment: One of the alignemtns in the blastRecord.
    @var hsp: Hsp's of the alignment.
    @return True or False depending if the BlastRecord was there to begin with.
    '''
    def printBlastRecord(self):
        
        if self.blastRecord == None:
            print "Blast record has not been set."
            return False
        else:
            for alignment in self.blastRecord.alignments:
                for hsp in alignment.hsps:
                    if hsp.expect < .000004:
                        print("Alignment")
                        print('sequence:', alignment.title)
                        print('length:', alignment.length)
                        print('e value', hsp.expect)
                        print(hsp.query)
                        print(hsp.match)
                        print(hsp.sbjct)
            
        return True
    '''
    Returns the e value of the best match if self.bestHsp has been found.
    
    @author: Donovan Jordan
    @return True or false if bestHsp exists or not
    '''
    def getHspExpect(self):
        
        if self.bestHsp == None:
            return False
        
        return self.bestHsp.expect
    
    '''
    Returns the best match if the best hsp has been found.
    
    @author: Donovan Jordan
    @return True or false depending if the bestHsp has been found or not.
    '''
    def getHspSbjct(self):
        
        if self.bestHsp == None:
            return False
        
        return self.bestHsp.sbjct
    
    '''
    Returns the Title of the Blast Result.
    
    @author: Donovan Jordan
    @return self.BlastAnswer if it exists. False otherwise.
    '''
    def getBlastAnswer(self):
        
        if self.blastAnswer == None:
            return False
        
        return self.blastAnswer
    '''
    Prints the result handler. Used for testing purposes to see the result handler's form.
    
    @author: Donovan Jordan
    @return True for success and False otherwise.
    '''
    def printResultHandler(self):

        if self.resultHandler == None:
            print "Result handler has not been set."
            return False
        else:
            print self.resultHandler.read()
            
        return True
    '''
    Another Testing method that prints the best hsp's.
    
    @author Jordan Hutcheson
    @return True or False Depending on if the blast Record exists or not
    '''
    def printHSPs(self):
        if self.blastRecord == None:
            print "Blast record has not been set."
            return False
        else:
            for alignment in self.blastRecord.alignments:
                for hsp in alignment.hsps:
                    if hsp.expect < .000004:
                        print(hsp)
            
        return True
    '''
    Prints the Best Hsp result from the blast record.
    
    @author: Jordan Hutcheson
    '''
    def printBestHsp(self):
        print(self.bestHsp)
    
    '''
    Prints the result in a format that mimics the online result from blast. This method
    is what everthing else basically works up to.
    
    @author: Jordan Hutcheson
    '''
    def printBlastBestResult(self):
        print(self.blastString)
    
    '''
    Forms the blast string to be printed. Just the String.
    
    @author: Jordan Hutcheson
    '''
    def _formBlastStringResult(self):
        self.blastString = self.bestHitDef + "\nSequenceID: " + str(self.bestHitID) + "      Length: "
        self.blastString += str(self.bestAlignmentLength) + "\nIdentities: " + str(self.bestHSPIdentities) + "      Gaps: "
        self.blastString += str(self.bestHSPGaps) + "\n" + str(self.bestHsp) 
        
    '''
    Returns the blastString which is the result we are wanting from Blast.
    
    @return blastString: The completed formatted string we want from blast.
    '''
    def getBlastString(self):
        return self.blastString
    
'''
This is our timeout signal handler for if blast timesout.

@author: Jordan Hutcheson
'''
def blastTimeoutHandler(signum, frame):
    print("Blast taking too much time!")
    raise OSError("Blast not Responding!")
        
    
#Below are useful calls for testing the program. Would prefer to keep them here, in case of future testing.
#seq = "AAACACAATAGCTAAGACCCAAACTGGGATTAGATACCCCACTATGCTTAGCCCTAAACCTCAACAGTTAAATCACAAAACTGCTCGCCAGAACACTACGAGCCACAGCTTAAAACTCAAAGGACCTGGCGGTGCTTCATATCCCTCTAGAGGAGCCTGTTCTGTAATCGATAAACCCCGATCAACCTCACCACCTCTTGCTCAGCCTATATACCGCCATCTTCAGCAAACCCTGATGAAGGC"
#blast = BlastHandler("AAACACAATAGCTAAGACCCAAACTGGGATTAGATACCCCACTATGCTTAGCCCTAAACCTCAACAGTTAAATCACAAAACTGCTCGCCAGAACACTACGAGCCACAGCTTAAAACTCAAAGGACCTGGCGGTGCTTCATATCCCTCTAGAGGAGCCTGTTCTGTAATCGATAAACCCCGATCAACCTCACCACCTCTTGCTCAGCCTATATACCGCCATCTTCAGCAAACCCTGATGAAGGC")
#blast.blastSendNucleotide()
#blast.blastRecordParse()
#blast.getBlastString()
#blast.printBlastBestResult()
