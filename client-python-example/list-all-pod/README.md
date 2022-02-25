
#### 基础环境准备

Linux环境 kubernetes环境

##### linux 下python 环境安装

```
yum -y install zlib-devel
wget https://www.python.org/ftp/python/3.8.6/Python-3.8.6.tgz

tar xf Python-3.8.6.tgz
cd Python-3.8.6
./configure
make -j 4 && make install
```

#### 安装python插件kubernetes
```

[root@kubecto ~]# pip3 install kubernetes

[root@kubecto ~]# pip3 list
Package            Version
------------------ ---------
cachetools         5.0.0
certifi            2021.10.8
charset-normalizer 2.0.12
google-auth        2.6.0
idna               3.3
kubernetes         22.6.0
oauthlib           3.2.0
pip                22.0.3
pyasn1             0.4.8
pyasn1-modules     0.2.8
python-dateutil    2.8.2
PyYAML             6.0
requests           2.27.1
requests-oauthlib  1.3.1
rsa                4.8
setuptools         49.2.1
six                1.16.0
urllib3            1.26.8
websocket-client   1.2.3

```

#### 执行权限
```
chmod +x list-all-pod.py

```

#### 运行代码

```
[root@kubecto list-all-pod]# python3.8 list-all-pod.py
Listing pods with their IPs:
172.90.90.195	calico-system	calico-kube-controllers-84cff75796-9xzz2
10.0.12.3	calico-system	calico-node-nsjdq
10.0.12.3	calico-system	calico-typha-7779d6cdd-2dtvf
172.90.90.196	default	nginx-84b9b46f96-qbh8z
172.90.90.193	kube-system	coredns-545d6fc579-8kdcl
172.90.90.194	kube-system	coredns-545d6fc579-vnxdt
10.0.12.3	kube-system	etcd-kubecto
10.0.12.3	kube-system	kube-apiserver-kubecto
10.0.12.3	kube-system	kube-controller-manager-kubecto
10.0.12.3	kube-system	kube-proxy-9mgzn
10.0.12.3	kube-system	kube-scheduler-kubecto
10.0.12.3	tigera-operator	tigera-operator-6944b4cb45-lnbrz
```

