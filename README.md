# Serverless-app-versions

Main repository for Master thesis on serverless.

## Description
* In [functions](https://github.com/dimgiagos44/Serverless-app-versions/tree/main/functions) there exist 4 versions of the same ML Workflow
* Each version consists of functions of different granularity
* Version1 is the most fine-grained, while Version4 is the most coarse-grained of the versions
* After deploying all the functions, by using the [exec script](https://github.com/dimgiagos44/Serverless-app-versions/blob/main/exec.sh)
we can run the desired instance on our local cluster as many times as we like in a sequential way of invocations
```
./exec.sh version1 url1 --times=10 yes yes --sleep=5s
```
* We can scale each function's replicas up or down so as to make the versions capable
of serving more or less requests per minute
```
kubectl scale deployment version1 -n openfaas-fn --replicas=2
```

## Comparative executions of two inputs
### Results from one execution
* Url1's duration = 135 seconds with total  8 frames created & processed (1 per 15 seconds)
* Url4's duration = 215 seconds with total 13 frames created & processed (1 per 15 seconds)
* Url5's duration = 260 seconds with total 17 frames created & processed (1 per 15 seconds)

![Screenshot from 2022-01-17 12-01-36](https://user-images.githubusercontent.com/57920951/149748857-ba70a7fa-cb70-41b0-b722-875a07e30ae3.png)

(Executions took place on 17 Januray 2022)

### Average results from 4 executions

![Screenshot from 2022-01-19 11-07-09](https://user-images.githubusercontent.com/57920951/150099964-1a678f9d-4758-480c-9b28-c9f77a38cf26.png)


## Example Usage

![Screenshot from 2022-01-15 20-41-39](https://user-images.githubusercontent.com/57920951/149634004-1356f129-a036-4c0b-857b-aa24e710a2ba.png)


