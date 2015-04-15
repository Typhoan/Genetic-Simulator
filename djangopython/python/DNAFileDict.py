'''
Created on Jan 31, 2015
@author: Jordan Hutcheson
@contact: email: jmh0049@auburn.edu
The purpose of the class is to attempt to handle all of the handling of the input file straight from the user.
It not only reads from the file and divides it up into a dictionary for the other parts of the program, but also
checks that the file is of the correct type. It throws its own errors for the program. 
Version 0.1 -  First full implementation of the project which initially fills all the function initially required of the class.
Version 0.2 - Includes the new function checkCorrectFileFormat which returns whether or not the file given has the fasta format
that the entire program wants to use. Also includes further in depth documentation. 
'''
import os
from djangopython.settings import MEDIA_ROOT


class DNAFileDict(object):
    
    '''
    Constructor for the File handler class.
    
    @param fileName - the name of the file that will be read
    
    @var objectDict: The dictionary of the class that will be used to quickly reference all of the species and dna strands with
    later parts of the project.
    @var fileName: Class holds onto the name of the file it is reading from.
    '''
    def __init__(self, fileName):
        self.objectDict = {}
        self.fileName = fileName
        
    '''
    Checks to make sure that the number of names of the species is equal to the number of nucleotides given.
    This is necessary to maintain the name value pairs.
    
    @param names: A list of the names read from the file
    @param nucleotides: A list of the nucleotides read from the file
    
    @var isSameNum: Boolean for whether the same number of names is equal to the number of nucleotides
    @return: Returns whether or not there is the same number of names as nucleotides
    '''
    def checkNumNamesAndNucleotides(self, names, nucleotides):
        isSameNum = False
        if len(names) == len(nucleotides):
            isSameNum = True
        return isSameNum
    
    '''
    Checks whether the file is of the correct fasta format. This should be performed before setLists.
    
    @param fileNameIn: The file to be checked for whether it is of fasta format or not.
    
    @var isCorrect: Boolean telling whether or not the file is of correct format
    @var thisFile: File object opened with fileNameIn's location
    @var line: Line of the file that is being read
    @var character: An individual character from that line in the file.
    @todo: Need to discover if the file can have blank species name or not.
    '''
    def checkCorrectFileFormat(self):
        isCorrect = False
        thisFile = open(self.fileName)
        checkSet = set("ATGC")
        for line in thisFile:
            if line[0] == ">":
                line = line.rstrip("\n")
                line = line.rstrip() #necessary to make sure the name of the file isn't blank
                if line == ">":#checking to make sure this line isn't blank with only an arrow
                    isCorrect = "One of the species names are not specified in this file"
                    break
                line = thisFile.next()
                line = line.rstrip("\n")
                line = line.rstrip()
                if set(line) <= checkSet:
                    isCorrect = True
                else:
                    isCorrect = False
                    break
            else:
                isCorrect = False
                break
        return isCorrect
            
                    
            
    '''
    Sets the dictionary of class. It does this by creating 2 lists of the names of the species and the corresponding nucleotides.
    The method also reads from the file to get this information. Calls setObjectDictionary to assign the two lists.
    
    
    @var objectNameList: List to hold all of the species names from the file.
    @var objectNucleotideList: List to hold all of the corresponding Nucleotides
    @var fileOpen: The file being read from.
    @var line: A single line from the file
    '''
            
    def setLists(self):
#         fileSuccess = False
#         while(not fileSuccess):
            objectNameList = []
            objectNucleotideList = []
            
            try:
                fileOpen = open(self.fileName)
                
#                 fileSuccess = True
            except IOError:
                return "IOError: File by that directory not found. Please try again."
            
            for line in fileOpen:
                if line[0] == ">":
                    line = line.rstrip("\n")
                    line = line.rstrip(" ")
                    line = line.lstrip(">")
                    objectNameList.append(line)
                else:
                    line = line.rstrip('\n, " ')
                    objectNucleotideList.append(line)
            self.setObjectDictionary(objectNameList, objectNucleotideList)
        
    '''
    Assigns the key-value pairs of the dictionary
    
    @param namesIn: The names for the dictionary
    @param nucleotidesIn: The nucleotides for the dictionary
    @return: Will return a string stating that the number of names does not match number of nucleotides if it fails the check.
    '''
    def setObjectDictionary(self, namesIn, nucleotidesIn):
        x = 0
        if self.checkNumNamesAndNucleotides(namesIn, nucleotidesIn):
            for name in namesIn:
                self.objectDict[name] = nucleotidesIn[x]
                x += 1
        else:
            return "Number of Names does not match Number of Nucleotides."   
    '''
    Returns the objectDict object
    
    @return: Returns the objectDict which is the dictionary.
    '''
    def getDNADict(self):
        return self.objectDict

'''
Required function for uploading this information to django.
'''
def handleUploadedFile(dnaFile, fileName, destination):
    filePlace = open(MEDIA_ROOT+destination+fileName, 'w+b')
    for chunk in dnaFile.chunks():
        filePlace.write(chunk)
    filePlace.close()
    print os.path.abspath(str(destination) + str(fileName))
    return os.path.abspath(MEDIA_ROOT+str(destination) + str(fileName))
    

#dic = DNAFileDict('Mito-1 Raw.txt')

#dic.setLists()
#print dic.getDNADict()