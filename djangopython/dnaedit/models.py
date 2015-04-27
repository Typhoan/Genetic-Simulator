from django.db import models
from django.utils import timezone
import time

# Create your models here.

class Lab(models.Model):
    
    '''
        This model is of a Lab. It allows a user to associate specific Labs to a species file.
    '''
    lab_name = models.CharField(max_length=200)
    dir_name = models.CharField(max_length=200)
    
    @classmethod
    def create(cls, labName, dirName):
        lab = cls(lab_name=labName, dir_name=dirName)
        
        return lab
    
    def __str__(self):
        return self.lab_name



class LabFile(models.Model):
    
    file_name = models.CharField(max_length=200)
    lab = models.ForeignKey(Lab)
    datetime_uploaded = models.DateTimeField()
    datetime_timezone = models.CharField(max_length=200)
    
    @classmethod
    def create(cls, file_name, lab):
        dateTime = timezone.now()
        timezoneNow = time.tzname[0]
        fileName = cls(file_name=file_name, lab=lab, datetime_uploaded=dateTime, datetime_timezone=timezoneNow)
        
        return fileName
    
    def __str__(self):
        return self.file_name
    
class Species(models.Model):
    '''
        This is a Species model that contains all of the information about a specific species.
        Each species contains the information for what file a species is associated to.
    '''
    dna_string = models.CharField(max_length=600)
    name = models.CharField(max_length=200)
    fileName = models.ForeignKey(LabFile)

    @classmethod
    def create(cls, name, dna_string, fileName):
        species = cls(name=name, dna_string=dna_string, fileName=fileName)
        
        return species
    
    def __str__(self):
        return self.name
    
class Document(models.Model):
    
    def __init__(self, labName):
        self.labName=labName
    spefile = models.FileField(upload_to='documents')