'''
Created on Jan 31, 2015

@author: jordan
'''


class DNAFileDict(object):
    

    def __init__(self, fileName):
        self.objectDict = {}
        self.fileName = fileName
        
    def checkNumNamesAndNucleotides(self, names, nucleotides):
        isSameNum = False
        if len(names) == len(nucleotides):
            isSameNum = True
        return isSameNum
        
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
            
            try:
                for line in fileOpen:
                    if line[0] == ">":
                        line = line.rstrip("\n")
                        line = line.rstrip(" ")
                        line = line.lstrip(">")
                        objectNameList.append(line)
                    else:
                        line = line.rstrip('\n, " ')
                        objectNucleotideList.append(line)
            except IndexError:
                return "IndexError: Index out of range."
            self.setObjectDictionary(objectNameList, objectNucleotideList)
            
    def setObjectDictionary(self, namesIn, nucleotidesIn):
        x = 0
        if self.checkNumNamesAndNucleotides(namesIn, nucleotidesIn):
            for name in namesIn:
                self.objectDict[name] = nucleotidesIn[x]
                x += 1
        else:
            return "Number of Names does not match Number of Nucleotides."   
        
    def getDNADict(self):
        return self.objectDict

def handleUploadedFile(dnaFile, fileName, destination):
    filePlace = open(destination+fileName, 'wb+')
    for chunk in dnaFile.chunks():
        filePlace.write(chunk)
    filePlace.close()
    
    return destination+fileName
    

#dic = DNAFileDict('Mito-1 Raw.txt')

#dic.setLists()
#print dic.getDNADict()