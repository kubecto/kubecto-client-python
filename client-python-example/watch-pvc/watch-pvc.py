#!/usr/local/bin/python3.8
import os
import pint
from kubernetes import client, config, watch


def main():
    # 配置namespace
    ns = os.getenv("K8S_NAMESPACE")
    if ns is None:
        ns = ""

    # 使用 package pint 处理 volume 数量
    unit = pint.UnitRegistry()
    unit.define('gibi = 2**30 = Gi')
    max_claims = unit.Quantity("150Gi")
    total_claims = unit.Quantity("0Gi")

    # 配置 client 
    config.load_kube_config()
    api = client.CoreV1Api()

    # 打印 PVC list
    pvcs = api.list_namespaced_persistent_volume_claim(namespace=ns, watch=False)
    print("")
    print("---- PVCs ---")
    print("%-16s\t%-40s\t%-6s" % ("Name", "Volume", "Size"))
    for pvc in pvcs.items:
        print("%-16s\t%-40s\t%-6s" %
              (pvc.metadata.name, pvc.spec.volume_name, pvc.spec.resources.requests['storage']))
    print("")


    # 配置 watch
    w = watch.Watch()
    for item in w.stream(api.list_namespaced_persistent_volume_claim, namespace=ns, timeout_seconds=0):
        pvc = item['object']
        

        # 解析 PVC 事件
        # 新的 PVC 添加
        if item['type'] == 'ADDED':
            size = pvc.spec.resources.requests['storage']
            claimQty = unit.Quantity(size)
            total_claims = total_claims + claimQty

            print("PVC 添加新的volume: %s; size %s" % (pvc.metadata.name, size))

            if total_claims >= max_claims:
                print("\033[0;31m---------------------------------------------")
                print("WARNING: claim 达到负载; 预设最大值 %s; 当前值 %s" % (max_claims, total_claims))
                print("---------------------------------------------\033[0m")
        
        # PVC 删除
        if item['type'] == 'DELETED':
            size = pvc.spec.resources.requests['storage']
            claimQty = unit.Quantity(size)
            total_claims = total_claims - claimQty

            print("PVC 删除volume: %s; size %s" % (pvc.metadata.name, size))

            if total_claims <= max_claims:
                print("---------------------------------------------")
                print("INFO: claim 使用正常; max %s; at %s" % (max_claims, total_claims))
                print("---------------------------------------------")

        
        # PVC 更新
        if item['type'] == "MODIFIED":
            print("MODIFIED: %s" % (pvc.metadata.name))
        print("\033[0;36m++++++++++++++++++++++++++++++++++++++")
        print("INFO: 本地 PVC 当前容量百分比 %4.1f%% " % ((total_claims/max_claims)*100))
        print("++++++++++++++++++++++++++++++++++++++\033[0m")

if __name__ == '__main__':
    main()
