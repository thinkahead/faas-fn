# MAX Object Detector

## Description
The default http://gateway-external-openfaas.apps.ibm-hcs.priv/function/max-object-detector/ returns a page with html that does not use the base url of /function/max-object-detector but server the pages for swagger off /function/max-object-detector. So I had to add the static swagger-ui.html with URLs referring to /function/max-object-detector. Changes mentioned in the monkey path at https://github.com/noirbizarre/flask-restplus/issues/517#issuecomment-564733399 caused the swagger to be hosted off /function/max-object-detector/function/max-object-detector, so removed those changes.

## Links
* Swagger UI http://gateway-external-openfaas.apps.ibm-hcs.priv/function/max-object-detector/swagger-ui.html
* Web UI http://gateway-external-openfaas.apps.ibm-hcs.priv/function/max-object-detector/index.html
* Jupyter Notebook http://madi-notebook-route-default.apps.ibm-hcs.priv/notebooks/demo.ipynb
