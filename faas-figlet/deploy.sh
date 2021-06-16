echo PASSWORD=$PASSWORD
curl http://admin:$PASSWORD@localhost:8081/system/functions -d '{"service": "figlet", "image": "karve/faas-figlet", "envProcess": "figlet", "network": "func_functions"}'
curl http://admin:$PASSWORD@127.0.0.1:8081/system/functions
