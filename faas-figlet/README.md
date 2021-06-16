# faas-figlet
OpenFaaS Figlet image.

```
export no_proxy=localhost,127.0.0.1,api.ibm-hcs.priv,10.3.158.61
PROXY_URL="//10.3.0.3:3128";export http_proxy="http:$PROXY_URL";export https_proxy="http:$PROXY_URL"
kubectl port-forward -n openfaas svc/gateway 8081:8080 &
./build.sh
docker push karve/faas-figlet
./deploy.sh
./test.sh
```
