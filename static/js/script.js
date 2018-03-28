$('#sel1').on('change', function() {
  	let value = this.value;
    let request = new XMLHttpRequest();
    let url = `http://localhost:3000/chain`;

    request.onreadystatechange = function() {
      if (this.readyState === 4 && this.status === 200) {
        let response = JSON.parse(this.responseText);
        let arr = response.chain[response.length-1].transations;
        getElements(arr,value);
      }
    }

    request.open("GET", url, true);
    request.send();

    getElements = function(arr,value) {
    	let pollutants = [];
    	let resources = [];
      for(var i = 0; i<arr.length;i++){
      	if(arr[i].entity === value){
      		pollutants = pollutants.concat(arr[i].pollutants);
      		resources = resources.concat(arr[i].resources_used);
      	}
      }
      console.log(pollutants,resources);
    }
});

$('#add').on('click',function(){
	$('#res').append("<div class='form-inline'><label for='resources'>Resources Used:</label><input type='text' class='form-control' id='resources'><label for='resources'>Quantity(in mg):</label><input type='text' class='form-control' id='resources'></div>")
});

$("#manufact").on('click',function(e) {
		var rec = $('#recieve').val();
		var sen = $('#send').val();
		var ent = $('#entity').val();
		var resource = $('.resources');
		var res=[];
		for(var i=0 ; i< resource.length;i+=2){
			res.append(`"${resource[i].value}":${resource[i+1].value}`);
		}
		console.log(resource);
        //prevent Default functionality
        e.preventDefault();
        var dataURL = {
			"reciever": `${rec}`,
			"sender": `${sen}`,
			"entity": `${ent}`,
			"resources_used": [{"plastic":25},{"Wood":2000}],
			"pollutants": ["CO2","SO2","CO"]
		}
        //get the action-url of the form
        var actionurl = `http://localhost:3000/transactions/new`;
        //do your own request an handle the results
        $.ajax({
                url: actionurl,
                type: 'post',
                contentType: 'application/json',
                data: JSON.stringify(dataURL),
                success: function(data) {
                    console.log(data)
                },
                error: function(err){
                	console.log(err);
                }
        });

    });

$('#mine').on('click', function() {
    let request = new XMLHttpRequest();
    let url = `http://localhost:3000/chain`;

    request.onreadystatechange = function() {
      if (this.readyState === 4 && this.status === 200) {
        let response = JSON.parse(this.responseText);
        alert("mining done");
      }
    }

    request.open("GET", url, true);
    request.send();
});
