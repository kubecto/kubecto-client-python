#!/usr/local/bin/python3.8
from kubernetes import client, config

#https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1PodStatus.md
#具体可以安装对应的表结构获取自己想要的功能

def main():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s\t%s\t%s" %
              (i.status.host_ip, i.status.pod_ip, i.status.phase, i.metadata.namespace, i.metadata.name))


if __name__ == '__main__':
    main()
