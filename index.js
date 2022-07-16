function sendMessageBatch(n){
	let body = {
		"body": generateData(n)
	};
	let options = {
		method: 'POST',
		mode: 'cors',
		credentials: 'omit',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	};
	fetch("http://127.0.0.1:5000/start/", options)
		.then((res) => console.log(res));
}

function generateData(n){
	let data = [];
	
	for(let i = 0; i < n; i++){
		data.push({
			id: i,
			body: "TEST MESSAGE"
		});
	}

	return data
}