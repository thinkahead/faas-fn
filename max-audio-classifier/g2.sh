faas-cli delete max-audio-classifier
PROXY_URL="//10.3.0.3:3128";export http_proxy="http:$PROXY_URL";export https_proxy="http:$PROXY_URL";export no_proxy=localhost,127.0.0.1,.ibm-hcs.priv,10.3.158.61
docker build -t max-audio-classifier .
if [ $? -eq 0 ]; then
 docker tag max-audio-classifier default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas-fn/max-audio-classifier
 unset http_proxy;unset https_proxy
 oc whoami -t > /tmp/oc_token
 docker login --tls-verify=false -u kubeadmin default-route-openshift-image-registry.apps.ibm-hcs.priv -p `cat /tmp/oc_token`
 docker push default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas-fn/max-audio-classifier --tls-verify=false
 faas-cli deploy -f ../max-audio-classifier.yml
 for i in {1..10}; do
  oc get deployment/max-audio-classifier -n openfaas-fn | grep "1/1"
  if [ $? -eq 0 ]; then
   break
  fi
  sleep 2
 done 
 oc logs deployment/max-audio-classifier -n openfaas-fn -f
fi

