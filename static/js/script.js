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
})