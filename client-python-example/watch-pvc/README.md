### 基础环境
自动pv供给 openebs安装,用于redis的pvc的实现

```
[root@kubecto client-python]# kubectl apply -f https://openebs.github.io/charts/openebs-operator.yaml
[root@kubecto client-python]# kubectl get po -n openebs
NAME                                            READY   STATUS    RESTARTS   AGE
openebs-localpv-provisioner-7fc6f78968-ztqd9    1/1     Running   0          3h27m
openebs-ndm-cluster-exporter-5c5ddddc89-5c7rc   1/1     Running   0          3h27m
openebs-ndm-node-exporter-cvpdj                 1/1     Running   0          3h27m
openebs-ndm-operator-56877788bf-grwld           1/1     Running   0          3h27m
openebs-ndm-vks2m                               1/1     Running   0          3h27m
```


### 安装redis charts

将包放入到本地服务器中

这里使用openebs中的openebs-hostpath存储类，其中在value.yaml已修改好，可直接使用

确保都绑定成功

```
cd redis
helm install redis ../redis

[root@kubecto client-python]# kubectl get pvc
NAME                        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS       AGE
redis-data-redis-master-0   Bound    pvc-0f0a57e2-f787-43f1-8257-ae4c0d5a2ff2   75Gi       RWO            openebs-hostpath   71m
redis-data-redis-slave-0    Bound    pvc-6e6a164d-588b-488a-85f2-b3a55d7c6546   75Gi       RWO            openebs-hostpath   71m
redis-data-redis-slave-1    Bound    pvc-cd0750d5-f7fc-446b-8f81-aaccdb5c9197   75Gi       RWO            openebs-hostpath   70m
```

### 运行程序监视pvc的预警值


<img width="686" alt="QQ20220226-021337@2x" src="https://user-images.githubusercontent.com/94602819/155766550-d3f88e87-123a-457f-95fb-3b4dfa59122a.png">

