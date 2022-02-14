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
## Benchmarking

### Average results from version1 vs version4 with 4 different inputs with single node deployment (davinci)
* Url1's duration = 180 seconds (0-180) with total 11 frames created & processed (1 per 15 seconds)
* Url4's duration = 280 seconds (0-280) with total 18 frames created & processed (1 per 15 seconds)
* Url5's duration = 500 seconds (0-500) with total 26 frames created & processed (1 per 15 seconds)
* Url6's duration = 500 seconds (0-500) with total 78 frames created & processed (1 per 5 seconds)

![Screenshot from 2022-02-04 10-38-27](https://user-images.githubusercontent.com/57920951/152516475-9b542414-3b81-4221-be99-28e5888d5744.png)

### Average results from version1 vs version2 vs version3 vs version4 with 1 input with single node (davinci)
* Url6's duration = 500 seconds (0-500) with total 78 frames created & processed (1 per 5 seconds)

 ![78frames_execution](https://user-images.githubusercontent.com/57920951/152551732-63426362-a7df-46bd-8f42-eb00fe53c3d7.png)
 
### Average results from version1. Single and Multi-node deployment, 3 replicas for facedetector-faceanalyzer-mobilenet
* Url1's duration = 180 seconds (0-180) with total 11  frames created & processed (1 per 15 seconds)
* Url4's duration = 280 seconds (0-280) with total 18  frames created & processed (1 per 15 seconds)
* Url5's duration = 500 seconds (0-500) with total 26  frames created & processed (1 per 15 seconds)
* Url6's duration = 500 seconds (0-500) with total 78  frames created & processed (1 per 5 seconds)
* Url7's duration = 654 seconds (0-654) with total 130 frames created & processed (1 per 5 seconds)

![single_multi2](https://user-images.githubusercontent.com/57920951/152982651-d522ac39-8d8e-4c61-9a32-cc74b095681b.png)

### Average results from version1 (single/multi-node) vs version4


![version1-4-single-multi](https://user-images.githubusercontent.com/57920951/153644735-bdc69f30-88f3-4ba1-895e-eb1e7c49aebb.png)

### Timestamps experiment for Version1(3 replicas) single-node VS Version1(3 replicas) multi-node deployments

![Screenshot from 2022-02-11 19-24-07](https://user-images.githubusercontent.com/57920951/153639554-15e0b71f-d2f9-4675-8445-173caa9e36c9.png)


![timestamps_experiment](https://user-images.githubusercontent.com/57920951/153643250-ea74508f-3049-48b1-a51d-addd0be4791f.png)

### Average results for Version1(1, 3 replicas) for single-node deployment: Davinci VS Liono

![Screenshot from 2022-02-14 12-41-20](https://user-images.githubusercontent.com/57920951/153849266-85194275-68a4-4ccd-bfb9-923df6a0fb2b.png)

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
