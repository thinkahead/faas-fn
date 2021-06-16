# OpenFaas for ppc64le

## Figlet
```
faas-cli build -f ./faas-figlet.yml
docker push karve/faas-figlet
kubectl port-forward -n openfaas svc/gateway 8081:8080 &
faas-cli deploy -f ./faas-figlet.yml
faas-cli list --gateway http://localhost:8081
curl http://localhost:8081/function/figlet -d Test
```

## Hello Python
```
kubectl port-forward -n openfaas svc/gateway 8081:8080 &
echo -n $PASSWORD | faas-cli login --username admin --password-stdin --gateway http://127.0.0.1:8081

cd /root/alexei/faas-fn
faas-cli new hello-ppc64le --lang python-ppc64le

handler.py
    return "Input: {}".format(req)

faas-cli build -f ./hello-ppc64le.yml
docker push karve/hello-ppc64le
faas-cli deploy -f ./hello-ppc64le.yml
oc get pods -n faas-fn
faas-cli list --gateway http://localhost:8081

oc create secret docker-registry docker --docker-server=docker.io --docker-username=karve --docker-password=8e711978-0734-4e7e-91ac-8468e5a174c8 --docker-email=karve@us.ibm.com -n openfaas-fn
oc secrets link default docker --for=pull -n openfaas-fn

unset http_proxy;unset https_proxy
curl http://admin:$PASSWORD@localhost:8081/function/hello-ppc64le -d 'Alexei'
faas-cli delete -f ./hello-ppc64le.yml
#faas-cli delete hello-ppc64le --gateway http://localhost:8081
```

# Hello Node10
```
faas-cli new hello-node10-ppc64le --lang node10-express
vi hello-node10-ppc64le/handler.js # https://github.com/openfaas-incubator/node10-express-template/
PROXY_URL="//10.3.0.3:3128";export http_proxy="http:$PROXY_URL";export https_proxy="http:$PROXY_URL"
faas-cli build -f ./hello-node10-ppc64le.yml
docker push karve/hello-node10-ppc64le
faas-cli deploy -f ./hello-node10-ppc64le.yml
faas-cli list --gateway http://localhost:8081
echo "Hi" | faas-cli invoke hello-node10-ppc64le --gateway http://localhost:8081
unset http_proxy;unset https_proxy
echo -n "hello" | faas-cli invoke hello-node10-ppc64le --gateway http://localhost:8081
uname -a | curl -X POST --data-binary @- http://localhost:8081/function/hello-node10-ppc64le -vvv -H "Content-Type:text/plain"
curl http://admin:$PASSWORD@localhost:8081/function/hello-node10-ppc64le -d 'Hi' -H "Content-Type:text/plain"
faas-cli delete hello-node10-ppc64le --gateway http://localhost:8081
```
