from django.http import HttpResponse
from django.template import RequestContext, loader
from bioedit.models import Lab
import python.SequenceAligner as Aligner
import python.TreeBuilder as TB
import python.SequenceTranscription as ST
import python.DNAFileDict as DNAFile
# Create your views here.

def index(request):
    template = loader.get_template('bioedit/index.html')
    
    labs = Lab.objects.all()
    
    context = RequestContext(request, {'labs': labs})
    return HttpResponse(template.render(context))

def labSelection(request, lab_id):
    labName = Lab.objects.filter(id=lab_id)[0].lab_name
    return HttpResponse("The lab you selected is: %s" % labName)

def species(request):
    template = loader.get_template('bioedit/secondary.html')
    
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def alignOutput(request):
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
            
    template = loader.get_template('bioedit/demoPage.html')
    context = RequestContext(request, {'rnas': rna, 'protiens':protien, 'aligned': alignedList, 'tree': tree, 'dot_matrix':dotMatrix})
    
    return HttpResponse(template.render(context))


def uploadFile(request):
    template = loader.get_template('bioedit/file.html')
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
            dna=[1,2,3,4]
        
    else:
        dna=[1,2,3,4]
    
    template = loader.get_template('bioedit/species.html')
    context = RequestContext(request, {'dna_sequences':dna})
    
    return HttpResponse(template.render(context))

    