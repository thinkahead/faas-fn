#!/usr/bin/env python

from joblib import Parallel, delayed
import time
import os
import subprocess
import sys

def process(index,total,value):
    value=str(value)
    print("Processing",index,"/",total,value, flush=True)
    retrycount=0
    while True:
        # create two files to hold the output and errors, respectively
        with open("/tmp/"+value+'.out','w+') as fout:
            with open("/tmp/"+value+'.err','w+') as ferr:
                cmd="printf \""+value+"\\\n\" | curl -X POST --data-binary @- http://gateway-external-openfaas.apps.ibm-hcs.priv/function/pi-ppc64le -H \"Content-Type: text/plain\""
                out = subprocess.Popen(cmd,shell=True,stdout=fout,stderr=ferr)
                out.wait(1200) # Wait upto 20 minutes for each request
                #print("returncode for "+value,out.returncode)
                # reset file to read from it
                fout.seek(0)
                # save output (if any) in variable
                output=fout.read()
                # reset file to read from it
                ferr.seek(0)
                # save errors (if any) in variable
                errors = ferr.read()
                #print("output",output)
                #print("errors",errors)
                if out.returncode!=0:
                    if retrycount>=10:
                        print("Giving Up returncode",out.returncode,"retrycount",retrycount,value)
                        return "*"+value
                    retrycount=retrycount+1
                    print("Sleeping 120s because returncode",out.returncode,"retrycount",retrycount,value)
                    print("output",output)
                    print("errors",errors)
                    time.sleep(120.1)
                    continue
                if output.find("Concurrent request limit exceeded.")>=0:
                    if retrycount>=10:
                        print("Giving Up Concurrent request limit exceeded. retrycount",retrycount,value)
                        return "*"+value
                    retrycount=retrycount+1
                    print("Sleeping 150s because Concurrent request limit exceeded. retrycount",retrycount,value)
                    time.sleep(150.1)
                    continue
                if output.find("Killed")>=0 or errors.find("Killed")>=0:
                    if retrycount>=10:
                        print("Giving Up Killed. retrycount",retrycount,value)
                        return "*"+value
                    retrycount=retrycount+1
                    print("Sleeping 60s because Killed. retrycount",retrycount,value)
                    time.sleep(60.1)
                    continue
                print("Processed",index,"/",total,value, flush=True)
                return value

values=[i for i in range(1800,2200,3)]
total=len(values)
results = Parallel(n_jobs=64, prefer="threads")(delayed(process)(index,total,value) for index,value in enumerate(values))
print(results, flush=True)

