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

### Average results from 3 executions with placement config1

![config1_avg_times](https://user-images.githubusercontent.com/57920951/150173565-6316c9f3-ba77-48a5-b7b8-86aac683d2bd.png)

* with config1: 

![Screenshot from 2022-01-19 18-19-54](https://user-images.githubusercontent.com/57920951/150173762-df3fed45-af57-4b42-ae7e-8a4f12027855.png)


### Average results from 3 executions with placement config2

![config2_avg_times_correct](https://user-images.githubusercontent.com/57920951/150394887-3a1671ee-3b2f-4cff-99b8-740d7c56ca58.png)

* with config2:
All functions placed in the same node.

## Example Usage

![Screenshot from 2022-01-15 20-41-39](https://user-images.githubusercontent.com/57920951/149634004-1356f129-a036-4c0b-857b-aa24e710a2ba.png)


