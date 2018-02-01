## About the project

This is a example for istio on kubernetes, Which with two service write in nodejs and python.

the more info about [the project](https://my.oschina.net/ganity/blog/1616866)

and the dependents like

![应用调用关系](https://static.oschina.net/uploads/img/201802/01134407_Ma0b.png "应用调用关系")

## How to use

make sure you have install kubernetes and Istio

### build docker image

- hello-node image

`cd nodeserver`

and then

`docker build -t hello-node:v1 .`

if you use Minikube, please do `eval $(minikube docker-env)` first.

- hello-py image

`cd pythonserver`

`docker build -t hello-py:v1 .`

### deployment 

`kubectl apply -f hello-istio.yaml`

### Access

use the ingress IP address to access the server

`kubectl get ingress -o wide`

Or if you use minikube
`export GATEWAY_URL=$(kubectl get po -l istio=ingress -n istio-system -o 'jsonpath={.items[0].status.hostIP}'):$(kubectl get svc istio-ingress -n istio-system -o 'jsonpath={.spec.ports[0].nodePort}')`

then

`curl $GATEWAY_URL`

and the Result:

```json
{
  "code": 200, 
  "data": {"name": "nodejs-istio", "value": "Hello World!"}, 
  "version": "1.0.0", 
  "author": "hello-py"
}
```
