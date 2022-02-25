
## 运行代码

```
[root@kubecto create-deploy]# python3.8 python-deploy-create.py

[INFO] deployment `kubecto-nginx-deployment` created.

NAMESPACE	NAME			REVISION	IMAGE
default		kubecto-nginx-deployment	1		nginx:1.15.1

```

## 查看部署

```
Every 2.0s: kubectl get po -o wide                                                                             Fri Feb 25 20:52:34 2022

NAME                                        READY   STATUS    RESTARTS   AGE   IP              NODE      NOMINATED NODE   READINESS GAT
ES
busybox-test                                1/1     Running   0          61m   172.90.90.198   kubecto   <none>           <none>
kubecto-nginx-deployment-7754554bb9-2pqrx   1/1     Running   0          6m    172.90.90.229   kubecto   <none>           <none>
kubecto-nginx-deployment-7754554bb9-99lb2   1/1     Running   0          6m    172.90.90.228   kubecto   <none>           <none>
kubecto-nginx-deployment-7754554bb9-c2j6f   1/1     Running   0          6m    172.90.90.230   kubecto   <none>           <none>
```
