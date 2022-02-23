# Serverless-app-versions

Main repository for Master thesis on serverless.

## Description
* In [functions](https://github.com/dimgiagos44/Serverless-app-versions/tree/main/functions) directory there exist 4 versions of the same ML Workflow
* Each version consists of functions of different granularity
* Version1 is the most fine-grained, while Version4 is the most coarse-grained of the versions
* After deploying all the functions, by using the [exec script](https://github.com/dimgiagos44/Serverless-app-versions/blob/main/exec.sh)
we can run the desired instance on our local cluster as many times as we like in a sequential way of invocations
```
./exec.sh version1 url1 --times=10 yes yes --sleep=5s --step=15s
```
* We can scale each function's replicas up or down so as to make the versions capable
of serving more or less requests per minute
```
kubectl scale deployment version1 -n openfaas-fn --replicas=2
```
<!---
### Configs:
* config1: 
![Screenshot from 2022-01-19 18-19-54](https://user-images.githubusercontent.com/57920951/150173762-df3fed45-af57-4b42-ae7e-8a4f12027855.png)

* config2: 
all functions placed on the worker3 (coroni) 

* config3: 
all functions placed on the worker1 (davinci)
--->
## Example Usage

![Screenshot from 2022-01-15 20-41-39](https://user-images.githubusercontent.com/57920951/149634004-1356f129-a036-4c0b-857b-aa24e710a2ba.png)
