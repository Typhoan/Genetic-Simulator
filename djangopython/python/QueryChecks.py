from dnaedit.models import Lab, LabFile

'''
Created on Feb 25, 2015

@author: donovan
'''

def checkLabNameExists(name):
    labNames = Lab.objects.filter(lab_name=name)
    
    if labNames.count() > 0:
        return True
    
    return False

def checkFileNameExists(name):
    fileNames = LabFile.objects.filter(file_name=name)
    
    if fileNames.count() > 0:
        return True
    
    return False