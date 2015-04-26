//==============================================================================================================================================================
//Helper functions
function addNewSequence(){
	var counter = parseInt($('#counter').val(), 10);
	counter+=1;
	var formInfo = $('#sequencesForm').html();
	formInfo += "<input type='text' size='15' name='"+counter.toString()+"' onblur='generateLists()' id='speciesName"+counter.toString()+"' value='Species "+counter.toString()+"'/>";
	formInfo += " <input type='text' size='100' oninput='isValid(this.value, this.name);' onblur='this.value=this.value.toUpperCase();' name='species"+counter.toString()+"' id='speciesValue"+counter.toString()+"' value=''/> ";
	formInfo += "<button id='speciesButton"+counter.toString()+"' type='button' onclick='deleteSequence("+counter.toString()+")'>Delete</button>";
	formInfo += " <span id='species"+counter.toString()+"'></span><br id='gone"+counter.toString()+"'/>";
	$('#sequencesForm').html(formInfo);
	$('#counter').val(counter);
	
	generateLists();
	startValidity();
}

function deleteSequence(number){
	$("#speciesName"+number).remove()
	$("#speciesValue"+number).remove()
	$("#speciesButton"+number).remove()
	$("#gone"+number).remove()
	$("#species"+number).remove()
	generateLists();
}

function isValid(sequence, id){

	var re = /^[atgcATGC]+$/;
	if (re.test(sequence)){
		$('#'+id).html('valid sequence');
	}
	else{
		$('#'+id).html('invalid sequence');
	}
}

function checkOneIsValid(id){

	var re = /^[atgcATGC]+$/;
	return re.test($('#speciesValue'+id).val());
	
}

function checkAllValid(){
	var counter = parseInt($('#counter').val(), 10);
	var re = /^[atgcATGC]+$/;
	var i;
	for(i=1; i<=counter; i++){
		if(document.getElementById("speciesName"+i)){
			if(!re.test($("#speciesValue"+i).val())){
				return false;
			}
		}
	}
	return true;
}

function startValidity(){
	var counter = parseInt($('#counter').val(), 10);
	
	var i;
	for(i=1; i<=counter; i++){
		if(document.getElementById("speciesName"+i)){
			isValid($("#speciesValue"+i).val(), "species"+i);
		}
	}
}

function generateSequenceDict(){
	var seqDict = {};
	var counter = parseInt($('#counter').val(), 10);
	
	var i;
	for(i=1; i<=counter; i++){
		if(document.getElementById("speciesName"+i)){
			seqDict[$("#speciesName"+i).val().trim()] = $("#speciesValue"+i).val();
		}
	}
	return seqDict;
	
}

function generateNameList(id, selectId){
	var seqSelect;
	var counter = parseInt($('#counter').val(), 10);
	
	seqSelect = "<select id='"+selectId+"'>";
	
	for(var i=1; i<=counter; i++){
			if(document.getElementById("speciesName"+i)){	
			seqSelect += "<option value='"+$("#speciesName"+i).attr("name")+"'>"+ $("#speciesName"+i).val().trim() +"</option>";
		}
	}
	
	seqSelect += "</select>";
	
	$("#"+id).html(seqSelect);
}

function labNameSetup(labs){
	
	var labSelect;
	var labId;
	labSelect = "<select id='lab' name='lab_id' onchange='sendLab(this.value)'>";
	labSelect += "<option selected='selected'>Please Select a lab</option>";
	for(labId in labs){
		labSelect += "<option value='"+labId+"'>"+ labs[labId] +"</option>";
	}
	
	labSelect += "</select>";
	
	$('#labSelection').html(labSelect);
	
}

function generateLists(){
	
	generateNameList("blazeSelectDiv", "blazeSelect");
	generateNameList("dotSelectDiv", "dotSelect");
	generateNameList("waveformSelectDiv", "waveformSelect");
}

function fileNameSetup(files){
	
	var fileSelect;
	var fileId;
	fileSelect = "<select id='file' name='file_id'>";
	fileSelect += "<option selected='selected'>Please Select a lab</option>";
	for(fileId in files){
		fileSelect += "<option value='"+fileId+"'>"+ files[fileId] +"</option>";
	}
	
	fileSelect += "</select>";
	fileSelect += "<br/><input type='submit'/>";
	
	$('#fileSend').html(fileSelect);
	
}

function setDotMatrix(dotStuff){
	var keys = Object.keys(dotStuff);
	var replacement="";
	var i;
	for(i=0; i<keys.length; i++){
		replacement += "<p>"+keys[i]+"<pre style='font-size:16px'>"+dotStuff[keys[i]]+"</pre></p>";
	}
	$("#dotDisplay").html(replacement);
}

function setDistanceMatrixString(distanceStuff){
	var replacement="";

	replacement += "<p>"+distanceStuff+"</p>";
	$("#distanceDisplay").html(replacement);
}

function setRNA(rnaStuff){
	var keys = Object.keys(rnaStuff);
	var replacement="";
	var i;
	for(i=0; i<keys.length; i++){
	console.log(keys[i]);
		replacement += "<p>"+keys[i]+": "+rnaStuff[keys[i]]+"</p>";
	}
	
	$("#rnaDisplay").html(replacement);
	
}

function setInverse(inverseStuff){
	var keys = Object.keys(inverseStuff);
	var replacement="";
	var i;
	for(i=0; i<keys.length; i++){
	console.log(keys[i]);
		replacement += "<p>"+keys[i]+": "+inverseStuff[keys[i]]+"</p>";
	}
	
	$("#inverseDisplay").html(replacement);
	
}

function setProtein(proteinStuff){
	var keys = Object.keys(proteinStuff);
	var replacement="";
	var i;
	for(i=0; i<keys.length; i++){
		replacement += "<p>"+keys[i]+": "+proteinStuff[keys[i]]+"</p>";
	}
	$("#proteinDisplay").html(replacement);
}

function setTopTree(treeStuff){
	var replacement="";
	replacement += "<img src='/"+treeStuff+"'/>";
	$("#treeDisplay").html(replacement);
}

function setTopTreeString(treeStuff){
	var replacement="";
	replacement += "<p>"+treeStuff+"</p>";
	$("#treeDisplay").html(replacement);
}


//==============================================================================================================================================================
//Ajax calls
function getLabs(url){
	$.ajax({
		
		url: url,
		type: "GET",
		data: {},
		success: function(data){
		
				labNameSetup(data.labs);
				
			},
		
	});
}

function getFiles(url, labId){
	$.ajax({
		
		url: url,
		type: "GET",
		data: {'lab_id': labId},
		success: function(data){
				
				fileNameSetup(data.files);
		},
		
	});
}

function getFileSequences(url, fileId){
	$.ajax({
			
		url: url,
		type: "GET",
		data: {'file_id': fileId},
		success: function(data){
				
				return data.sequences;
		},
			
	});
}

function getProteinFromDNA(url, dna){
	$.ajax({
		
		url:url,
		type: "POST",
		data: {"dna": dna},
		success: function(data){
		
				setProtein(data.protein);
		},
		
	});

}

function getRNAFromDNA(url, dna){
	$.ajax({
	
		url: url,
		type: "POST",
		data: {"dna": dna},
		success: function(data){
		
				setRNA(data.rna);
		},
		
	});
	
}

function getInverseDNA(url, dna){
	$.ajax({
	
		url:url,
		type: "POST",
		data: {"dna": dna},
		success: function(data){
		
				setInverse(data.inverse_dna);
				
		},
		
	});

}

function getDistanceMatrix(url, dna){
	$.ajax({
	
		url:url,
		type: "POST",
		data: {"unaligned_sequences": dna},
		success: function(data){
		
				return data.distance_matrix;
		},
		
	});
}

function getDistanceMatrixString(url, dna){
	$.ajax({
	
		url:url,
		type: "POST",
		data: {"unaligned_sequences": dna},
		success: function(data){
		
				setDistanceMatrixString(data.distance_matrix);
		},
		
	});
}

function getBlazeReport(url, sequence){
	$.ajax({
	
		url:url,
		type: "POST",
		data: {"sequence": sequence},
		success: function(data){
			
			$("#blazeDisplay").html("<p>"+data.blaze_report+"</p>");
		},
		error: function(request, err){
			
			var data = "<p>There was an issue processing your BLAZE Report.";
			data+= " Your sequence may have been too small or it could not process at this moment.";
			data+= "<br/>You can try again at <a href='http://blast.ncbi.nlm.nih.gov/Blast.cgi'>http://blast.ncbi.nlm.nih.gov</a>.</p>"
			
			$("#blazeDisplay").html(data);
		}
		
	});
}

function getDNAFromRNA(url, rna){
	$.ajax({
		
		url:url,
		type: "POST",
		data: {"rna": rna},
		success: function(data){
		
				return data.dna;
		},
		
	});
}

function getProteinFromRNA(url, rna){
	$.ajax({
	
		url:url,
		type: "POST",
		data: {"rna": rna},
		success: function(data){
			return data.protein;	
		},
		
	});
}

function getTopologyFilePath(url, sequences){
	$.ajax({
		
		url: url,
		type: "POST",
		data: {'unaligned_sequences': sequences},
		success: function(data){
				
				setTopTree(data.file_path);
		},
		
	});
}

function getTopologyTreeString(url, sequences){
	$.ajax({
		
		url: url,
		type: "POST",
		data: {'unaligned_sequences': sequences},
		success: function(data){
				
				setTopTreeString(data.tree_string);
		},
		
	});
	
}

function getAlignment(url, dna){
	$.ajax({
		
		url: url,
		type: "POST",
		data: {'dna': dna},
		success: function(data){
				
				//return data.aligned_sequences;
		},
		
	});
	
}

function getDotMatrix(url, sequences, domSeq){
	
	$.ajax({
		
		url: url,
		type: "POST",
		data: {'sequences': sequences, 'dominant_species': domSeq},
		success: function(data){
				
				setDotMatrix(data.dot_matrix);
		},
		
	});
}


//In the form, have a file and the lab name.
//The lab name must have the name set to lab_name.
//The file must have the name set to lab_file.
function uploadFile(url, formData){
	
	$.ajax({
    	url: url,
    	type: "POST",
    	data: formData,
    	processData: false,  // tell jQuery not to process the data
  		contentType: false,   // tell jQuery not to set contentType
    	success: function(data){
    		return data.message;
    	},
    
    })
}