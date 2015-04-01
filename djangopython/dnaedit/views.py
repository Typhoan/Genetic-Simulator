from django.http import HttpResponse
from django.template import RequestContext, loader
from dnaedit.models import Lab, Species, LabFile
import python.SequenceAligner as Aligner
import python.TreeBuilder as TB
import python.SequenceTranscription as ST
import python.DNAFileDict as DNAFile
import python.QueryChecks as Checks
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    template = loader.get_template('dnaedit/index.html')
    
    labs = Lab.objects.all()
    
    context = RequestContext(request, {'labs': labs})
    return HttpResponse(template.render(context))

def labSelection(request, lab_id):
    labName = Lab.objects.filter(id=lab_id)[0].lab_name
    return HttpResponse("The lab you selected is: %s" % labName)

def showFiles(request):
    template = loader.get_template('dnaedit/showFiles.html')
    
    files = LabFile.objects.all()
    
    context = RequestContext(request, {'files': files})
    return HttpResponse(template.render(context))


def fileSelection(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
    else:
        file_id = -1
    labFile = LabFile.objects.filter(id=file_id)[0]
    dna = Species.objects.filter(fileName=labFile)
    
    template = loader.get_template("dnaedit/speciesFromDB.html")
    context = RequestContext(request, {'dna_sequences':dna})
    
    return HttpResponse(template.render(context))

def species(request):
    template = loader.get_template('dnaedit/secondary.html')
    
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def generateOutput(request):
    spes = []
    if request.method == 'POST':
        postCount = request.POST.get('count')
        
        for value in range(int(postCount)):
            spes.append(request.POST.get('species'+str(value+1)))
        
    if spes:
        align = Aligner.SequenceAligner()
        aligningSpes = spes
        alignedList = align.alignSequences(aligningSpes.pop(), aligningSpes)
        
        tree = TB.createTree(alignedList)
        
        dotMatrix = align.generateDotMatrix(alignedList)
        rna = []
        for strand in spes:
            rna.append(ST.DNAToRNA(strand))
        
        protien = []
        for strings in rna:
            protien.append(ST.RNAToProtien(strings))
        #x,y = alignSequences(dna[0], dna)
        #align_output = createTree(spes)
            
    template = loader.get_template('dnaedit/demoPage.html')
    context = RequestContext(request, {'rnas': rna, 'protiens':protien, 'tree': tree, 'dot_matrix':dotMatrix})
    
    return HttpResponse(template.render(context))

def uploadFile(request):
    template = loader.get_template('dnaedit/file.html')
    context = RequestContext(request)
    
    return HttpResponse(template.render(context))

def fileHandler(request):
    if request.method == 'POST':
        strands = request.FILES['group_file']
        
    if strands:
        name = DNAFile.handleUploadedFile(strands, strands.name, '')
        DNAdict = DNAFile.DNAFileDict(fileName=name)
        DNAdict.setLists()
        
        dna = []
        
        dnaKeys = DNAdict.getDNADict()
        for key in dnaKeys.keys():
            dna.append(dnaKeys[key])
            
        
        if not dna:
            dna=[5,6,7,8]
        
    else:
        dna=[1,2,3,4]
    
    template = loader.get_template('dnaedit/species.html')
    context = RequestContext(request, {'dna_sequences':dna})
    
    return HttpResponse(template.render(context))

def fileSparse(request):
    message=""
    if request.method == 'POST':
        strands = request.FILES['group_file']
        labName = request.POST.get('labname', False)
        
    if strands:
        strandsName = strands.name
        name = DNAFile.handleUploadedFile(strands, strandsName, '')
        DNAdict = DNAFile.DNAFileDict(fileName=name)
        
        isGoodFile = DNAdict.checkCorrectFileFormat()
        
        if isGoodFile:
            DNAdict.setLists()
        
            if labName:
                if not Checks.checkLabNameExists(labName):
                    lab = Lab.create(labName=labName, dirName=labName)
                    lab.save()
                else:
                    lab = Lab.objects.filter(lab_name = labName)[0]   
        
            if lab and strandsName:
                if not Checks.checkFileNameExists(strandsName):
                    labFile = LabFile.create(file_name=strandsName, lab=lab)
                    labFile.save()
                else:
                    labFile = LabFile.objects.filter(file_name = strandsName)[0]
                    message="Lab currently exists. Please try again."
        
            dnaKeys = DNAdict.getDNADict()
            for key in dnaKeys.keys():
                if not Checks.checkSpeciesExists(dnaString=dnaKeys[key], name=key, labFile=labFile):
                    species = Species.create(name=key, dna_string=dnaKeys[key], fileName=labFile)
                    species.save()
                
            if message == "":
                message="Lab has been successfully added."
        
        else:
            message = "File contained the wrong format. Please try again."
        
    else:
        message = "No file was uploaded. Please try again."
    
    template = loader.get_template('dnaedit/file.html')
    context = RequestContext(request, {'message':message})
    
    return HttpResponse(template.render(context))


#AJAX TEST FUNCTIONS
@csrf_exempt
def getDNAInformation(request):
    spes = []
    regSpes = []
    key = []
    if request.method == 'POST':
        postCount = request.POST.get('count')
        
        for value in range(int(postCount)):
            spes.append(request.POST.get('species'+str(value+1)))
            regSpes.append(request.POST.get('species'+str(value+1)))
            key.append('species'+str(value+1))
    
    if spes:
        align = Aligner.SequenceAligner()
        aligningSpes = spes
        alignedList = align.alignSequences(aligningSpes[0], aligningSpes[1:])
        
        tree = TB.createTree(alignedList)
        
        dotMatrix = align.generateDotMatrix(alignedList)
        
        dotMatrixSend = {}
        for i in range(int(postCount)):
            dotMatrixSend[key[i]] = dotMatrix[i]
            
        rna = {}
        keyIterator = 0
        for strand in regSpes:
            rna[key[keyIterator]]=ST.DNAToRNA(strand)
            keyIterator += 1
            
        protien = {}

        for k in range(int(postCount)):
            protien[key[k]] = ST.RNAToProtien(rna[key[k]])
        #x,y = alignSequences(dna[0], dna)
        #align_output = createTree(spes)
        
    responseDict = {'keys':key ,'rnaSequences': rna, 'proteinSequences':protien, 'tree': tree, 'dotMatrix':dotMatrixSend}
    response = JsonResponse(responseDict)
    
    return response


def fileSelectionAjax(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
    else:
        file_id = -1
    labFile = LabFile.objects.filter(id=file_id)[0]
    dna = Species.objects.filter(fileName=labFile)
    
    template = loader.get_template("dnaedit/ajaxDemo.html")
    context = RequestContext(request, {'dna_sequences':dna})
    
    return HttpResponse(template.render(context))

def ajaxShowFiles(request):
    template = loader.get_template('dnaedit/ajaxShowFiles.html')
    
    files = LabFile.objects.all()
    
    context = RequestContext(request, {'files': files})
    return HttpResponse(template.render(context))
