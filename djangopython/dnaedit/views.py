from django.http import HttpResponse
from django.template import RequestContext, loader
from dnaedit.models import Lab, Species, LabFile
import python.SequenceAligner as Aligner
import python.TreeBuilder as TB
import python.SequenceTranslation as ST
import python.DNAFileDict as DNAFile
import python.QueryChecks as Checks
import python.BlastHandler as BLAZE
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from djangopython.settings import MEDIA_ROOT
import time
import json as j
# Create your views here.


def imageShow(request, imageName):
    image_data = open(MEDIA_ROOT+"images/"+imageName, "rb").read()
    
    return HttpResponse(image_data, content_type="image/png")

def uploadFile(request):
    template = loader.get_template('dnaedit/file.html')
    context = RequestContext(request)
    
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
        
        #treeFile = TB.TreeBuilder()
        #tree = treeFile.createTree(alignedList)
        
        dotMatrix = align.generateDotMatrix(alignedList)
        
        dotMatrixSend = {}
        for i in range(int(postCount)):
            dotMatrixSend[key[i]] = dotMatrix[i]
            
        rna = {}
        keyIterator = 0
        for strand in regSpes:
            rna[key[keyIterator]]=ST.DNAToRNA(strand)
            keyIterator += 1
            
        protein = {}

        for k in range(int(postCount)):
            protein[key[k]] = ST.RNAToProtein(rna[key[k]])
        #x,y = alignSequences(dna[0], dna)
        #align_output = createTree(spes)
        
        time.sleep(10)
        
    responseDict = {'keys':key ,'rnaSequences': rna, 'proteinSequences':protein, 'dotMatrix':dotMatrixSend}
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


'''

API Methods

'''


'''
    Send the labs in a dictionary with the labs id being 
    the key and the lab name being the value.
'''
@csrf_exempt
def sendLabs(request):
    
    labs = Lab.objects.all()
    
    labNames = {}
    
    for lab in labs:
        labNames[lab.id]= lab.lab_name
    
    responseDict = {'labs': labNames}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send the files for a specific lab in a dictionary with the files id 
    being the key and the file name being the value.
    
    Takes in a lab_id to associate the specific lab.
'''
@csrf_exempt
def sendFiles(request):
    if request.method == 'POST':
        labId = request.POST.get('lab_id')
    elif request.method == 'GET':
        labId = request.GET.get('lab_id')
    else:
        return HttpResponse(status=400, reason='No information was given.')
        
    
    lab = Lab.objects.filter(id = labId)[0]
    files = LabFile.objects.filter(lab = lab)
    filesDict = {}
    
    for f in files:
        filesDict[f.id] = f.file_name
        
    responseDict = {'files': filesDict}
    response = JsonResponse(responseDict)
    
    return response

def sendFileSequences(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
    elif request.method == 'GET':
        file_id = request.GET.get('file_id')
    else:
        return HttpResponse(status=400, reason='No information was given.')
    
    labFile = LabFile.objects.filter(id=file_id)[0]
    dna = Species.objects.filter(fileName=labFile)
    
    responseDict = {'sequences':dna}
    response = JsonResponse(responseDict)
    
    return response

'''
    Send the topology tree image path.
    
    Takes in a json string of a dictionary that contains the aligned sequences
    with the name of the species as the key and the actual sequence as the value.
'''
@csrf_exempt
def getTopologyFilePath(request):
    if request.method == 'POST':
        unalignedSeq = j.loads(request.POST.get('unaligned_sequences'))
    elif request.method == 'GET':
        unalignedSeq = j.loads(request.GET.get('unaligned_sequences'))
        
    if unalignedSeq:
        try:
            align = Aligner.SequenceAligner()
            alignedSeq = align.alignSequences(unalignedSeq)
            tree = TB.TreeBuilder(alignedSeq)
            treePath = tree.createTree()
        except Exception as e:
            return HttpResponse(status=400, reason=str(e))
    else:
        return HttpResponse(status=400, reason='No information was given.')
        
    responseDict = {'file_path': treePath}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send the topology tree as a string for a ete2 system to process its own images.
    
    Takes in a json string of a dictionary that contains the aligned sequences
    with the name of the species as the key and the actual sequence as the value.
'''
@csrf_exempt
def getTopologyTreeString(request):
    if request.method == 'POST':
        unalignedSeq = j.loads(request.POST.get('unaligned_sequences'))
    elif request.method == 'GET':
        unalignedSeq = j.loads(request.GET.get('unaligned_sequences'))
        
    if unalignedSeq:
        #try:
        align = Aligner.SequenceAligner()
        alignedSeq = align.alignSequences(unalignedSeq)
        tree = TB.TreeBuilder(alignedSeq)
        treeString = tree.createTreeString()
        #except Exception as e:
        #    return HttpResponse(status=400, reason=str(e))
    else:
        return HttpResponse(status=400, reason='No information was given.')
    

        
    responseDict = {'tree_string': treeString}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send a dictionary of the rna with keys represented by the species names
    and the values as the actual sequence.
    
    Takes in a json string of a dictionary that contains the dna sequences
    with the name of the species as the key and the actual sequence as the value.
'''
@csrf_exempt
def getRNAFromDNA(request):
    if request.method == 'POST':
        allignedSeq = j.loads(request.POST.get('dna'))
    elif request.method == 'GET':
        allignedSeq = j.loads(request.GET.get('dna'))
        
    if allignedSeq:
        try:
            rna = {}
            for key in allignedSeq.keys():
                rna[key]=ST.DNAToRNA(allignedSeq[key])
        except Exception as e:
            return HttpResponse(status=400, reason=str(e))

    else:
        return HttpResponse(status=400, reason='No information was given.')
    
        
    responseDict = {'rna': rna}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send a dictionary of the dna with keys represented by the species names
    and the values as the actual sequence.
    
    Takes in a json string of a dictionary that contains the rna sequences
    with the name of the species as the key and the actual sequence as the value.
'''
@csrf_exempt
def getDNAFromRNA(request):
    if request.method == 'POST':
        rnaSeq = j.loads(request.POST.get('rna'))
    elif request.method == 'GET':
        rnaSeq = j.loads(request.GET.get('rna'))    
    if rnaSeq:
        try:
            dna = {}
            for key in rnaSeq.keys():
                dna[key]=ST.RNAToDNA(rnaSeq[key])
        except Exception as e:
            return HttpResponse(status=400, reason=str(e))
    else:
        return HttpResponse(status=400, reason='No information was given.')
    
        
    responseDict = {'dna': dna}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send a dictionary of the dna with keys represented by the species names
    and the values as the inverse sequence.
    
    Takes in a json string of a dictionary that contains the dna sequences
    with the name of the species as the key and the actual sequence as the value.
'''
@csrf_exempt
def getInverseDNA(request):
    if request.method == 'POST':
        dnaSeq = j.loads(request.POST.get('dna'))
    elif request.method == 'GET':
        dnaSeq = j.loads(request.GET.get('dna'))    
    if dnaSeq:
        try:
            inverseDNA = {}
            for key in dnaSeq.keys():
                inverseDNA[key]=ST.invertDNA(dnaSeq[key])
        except Exception as e:
            return HttpResponse(status=400, reason=str(e))
    else:
        return HttpResponse(status=400, reason='No information was given.')
    
        
    responseDict = {'inverse_dna': inverseDNA}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send a dictionary of the protein with keys represented by the species names
    and the values as the actual sequence.
    
    Takes in a json string of a dictionary that contains the rna sequences
    with the name of the species as the key and the actual sequence as the value.
'''
@csrf_exempt
def getProteinFromRNA(request):
    if request.method == 'POST':
        rnaSeq = j.loads(request.POST.get('rna'))
    elif request.method == 'GET':
        rnaSeq = j.loads(request.GET.get('rna'))    
    if rnaSeq:
        try:
            protein = {}
            for key in rnaSeq.keys():
                protein[key]=ST.RNAToProtein(rnaSeq[key])
        except Exception as e:
            return HttpResponse(status=400, reason=str(e))

    else:
        return HttpResponse(status=400, reason='No information was given.')
    
        
    responseDict = {'protein': protein}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send a dictionary of the protein with keys represented by the species names
    and the values as the actual sequence.
    
    Takes in a json string of a dictionary that contains the dna sequences
    with the name of the species as the key and the actual sequence as the value.
'''
@csrf_exempt
def getProteinFromDNA(request):
    if request.method == 'POST':
        dnaSeq = j.loads(request.POST.get('dna'))
    elif request.method == 'GET':
        dnaSeq = j.loads(request.GET.get('dna'))
            
    if dnaSeq:
        try:
            protein = {}
            for key in dnaSeq.keys():
                protein[key]=ST.RNAToProtein(ST.DNAToRNA(dnaSeq[key]))
        except Exception as e:
            return HttpResponse(status=400, reason=str(e))

    else:
        return HttpResponse(status=400, reason='No information was given.')
    
        
    responseDict = {'protein': protein}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send a dictionary of the aligned sequences with keys represented by the species names
    and the values as the actual sequence.
    
    Takes in a json string of a dictionary that contains the unaligned sequences
    with the name of the species as the key and the actual sequence as the value.
'''
@csrf_exempt
def getAlignedSequences(request):
    if request.method == 'POST':
        unalignedSeq = j.loads(request.POST.get('dna'))
    elif request.method == 'GET':
        unalignedSeq = j.loads(request.GET.get('dna'))
        
    if unalignedSeq:
        try:
            align = Aligner.SequenceAligner()
            alignedSeq = align.alignSequences(unalignedSeq)
            
        except Exception as e:
            return HttpResponse(status=400, reason=str(e))
    else:
        return HttpResponse(status=400, reason='No information was given.')
        
    responseDict = {'aligned_sequences': alignedSeq}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send a dictionary of the dot matrix with keys represented by the species names
    and the values as the actual sequence.
    
    Takes in a json string of a dictionary that contains the sequences
    with the name of the species as the key and the actual sequence as the value.
'''
@csrf_exempt
def getDotMatrix(request):
    if request.method == 'POST':
        unalignedSeq = j.loads(request.POST.get('sequences'))
        seqName = request.POST.get('dominant_species')
    elif request.method == 'GET':
        unalignedSeq = j.loads(request.GET.get('sequences'))
        seqName = request.GET.get('dominant_species')
        
    if unalignedSeq:
        try:
            align = Aligner.SequenceAligner()
            alignedSeq = align.alignSequences(unalignedSeq)
            dotMatrix = align.generateDotMatrix(seqName, alignedSeq)
            
        except Exception as e:
            return HttpResponse(status=400, reason=str(e))
    else:
        return HttpResponse(status=400, reason='No information was given.')
        
    responseDict = {'dot_matrix': dotMatrix}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send a report of the sequence posted.
    
    Takes in a sequence that is sent to BLAST.
'''
@csrf_exempt
def getBlazeReport(request):
    if request.method == 'POST':
        blazeSeq = request.POST.get('sequence')
    elif request.method == 'GET':
        blazeSeq = request.GET.get('sequence')
    if blazeSeq:
        
        blazeObj = BLAZE.BlastHandler(blazeSeq)
        blazeObj.blastSendNucleotide()
        blazeObj.blastRecordParse()
        blazeReport = blazeObj.getBlastString()
            
        #except Exception as e:
        #   return HttpResponse(status=400, reason=str(e))
    else:
        return HttpResponse(status=400, reason='No information was given.')
        
    responseDict = {'blaze_report': blazeReport}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send a dictionary of the sequence distances with keys represented by the species names
    and the values as the distances from one another.
    
    Takes in a json string of a dictionary that contains the aligned sequences
    with the name of the species as the key and the actual sequence as the value.
'''
@csrf_exempt
def getDistanceMatrix(request):
    if request.method == 'POST':
        unalignedSeq = j.loads(request.POST.get('unaligned_sequences'))
    elif request.method == 'GET':
        unalignedSeq = j.loads(request.GET.get('unaligned_sequences'))
        
    if unalignedSeq:
        align = Aligner.SequenceAligner()
        alignedSeq = align.alignSequences(unalignedSeq)
        tree = TB.TreeBuilder(alignedSeq)
        distanceMatrix = tree.getDistanceMatrix()
        '''
        try:
            tree = TB.TreeBuilder(allignedSeq)
            distanceMatrix = tree.getDistanceMatrix()
        except Exception as e:
            return HttpResponse(status=400, reason=str(e))
        '''
    else:
        return HttpResponse(status=400, reason='No information was given.')
        
    responseDict = {'distance_matrix': distanceMatrix}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send a string representation of the sequence distances.
    
    Takes in a json string of a dictionary that contains the aligned sequences
    with the name of the species as the key and the actual sequence as the value.
'''
@csrf_exempt
def getDistanceMatrixString(request):
    if request.method == 'POST':
        unalignedSeq = j.loads(request.POST.get('unaligned_sequences'))
    elif request.method == 'GET':
        unalignedSeq = j.loads(request.GET.get('unaligned_sequences'))
        
    if unalignedSeq:
        try:
            align = Aligner.SequenceAligner()
            alignedSeq = align.alignSequences(unalignedSeq)
            tree = TB.TreeBuilder(alignedSeq)
            distanceMatrixString = tree.getDistanceMatrixAsString()
        except Exception as e:
            return HttpResponse(status=400, reason=str(e))
    else:
        return HttpResponse(status=400, reason='No information was given.')
        
    responseDict = {'distance_matrix': distanceMatrixString}
    response = JsonResponse(responseDict)
    
    return response


'''
    Send a string that is a message on whether or not the file was uploaded.
    
    Takes in a file called lab_file and the labname to be associated to the file.
'''
@csrf_exempt
def uploadLabFile(request):
    message=""
    if request.method == 'POST':
        strands = request.FILES['lab_file']
        labName = request.POST.get('lab_name', False)
    elif request.method == 'GET':
        strands = request.FILES['lab_file']
        labName = request.GET.get('lab_name', False)
    if strands:
        try:
            strandsName = strands.name
            filePath = DNAFile.handleUploadedFile(strands, strandsName, 'media/files/')
            DNAdict = DNAFile.DNAFileDict(filePath)
        
            isGoodFile = DNAdict.checkCorrectFileFormat()
            lab = None
            labFile = None
        
            if isGoodFile:
                DNAdict.populateDict()
        
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
        
                dnaKeys = DNAdict.getDNADict()
                for key in dnaKeys.keys():
                    if not Checks.checkSpeciesExists(dnaString=dnaKeys[key], name=key, labFile=labFile):
                        species = Species.create(name=key, dna_string=dnaKeys[key], fileName=labFile)
                        species.save()
                
                if message == "":
                    message="Lab has been successfully added."
        
            else:
                message = "File contained the wrong format. Please try again."
        except IOError as e:
            return HttpResponse(status=400, reason=str(e))
        except BaseException as e:
            return HttpResponse(status=400, reason=str(e))
        except Exception:
            return HttpResponse(status=400, reason="File contained the wrong format. Please try again.")
    else:
        message = "No file was uploaded. Please try again."
    
    jsonDict = {'message':message}
    
    return JsonResponse(jsonDict)
