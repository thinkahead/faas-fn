# OpenFaas on ppc64le

## Images used by openfaas install for ppc64le
- **alertmanager** image: prom/alertmanager-linux-ppc64le    
- **basic-auth-plugin** image: image-registry.openshift-image-registry.svc:5000/openfaas/basic-auth:latest-dev    
- **gateway** image: image-registry.openshift-image-registry.svc:5000/openfaas/gateway:latest-dev and image: image-registry.openshift-image-registry.svc:5000/openfaas/faas-netes:latest-dev    
- **nats** image: image-registry.openshift-image-registry.svc:5000/openfaas/nats-streaming:latest-dev    
- **prometheus** image: prom/prometheus-linux-ppc64le    
- **queue-worker** image: image-registry.openshift-image-registry.svc:5000/openfaas/nats-queue-worker:latest-dev    

## Dockerfile and docker-entrypoint for nats-streaming-server used in next section
docker/Dockerfile
```
FROM --platform=${BUILDPLATFORM:-linux/ppc64le} golang:1.16-alpine AS builder

ARG TARGETPLATFORM
ARG BUILDPLATFORM

RUN apk add --update git
RUN apk add build-base

WORKDIR $GOPATH/src/github.com/nats-io/nats-streaming-server

MAINTAINER Alexei Karve <karve@us.ibm.com>

COPY . .

RUN CGO_ENABLED=0 GO111MODULE=off GOARCH=ppc64le go build -v -a -tags netgo -installsuffix netgo -ldflags "-s -w -X github.com/nats-io/nats-streaming-server/server.gitCommit=`git rev-parse --short HEAD`" -o /nats-streaming-server

FROM --platform=${TARGETPLATFORM:-linux/ppc64le} alpine:latest

RUN apk add --update ca-certificates

COPY --from=builder /nats-streaming-server /usr/local/bin/nats-streaming-server
RUN ln -s /usr/local/bin/nats-streaming-server /nats-streaming-server
COPY docker-entrypoint.sh /usr/local/bin
EXPOSE 4222 8222
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["nats-streaming-server", "-m", "8222"]
```
docker/docker-entrypoint.sh
https://github.com/nats-io/nats-streaming-docker/blob/main/0.22.1/alpine3.14/docker-entrypoint.sh
```
#!/bin/sh
set -e

# this if will check if the first argument is a flag
# but only works if all arguments require a hyphenated flag
# -v; -SL; -f arg; etc will work, but not arg1 arg2
if [ "$#" -eq 0 ] || [ "${1#-}" != "$1" ]; then
    set -- nats-streaming-server "$@"
fi

# else default to run whatever the user wanted like "bash" or "sh"
exec "$@"
```

## Building images for ppc64le
```
git clone https://github.com/openfaas/faas.git
cd faas
# image: image-registry.openshift-image-registry.svc:5000/openfaas/gateway:latest-dev
cd gateway
docker build --build-arg BUILDPLATFORM=linux/ppc64le --build-arg http_proxy=http://10.3.0.3:3128 --build-arg https_proxy=http://10.3.0.3:3128 -t default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas/gateway:latest-dev .
docker push default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas/gateway:latest-dev --tls-verify=false
# image: image-registry.openshift-image-registry.svc:5000/openfaas/basic-auth:latest-dev
cd ../auth/basic-auth
docker build --build-arg BUILDPLATFORM=linux/ppc64le --build-arg http_proxy=http://10.3.0.3:3128 --build-arg https_proxy=http://10.3.0.3:3128 -t default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas/basic-auth:latest-dev .
docker push default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas/basic-auth:latest-dev --tls-verify=false
# image: image-registry.openshift-image-registry.svc:5000/openfaas/faas-netes:latest-dev
git clone https://github.com/openfaas/faas-netes.git
cd faas-netes
docker build --build-arg BUILDPLATFORM=linux/ppc64le --build-arg http_proxy=http://10.3.0.3:3128 --build-arg https_proxy=http://10.3.0.3:3128 -t default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas/faas-netes:latest-dev .
docker push default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas/faas-netes:latest-dev --tls-verify=false
# image: image-registry.openshift-image-registry.svc:5000/openfaas/nats-streaming:latest-dev
git clone https://github.com/nats-io/nats-streaming-server.git
cd nats-streaming-server
# Create docker/Dockerfile and docker/docker-entrypoint.sh as in previous section
docker build --build-arg TARGETPLATFORM=linux/ppc64le --build-arg http_proxy=http://10.3.0.3:3128 --build-arg https_proxy=http://10.3.0.3:3128 -t default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas/nats-streaming:latest-dev -f docker/Dockerfile .
docker push default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas/nats-streaming:latest-dev --tls-verify=false
# image: image-registry.openshift-image-registry.svc:5000/openfaas/nats-queue-worker:latest-dev
# Comment out the following line in Dockerfile, it gives error on ppc64le because the /scratch-tmp is empty
#COPY --from=golang --chown=app:app /scratch-tmp /tmp
docker build --build-arg http_proxy=http://10.3.0.3:3128 --build-arg https_proxy=http://10.3.0.3:3128 -t default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas/nats-queue-worker:latest-dev .
docker push default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas/nats-queue-worker:latest-dev --tls-verify=false
```
## Building faas-cli for ppc64le
```
git clone https://github.com/openfaas/faas-cli.git
cd faas-cli
# change Dockerfile and optionally Dockerfile.redist
-FROM teamserverless/license-check:0.3.9 as license-check
+FROM teamserverless/license-check:latest-ppc64le as license-check

# modify build.sh to add --build-arg BUILDPLATFORM=linux/ppc64le in both docker build lines
#./build.sh
# or
docker build --build-arg BUILDPLATFORM=linux/ppc64le --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy --target release -t openfaas/faas-cli:latest-dev .
docker create --name faas-cli openfaas/faas-cli:latest-dev && docker cp faas-cli:/usr/bin/faas-cli . && docker rm -f faas-cli
sudo mv faas-cli /usr/local/bin
```

## Building arkade for ppc64le (Optional)
If you want to use helm, arkade is not required.
```
# modify Makefile under dist
CGO_ENABLED=0 GOOS=linux GOARCH=ppc64le go build -ldflags $(LDFLAGS) -a -installsuffix cgo -o bin/arkade
make
# Creates bin/arkade
```

## Building watchdog (Optional)
The watchdog is used in Dockerfiles used by functions. You do not need to build this. Instead, you can use the docker.io/powerlinux/classic-watchdog:latest-dev-ppc64le as watchdog. However if you build it, then you can copy over the bin/fwatchdog-ppc64le into the template folder with the Dockerfile for functions
```
git clone https://github.com/openfaas/classic-watchdog.git
cd classic-watchdog
# modify Makefile under dist
GOARCH=ppc64le CGO_ENABLED=0 GOOS=linux go build -mod=vendor -a -ldflags $(LDFLAGS) -installsuffix cgo -o bin/fwatchdog-ppc64le
make
ls bin/fwatchdog-ppc64le
cd ..

git clone https://github.com/openfaas/of-watchdog.git
cd of-watchdog
# modify Makefile under dist
GOARCH=ppc64le CGO_ENABLED=0 GOOS=linux go build -mod=vendor -a -ldflags "-s -w -X main.Version=0.8.4-1-g989ac5f-dirty-1623851326 -X main.GitCommit=989ac5f0d2b4560d7b1d9f18d0231449527cc47c" -installsuffix cgo -o bin/fwatchdog-ppc64le
make
ls bin/fwatchdog-ppc64le
cd ..
```
More details about both the classic watchdog and of-watchdog are at https://docs.openfaas.com/architecture/watchdog/

## Issues
### Tight container limits may cause "read init-p: connection reset by peer"
This problem occurs on alertmanager. It is fixed by change memory to 250Mi and 500Mi in the alertmanager template.
https://github.com/opencontainers/runc/issues/1914

### Dockerhub limit reached
```
oc create secret docker-registry docker --docker-server=docker.io --docker-username=$user --docker-password=$token --docker-email=$email -n openfaas
oc secrets link default docker --for=pull -n openfaas
oc get serviceaccounts | grep openfaas
oc secrets link openfaas-prometheus docker --for=pull -n openfaas
oc secrets link openfaas-operator docker --for=pull -n openfaas
oc secrets link openfaas-controller docker --for=pull -n openfaas
```
### forbidden: cannot set blockOwnerDeletion if an ownerReference refers to a resource you can't set finalizers
https://github.com/openfaas/faas-netes/issues/807
It probably requires adding the rule with some specific resource/finalizer to openfaas-operator-rw role in openfaas-fn namespace or openfaas-operator-controller clusterrole. It works with the rule below added:
```
  - apiGroups:
    - openfaas.com
    resources:
    - '*'
    verbs:
    - update
```

### Error in the name of component openfaas-operator
component: openaas-operator should be changed to component: openfaas-operator in the template
https://github.com/openfaas/faas-netes/blob/master/chart/openfaas/templates/operator-rbac.yaml#L113

## Installing openfaas
### Using arkade
**install-with-arkade.sh**
```
#!/bin/bash

export TIMEOUT=60s
arkade install openfaas --set securityContext=false --set gateway.upstreamTimeout=$TIMEOUT  \
 --set gateway.writeTimeout=$TIMEOUT \
 --set gateway.readTimeout=$TIMEOUT  \
 --set faasnetes.writeTimeout=$TIMEOUT  \
 --set faasnetes.readTimeout=$TIMEOUT  \
 --set queueWorker.ackWait=$TIMEOUT \
 --operator \
 --set gateway.directFunctions=false  \
 --set nats.image=image-registry.openshift-image-registry.svc:5000/openfaas/nats-streaming:latest-dev \
 --set gateway.image=image-registry.openshift-image-registry.svc:5000/openfaas/gateway:latest-dev \
 --set basicAuthPlugin.image=image-registry.openshift-image-registry.svc:5000/openfaas/basic-auth:latest-dev \
 --set faasnetes.image=image-registry.openshift-image-registry.svc:5000/openfaas/faas-netes:latest-dev \
 --set operator.image=image-registry.openshift-image-registry.svc:5000/openfaas/faas-netes:latest-dev \
 --set queueWorker.image=image-registry.openshift-image-registry.svc:5000/openfaas/nats-queue-worker:latest-dev \
 --set prometheus.image=prom/prometheus-linux-ppc64le \
 --set alertmanager.image=prom/alertmanager-linux-ppc64le \
 --set alertmanager.resources.requests.memory=250Mi \
 --set alertmanager.resources.limits.memory=500Mi
# --set clusterRole=true
sleep 3
oc secrets link openfaas-prometheus docker --for=pull -n openfaas
oc secrets link openfaas-operator docker --for=pull -n openfaas
oc secrets link openfaas-controller docker --for=pull -n openfaas
oc secrets link default docker --for=pull -n openfaas
```
**Installing**
```
chmod +x install-with-arcade.sh
./install-with-arcade.sh
```

### Using helm
```
cd chart && helm package openfaas/ && helm package kafka-connector/ && helm package cron-connector/ && helm package nats-connector/ && helm package mqtt-connector/
kubectl -n openfaas create secret generic basic-auth --from-literal=basic-auth-user=admin --from-literal=basic-auth-password="$PASSWORD"
# helm upgrade openfaas --install chart/openfaas-7.3.0.tgz --namespace openfaas --set basic_auth=true --set functionNamespace=openfaas-fn --set operator.create=true --set securityContext=false --set gateway.scaleFromZero=false
helm upgrade --install openfaas chart/openfaas-7.3.0.tgz --namespace openfaas --set gateway.replicas=1 --set queueWorker.replicas=1 --set serviceType=NodePort --set openfaasImagePullPolicy=IfNotPresent --set faasnetes.imagePullPolicy=Always --set basicAuthPlugin.replicas=1 --set basic_auth=true --set clusterRole=false --set gateway.directFunctions=false --set ingressOperator.create=false --set queueWorker.maxInflight=1 --set securityContext=false --set operator.create=true
kubectl -n openfaas get deployments -l "release=openfaas, app=openfaas" -w
kubectl get events -n openfaas-fn --sort-by=.metadata.creationTimestamp 
```

## Uninstalling openfaas
Use helm to delete openfaas for both above cases.
```
helm delete openfaas --namespace openfaas
```

## Samples
### Return PI or Euler's number to the wanted accuracy
#### Print value of Pi to fixed accuracy
The dockerfile-ppc64le template contains a Dockerfile using perl from alpine:3.12 docker image. The ENV is set as follows for computing the value of Pi with the fixed value of 100 digits
```
ENV fprocess='perl -Mbignum=bpi -wle print(bpi(100))'
```

The Dockerfile in dockerfile-ppc64le refers to the classic-watchdog ppc64le binary that can either be compiled locally or from docker.io/powerlinux
```
#FROM ghcr.io/openfaas/classic-watchdog:0.1.5 as watchdog
FROM docker.io/powerlinux/classic-watchdog:latest-dev-ppc64le as watchdog
```

The following snippet shows all the commands to build, deploy and invoke this function on openfaas
```
export OPENFAAS_PREFIX=karve
export OPENFAAS_URL=http://gateway-external-openfaas.apps.ibm-hcs.priv
faas-cli new pi-$OPENFAAS_PREFIX-ppc64le --lang dockerfile-ppc64le # --prefix=$OPENFAAS_PREFIX
vi pi-$OPENFAAS_PREFIX-ppc64le/Dockerfile # Append perl to apk add. It will install perl 5.30.3-r0
sed -i "s/lang: dockerfile-ppc64le/lang: dockerfile/" pi-$OPENFAAS_PREFIX-ppc64le.yml # Change lang: dockerfile
#vi pi-$OPENFAAS_PREFIX-ppc64le.yml # Change lang: dockerfile
faas-cli build -f pi-$OPENFAAS_PREFIX-ppc64le.yml
docker login -u $OPENFAAS_PREFIX
docker push $OPENFAAS_PREFIX/pi-$OPENFAAS_PREFIX-ppc64le
faas-cli deploy -f ./pi-$OPENFAAS_PREFIX-ppc64le.yml
echo "" | faas-cli invoke pi-karve-ppc64le --gateway $OPENFAAS_URL
curl $OPENFAAS_URL/function/pi-$OPENFAAS_PREFIX-ppc64le
#rm -rf pi-$OPENFAAS_PREFIX-ppc64le*
```
Replace the ENV with bpi(100) in Dockerfile with bexp(1,100) to find the value of e raised to appropriate power or any other function https://perldoc.perl.org/bignum

#### Auto scaling
```
faas-cli deploy -f ./pi-$OPENFAAS_PREFIX-ppc64le.yml --label com.openfaas.scale.max=10 --label com.openfaas.scale.min=1
faas-cli describe pi-$OPENFAAS_PREFIX-ppc64le --gateway $OPENFAAS_URL
for i in {0..100}; do echo "" | faas-cli invoke pi-$OPENFAAS_PREFIX-ppc64le --gateway $OPENFAAS_URL && echo; done;
watch "faas-cli describe pi-$OPENFAAS_PREFIX-ppc64le --gateway $OPENFAAS_URL;oc get pods -n openfaas-fn"
```
In prometheus graph
```
rate( gateway_function_invocation_total{code="200"} [20s])
```

Instead of the for loop in bash to generate load, we can use hey https://github.com/rakyll/hey
```
hey -z=5m -q 100 -c 20 -m POST -d=Test http://gateway-external-openfaas.apps.ibm-hcs.priv//function/pi-karve-ppc64le
```
The options -c will simulate 20 concurrent users, -z will run for 5m and then complete, -q rate limit in queries per second (QPS) 100 per worker.

#### Generate the new pi-ppc64le
Use the dockerfile-perl template or the dockerfile-ppc64le. The Dockerfile in dockerfile-perl template is updated for installing perl 5.32.0 as in https://github.com/scottw/alpine-perl. The dockerfile-ppc64le uses that perl 5.30.3-r0.

```
faas-cli new pi-ppc64le --lang dockerfile-perl
```
This template also contains a Dockerfile that installs perl with the following ENV for computing the value of Pi with the fixed value of 100 digits as before. In this scenario, we want to send input withmultiple lines, each line containing the accuracy in number of digits desired. This will thus print values of PI or Euler's number to multiple digits of accuracy.

I could not however figure out how to escape the ENV for fprocess with either of the following:
```
'foreach my $line ( <STDIN> ) { chomp($line);if ($line=~/^$/) { last; } print(bpi($line)); }'
"foreach my \$line ( <STDIN> ) { chomp(\$line);if (\$line=~/^\$/) { last; } print(bpi(\$line)); }"
```
If someone can find the appropriate escape characters for ENV, please leave comments below.  I added a separate file runme.pl to invoke it in fprocess. 

**runme.pl** for PI
```
#!/usr/local/bin/perl
use bignum;
foreach my $line ( <STDIN> ) { chomp($line);print $line,"\n";if ($line=~/^$/) { last; } print(bignum::bpi($line),"\n"); }
```
For above, we can provide multiple lines as follows where each l;ine is the desired accuracy:
```
10
100

```

**runme.pl** for Euler's number e raised to the appropriate power, to the wanted accuracy.
```
#!/usr/local/bin/perl
use bignum;
foreach my $line ( <STDIN> ) { chomp($line);print $line,"\n";if ($line=~/^$/) { last; } print(bignum::bexp((split(' ',$line))[0],(split(' ',$line))[1]),"\n"); }
```
For above, we can provide multiple lines as follows where first number in each line is the power and second is the desired accuracy:
```
1 20
1 30
2 30

```

Replace the "ENV fprocess" in Dockerfile with the lines below:
```
COPY runme.pl /home/app/runme.pl
ENV fprocess="/home/app/runme.pl"
```

#### Update the pi-ppc64le.yml
The faas-cli build command however adds the Dockerfile from the template into the build/pi2-ppc64le/function/ directory instead of the build/pi2-ppc64le/. So we change the lang: dockerfile-perl to lang: dockerfile.
Also update the image: pi-ppc64le:latest with image: karve/pi-ppc64le:latest
and gateway: http://gateway-external-openfaas.apps.ibm-hcs.priv
If you are going to provide larger values for accuracy, you will need to increase the timeouts in template.yml in the environment. https://github.com/openfaas/faas-cli
```
    environment:
      read_timeout: "20s"
      write_timeout: "20s"
      exec_timeout: "20s"
```
#### Test locally on docker
```
faas-cli build -f ./pi-ppc64le.yml && docker run --rm -p 8081:8080 --name test-this karve/pi-ppc64le
curl http://127.0.0.1:8081 --data-binary @test
```
**test**
```
10
20
30

```

#### Test function on cluster
```
faas-cli build -f ./pi-ppc64le.yml
docker push karve/pi-ppc64le
faas-cli deploy -f ./pi-ppc64le.yml
faas-cli list --gateway http://gateway-external-openfaas.apps.ibm-hcs.priv
printf "10\n20\n30\n" | faas-cli invoke pi-ppc64le --gateway http://gateway-external-openfaas.apps.ibm-hcs.priv
printf "10\n20\n30\n" | curl -X POST --data-binary @- http://gateway-external-openfaas.apps.ibm-hcs.priv/function/pi-ppc64le -vvv -H "Content-Type:text/plain"
```
Output
```
10 3.141592654
20 3.1415926535897932385
30 3.14159265358979323846264338328
```

#### Delete the instance of pi-ppc64le
```
faas-cli delete pi-ppc64le --gateway http://gateway-external-openfaas.apps.ibm-hcs.priv
```

#### Testing with CRDs
We can build the image directly with docker command 
```
cd pi-ppc64le
doker build -t karve/pi-ppc64le .
cd ..
```
or use the image we built with the "faas-cli build" command previously.

We can install using the pi-ppc64le-function.yml if --operator is set during install of openfaas
```
oc apply -f pi-ppc64le-function.yml
oc get function -n openfaas-fn
```

#### Deleting the function
```
oc delete function pi-ppc64le -n openfaas-fn
```

To use the HPAv2, we need to comment out the following labels from the pi-ppc64le-function.yml and deploy again with -label com.openfaas.scale.factor=0.
```
  labels:
    com.openfaas.scale.min: "2"
    com.openfaas.scale.max: "15"
```

Alternatively, we can set the labels in the pi-ppc64le-function.yml and apply the yaml.
```
    labels:
      com.openfaas.scale.factor: 0
```

We can also disable auto-scaling by scaling alertmanager down to zero replicas, this will stop it from firing alerts.
```
kubectl scale -n openfaas deploy/alertmanager --replicas=0
```
We do not want to scale using prometheus alerts.

**Create a HPAv2 rule for CPU** The parameters -n openfaas-fn refers to where the function is deployed, pi-ppc64le is the name of the function, --cpu-percentage is the level of CPU the pod should reach before additional replicas are added, --min minimum number of pods, --max maximum number of pods. HPA calculates pod cpu utilization as total cpu usage of all containers in pod divided by total requested. https://github.com/kubernetes/kubernetes/blob/v1.9.0/pkg/controller/podautoscaler/metrics/utilization.go#L49
```
oc autoscale deployment -n openfaas-fn \
  pi-ppc64le \
  --cpu-percent=50 \
  --min=2 \
  --max=20
oc get hpa/pi-ppc64le -n openfaas-fn # View the HPA record

# Generate the load and watch the cpu load
hey -z=10m -c 2 -m POST -d=Test http://gateway-external-openfaas.apps.ibm-hcs.priv/function/pi-ppc64le --data-binary @test -H "Content-Type: text/plain"
watch "faas-cli describe pi-ppc64le --gateway $OPENFAAS_URL;oc get pods -n openfaas-fn" # Shows the number of replicas and invocations
watch "kubectl top pod -n openfaas-fn" # Usage of pods
watch "oc describe hpa/pi-ppc64le -n openfaas-fn" # Get detailed information including any events such as scaling up and down
```
HPA reacts slowly to changes in traffic, both for scaling up and for scaling down. In some instances you may wait more than 5 minutes for all your pods to scale back down to default level after the load has stopped.

Sample output from ```oc describe hpa/pi-ppc64le -n openfaas-fn```
```
Name:                                                  pi-ppc64le
Namespace:                                             openfaas-fn
Labels:                                                <none>
Annotations:                                           <none>
CreationTimestamp:                                     Mon, 21 Jun 2021 12:31:22 -0400
Reference:                                             Deployment/pi-ppc64le
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  49% (49m) / 50%
Min replicas:                                          2
Max replicas:                                          20
Deployment pods:                                       6 current / 6 desired
Conditions:
  Type            Status  Reason              Message
  ----            ------  ------              -------
  AbleToScale     True    ReadyForNewScale    recommended size matches current size
  ScalingActive   True    ValidMetricFound    the HPA was able to successfully calculate a replica count from cpu resource utilization (per
centage of request)
  ScalingLimited  False   DesiredWithinRange  the desired count is within the acceptable range
Events:
  Type    Reason             Age    From                       Message
  ----    ------             ----   ----                       -------
  Normal  SuccessfulRescale  3m53s  horizontal-pod-autoscaler  New size: 4; reason: cpu resource utilization (percentage of request) above
target
  Normal  SuccessfulRescale  3m37s  horizontal-pod-autoscaler  New size: 5; reason: cpu resource utilization (percentage of request) above
target
  Normal  SuccessfulRescale  3m22s  horizontal-pod-autoscaler  New size: 6; reason: cpu resource utilization (percentage of request) above
target
```

### Figlet
```
faas-cli build -f ./faas-figlet.yml
docker push karve/faas-figlet
kubectl port-forward -n openfaas svc/gateway 8081:8080 &
faas-cli deploy -f ./faas-figlet.yml
faas-cli list --gateway http://localhost:8081
curl http://localhost:8081/function/figlet -d Test
echo Hi | faas-cli invoke figlet --gateway http://localhost:8081
```

### Hello Python
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

### Hello Node10
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
## Timeouts
If the functions take a long time to respond
1. annotate the route with the higher timeout value
```
oc annotate route gateway-external --overwrite haproxy.router.openshift.io/timeout=600s -n openfaas
```
2. Set the appropriate timeouts in /etc/haproxy/haproxy.cfg
```
    timeout http-request    10s
    timeout queue           10m
    timeout connect         10s
    timeout client          10m
    timeout server          10m
    timeout http-keep-alive 10s
    timeout check           10s
```
3. Set the timeouts in the function definition environment
```
    environment:
      read_timeout: "600s"
      write_timeout: "600s"
      upstream_timeout: "600s"
      exec_timeout: "600s"
```

## Creating prometheus alert
For scaling up, try:
```
        - alert: APIHighRetryRate
          expr: sum(rate(gateway_function_invocation_total{code="429"}[10s])) BY (function_name) > 1
          for: 5s
          labels:
            service: gateway
            severity: major
          annotations:
            description: High retry rate on "{{$labels.function_name}}"
            summary: High retry rate on "{{$labels.function_name}}"
```
Add it to your config
```
oc edit -n openfaas configmap/prometheus-config
```
## OpenFaaS Dashboard in Grafana
```
PROXY_URL="//10.3.0.3:3128";export http_proxy="http:$PROXY_URL";export https_proxy="http:$PROXY_URL";export no_proxy=gateway-external-openfaas.apps.ibm-hcs.priv,localhost,127.0.0.1,api.ibm-hcs.priv,10.3.158.61
git clone https://github.com/stefanprodan/faas-grafana.git
cd faas-grafana/Grafana
# vi Dockerfile # Change FROM ibmcom/grafana-ppc64le:5.2.0-f4
docker build -t default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas/faas-grafana:5.2.0-f4 .
unset http_proxy;unset https_proxy
docker push default-route-openshift-image-registry.apps.ibm-hcs.priv/openfaas/faas-grafana:5.2.0-f4 --tls-verify=false
# Deploy a pod for Grafana
oc -n openfaas run --image=image-registry.openshift-image-registry.svc:5000/openfaas/faas-grafana:5.2.0-f4 --port=3000 grafana
oc -n openfaas expose pod grafana --type=NodePort --name=grafana
oc expose svc grafana
oc -n openfaas get routes grafana -o jsonpath='{.spec.host}'
```

## References
- Self-paced workshop for OpenFaaS https://github.com/openfaas/workshop/blob/master/README.md
- Manage functions with Kubelet https://www.openfaas.com/blog/manage-functions-with-kubectl/
- Metrics HPAv2 with OpenFaaS https://docs.openfaas.com/tutorials/kubernetes-hpa/
- Custom Alert for 429 https://github.com/openfaas/nats-queue-worker/issues/105#issuecomment-787494533
- Serverless Computing on Constrained Edge Devices https://helda.helsinki.fi/bitstream/handle/10138/314280/Tilles_Jan_Pro_gradu_2020.pdf?sequence=3&isAllowed=y
