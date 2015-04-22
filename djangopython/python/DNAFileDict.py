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

Version 1.0 - Final Version with suggested updates after review of code.
'''


class DNAFileDict(object):
    
    '''
    Constructor for the File handler class.
    
    @param fileName - the name of the file that will be read
    
    @var objectDict: The dictionary of the class that will be used to quickly reference all of the species and dna strands with
    later parts of the project.
    @var pathName: Class holds onto the path of the file being read.    '''
    def __init__(self, pathName):
        self.objectDict = {}
        self.pathName = pathName
    '''
    Checks to make sure that the number of names of the species is equal to the number of nucleotides given.
    This is necessary to maintain the name value pairs.
    
    @param speciesNames: A list of the names read from the file
    @param speciesNucleotides: A list of the nucleotides read from the file
    
    @var isSameNum: Boolean for whether the same number of names is equal to the number of nucleotides
    @return: Returns whether or not there is the same number of names as nucleotides
    '''
    def checkNumNamesAndNucleotides(self, speciesNames, speciesNucleotides):
        isSameNum = False
        if len(speciesNames) == len(speciesNucleotides):
            isSameNum = True
        return isSameNum
    
    '''
    Checks whether the file is of the correct fasta format. This should be performed before setLists.
    
    @var thisFile: File object opened with self.pathName's location
    @var line: Line of the file that is being read. For each iteration of the loop it will first look at the name of the
        species and then the accompanying nucleotide sequence. E.G.:

    First--->    >Frog 
         --->    ATTGGCC         
    Second-->    >Cat
        --->    ATTGGCC

    @var checkSet: Set of characters that are allowed in fasta file format.
    '''
    def checkCorrectFileFormat(self):
        try:
            thisFile = open(self.pathName)
        except IOError:
            raise IOError("File Path not found in checkCorrectFileFormat")  
        checkSet = set("ATGC-")
        for line in thisFile:
            if line[0] == ">":
                line = line.rstrip("\n")
                line = line.rstrip() #necessary to make sure the name of the file isn't blank
                if line == ">":#checking to make sure this line isn't blank with only an arrow
                    return False
                line = thisFile.next()#Now we check to make sure the next line is correctly formatted and is the nucleotide list
                line = line.rstrip("\n")
                line = line.rstrip()
                if not set(line) <= checkSet:
                    return False
            else:
                return False
            
        return True           
            
    '''
    Sets the dictionary of class. It does this by creating 2 lists of the names of the species and the corresponding nucleotides.
    The method also reads from the file to get this information. Calls setObjectDictionary to assign the two lists.
    
    
    @var objectNameList: List to hold all of the species names from the file.
    @var objectNucleotideList: List to hold all of the corresponding Nucleotides
    @var fileOpen: The file being read from.
    @var line: A single line from the file
    '''
            
    def populateDict(self):
            objectNameList = []
            objectNucleotideList = []
            
            try:
                fileOpen = open(self.fileName)
            except IOError:
                raise IOError("File Path not found in populateDict")  
            
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
    
    @param speciesNamesIn: The names for the dictionary
    @param speciesNucleotidesIn: The nucleotides for the dictionary
    @return: Will return a string stating that the number of names does not match number of nucleotides if it fails the check.
    '''
    def setObjectDictionary(self, speciesNamesIn, speciesNucleotidesIn):
        x = 0
        if self.checkNumNamesAndNucleotides(speciesNamesIn, speciesNucleotidesIn):
            for name in speciesNamesIn:
                self.objectDict[name] = speciesNucleotidesIn[x]
                x += 1
        else:
            raise BaseException("The number of species names !=  number of nucleotide sequences")   
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
    try:
        filePlace = open(destination+fileName, 'wb+')
    except IOError:
        raise IOError("handleUploadedFile cannot find filepath.")
    for chunk in dnaFile.chunks():
        filePlace.write(chunk)
    filePlace.close()
    
    return destination+fileName
    

#dic = DNAFileDict('Mito-1 Raw.txt')

#dic.setLists()
#print dic.getDNADict()
