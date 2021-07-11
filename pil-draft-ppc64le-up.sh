faas-cli delete -f ./pil-draft-ppc64le.yml
PROXY_URL="//10.3.0.3:3128";export http_proxy="http:$PROXY_URL";export https_proxy="http:$PROXY_URL";export no_proxy=.ibm-hcs.priv,localhost
faas-cli build --build-arg 'TEST_ENABLED=false' -f ./pil-draft-ppc64le.yml
if [ $? -eq 0 ]; then
 docker tag image-registry.openshift-image-registry.svc:5000/openfaas-fn/pil-draft-ppc64le:latest default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas-fn/pil-draft-ppc64le:latest
 #unset http_proxy;unset https_proxy
 docker push default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas-fn/pil-draft-ppc64le:latest --tls-verify=false
 faas-cli deploy -f pil-draft-ppc64le.yml
 oc get pods -w
 # faas-cli logs pil-draft-ppc64le
else
 echo Build failed
fi

