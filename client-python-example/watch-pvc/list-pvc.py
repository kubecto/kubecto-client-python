#!/usr/local/bin/python3.8
import os

from kubernetes import client, config, watch

def main():    
    ns = os.getenv("K8S_NAMESPACE")
    if ns is None:
        ns = ""
    config.load_kube_config()
    api = client.CoreV1Api()
    pvcs = api.list_namespaced_persistent_volume_claim(
      namespace=ns, watch=False)

    print("")
    print("---- 监听PVC的变化 ---")
    print("%-30s\t%-40s\t%-6s" % ("Name", "Volume", "Size"))
    for pvc in pvcs.items:
        print("%-16s\t%-40s\t%-6s" %
              (pvc.metadata.name, pvc.spec.volume_name, pvc.spec.resources.requests['storage']))
    print("")

    # 持续Watch pvc的变化 
    w = watch.Watch()
    for item in w.stream(api.list_namespaced_persistent_volume_claim, namespace=ns, timeout_seconds=0):
        pvc = item['object']


if __name__ == '__main__':
    main()
