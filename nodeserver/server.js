var http = require('http');

var handleRequest = function(request, response) {
  console.log('Received request for URL: ' + request.url);
  response.writeHead(200, {'Content-Type': 'application/json'});
  var data = {  
	    "name":"nodejs-istio",  
	    "value":"Hello World!"  
	};  
	response.end(JSON.stringify(data));  
};
var www = http.createServer(handleRequest);
www.listen(8080);