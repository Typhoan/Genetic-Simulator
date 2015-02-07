from django.db import models

# Create your models here.

class Lab(models.Model):
    lab_name = models.CharField(max_length=200)
    dir_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.lab_name

class Species(models.Model):
    dna_string = models.CharField(max_length=600)
    name = models.CharField(max_length=200)
    lab = models.ForeignKey(Lab)
    fileName = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Document(models.Model):
    
    def __init__(self, labName):
        self.labName=labName
    spefile = models.FileField(upload_to='documents')