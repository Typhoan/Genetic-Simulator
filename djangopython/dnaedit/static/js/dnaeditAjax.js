function getLabs(url){
	$.ajax({
		
		url: url,
		type: "GET",
		data: {},
		success: function(data){
		
				//var jsonParse = JSON.parse(data);
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
		
				//var jsonParse = JSON.parse(data);
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
		
				//var jsonParse = JSON.parse(data);
				console.log(data);
				return data.protein;
			},
		
	});

}


$.ajax({

	url:"{% url 'dnaedit:dnatorna' %}",
	type: "POST",
	data: {"dna": dataString},
	success: function(data){
	
			//var jsonParse = JSON.parse(data);
			console.log(data);
			rnaTest(JSON.stringify(data.rna));
		},
	
});
$.ajax({

	url:"{% url 'dnaedit:inverseDna' %}",
	type: "POST",
	data: {"dna": dataString},
	success: function(data){
	
			//var jsonParse = JSON.parse(data);
			console.log(data);
			
		},
	
});
$.ajax({

	url:"{% url 'dnaedit:distanceMatrix' %}",
	type: "POST",
	data: {"aligned_sequences": dataString},
	success: function(data){
	
			//var jsonParse = JSON.parse(data);
			console.log(data);
			
		},
	
});
$.ajax({

	url:"{% url 'dnaedit:blaze' %}",
	type: "POST",
	data: {"sequence": $("#speciesValue1").val()},
	success: function(data){
	
			//var jsonParse = JSON.parse(data);
			console.log(data);
			
		},
	
});