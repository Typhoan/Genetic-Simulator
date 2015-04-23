function getLabs(url){
	$.ajax({
		
		url: url,
		type: "GET",
		data: {},
		success: function(data){
		
				console.log(data);
				return data.labs;
				
			},
		
	});
}

function getFiles(url, labId){
	$.ajax({
		
		url: url,
		type: "GET",
		data: {'lab_id': labId},
		success: function(data){
				console.log(data);
				
				return data.files
			},
		
	});
}

function getProteinFromDNA(url, dna){
	$.ajax({
		
		url:url,
		type: "POST",
		data: {"dna": dna},
		success: function(data){
		
				console.log(data);
				return data.protein;
			},
		
	});

}

function getRNAFromDNA(url, dna){
	$.ajax({
	
		url: url,
		type: "POST",
		data: {"dna": dna},
		success: function(data){
		
				console.log(data);
				return data.rna;
			},
		
	});
	
}

function getInverseDNA(url, dna){
	$.ajax({
	
		url:url,
		type: "POST",
		data: {"dna": dna},
		success: function(data){
		
				console.log(data);
				return data.inverse_dna;
				
			},
		
	});

}

function getDistanceMatrix(url, dna){
	$.ajax({
	
		url:url,
		type: "POST",
		data: {"dna": dna},
		success: function(data){
		
				console.log(data);
				return data.distance_matrix;
			},
		
	});
}

function getBlazeReport(url, sequence){
	$.ajax({
	
		url:url,
		type: "POST",
		data: {"sequence": sequence},
		success: function(data){
				console.log(data);
				return data.blaze_report;
			},
		
	});
}

function getDNAFromRNA(url, rna){
	$.ajax({
		
		url:url,
		type: "POST",
		data: {"rna": rna},
		success: function(data){
		
				console.log(data);
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
			console.log(data);
			return data.protein;	
		},
		
	});
}

function getFileSequences(url, fileId){
	$.ajax({
			
			url: url,
			type: "GET",
			data: {'file_id': fileId},
			success: function(data){
					console.log(data);
					
					return data.sequences;
				},
			
	});
}

function getTopologyFilePath(url, sequences){
	$.ajax({
		
		url: url,
		type: "POST",
		data: {'sequences': sequences},
		success: function(data){
				console.log(data);
				
				return data.file_path;
			},
		
	});
}

function getTopologyTreeString(url, sequences){
	$.ajax({
		
		url: url,
		type: "POST",
		data: {'unalligned_sequences': sequences},
		success: function(data){
				console.log(data);
				
				return data.tree_string;
			},
		
	});
	
}

function getAlignment(url, dna){
	$.ajax({
		
		url: url,
		type: "POST",
		data: {'dna': dna},
		success: function(data){
				console.log(data);
				
				return data.aligned_sequences;
			},
		
	});
	
}

function getDotMatrix(url, sequences){
	
	$.ajax({
		
		url: url,
		type: "POST",
		data: {'sequences': sequences},
		success: function(data){
				console.log(data);
				
				return data.dot_matrix;
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
    		console.log(data);
    		return data.message;
    	},
    
    })
}