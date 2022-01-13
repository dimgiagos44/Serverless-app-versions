# Serverless-app-versions

Main repository for Master thesis on serverless.

## Description
* In [functions](https://github.com/dimgiagos44/Serverless-app-versions/tree/main/functions) there exist 4 versions of the same ML Workflow
* Each version consists of functions of different granularity
* Version1 is the most fine-grained, while Version4 is the most coarse-grained of the versions
* After deploying all the functions, by using the [exec script](https://github.com/dimgiagos44/Serverless-app-versions/blob/main/exec.sh)
we can run the desired instance on our local cluster as many times as we like in a sequential way of invocations
```
./exec.sh version1 url1 10 yes yes
```
* We can scale each function's replicas up or down so as to make the versions capable
of serving more or less requests per minute
```
kubectl scale deployment version1 -n openfaas-fn --replicas=2
```


## Example Usage

![Screenshot from 2022-01-13 13-34-28](https://user-images.githubusercontent.com/57920951/149323209-26a6a7c0-8307-4b88-a4ca-72b80605a9ba.png)

![Screenshot from 2022-01-13 13-34-49](https://user-images.githubusercontent.com/57920951/149323217-9d14f329-8435-4fea-bbd9-1f9768a1e408.png)
