# MAX Image Segmenter

## Description
The default http://gateway-external-openfaas.apps.ibm-hcs.priv/function/max-image-segmenter/ returns a page with html that does not use the base url of /function/max-image-segmenter but server the pages for swagger off /function/max-image-segmenter. So I had to add the static swagger-ui.html with URLs referring to /function/max-image-segmenter and swagger2.json. Changes mentioned in the monkey path at https://github.com/noirbizarre/flask-restplus/issues/517#issuecomment-564733399 caused the swagger to be hosted off /function/max-image-segmenter/function/max-image-segmenter, so removed those changes.

## Links
* Swagger UI http://gateway-external-openfaas.apps.ibm-hcs.priv/function/max-image-segmenter/swagger-ui.html
* Web UI http://gateway-external-openfaas.apps.ibm-hcs.priv/function/max-image-segmenter/index.html
* Jupyter Notebook http://madi-notebook-route-default.apps.ibm-hcs.priv/notebooks/demo.ipynb
