# MAX Audio Classifier

## Description
The default http://gateway-external-openfaas.apps.ibm-hcs.priv/function/max-audio-classifier/ returns a page with html that does not use the base url of /function/max-audio-classifier but server the pages for swagger off /function/max-audio-classifier. So I had to add the static swagger-ui.html with URLs referring to /function/max-audio-classifier and swagger2.json. Changes mentioned in the monkey path at https://github.com/noirbizarre/flask-restplus/issues/517#issuecomment-564733399 caused the swagger to be hosted off /function/max-audio-classifier/function/max-audio-classifier, so removed those changes.

## Links
* Swagger UI http://gateway-external-openfaas.apps.ibm-hcs.priv/function/max-audio-classifier/swagger-ui.html
* Web UI http://gateway-external-openfaas.apps.ibm-hcs.priv/function/max-audio-classifier/index.html
