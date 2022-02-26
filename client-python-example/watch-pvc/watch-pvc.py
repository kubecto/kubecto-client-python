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
    # 设置最大阀值
    max_claims = unit.Quantity("150Gi")
    total_claims = unit.Quantity("0Gi")

    # 配置 client 
    config.load_kube_config()

    # https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md
    # 包中 Swagger 生成的类型client包括版本化 API 对象类和序列化器类，它们提供对 API 操作的访问
    api = client.CoreV1Api()

    # 打印 PVC list
    # 在swagger当中提取list_namespaced_persistent_volume_claim拿到pvc的列表
    pvcs = api.list_namespaced_persistent_volume_claim(namespace=ns, watch=False)
    print("")
    print("---- 监视PVC的变化 ---")
    
    # 打印表格类型
    print("%-30s\t%-20s\t%-40s\t%-6s" % ("Storageclass", "Name", "Volume", "Size"))
    for pvc in pvcs.items:
    
    # 取出list过后的值放入对应的表格中
        print("%-16s\t%-16s\t%-40s\t%-6s" %
    # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1PersistentVolumeClaimSpec.md
    # 还是按照之前将的python-client包的内容去拿对应的值
              (pvc.spec.storage_class_name, pvc.metadata.name, pvc.spec.volume_name, pvc.spec.resources.requests['storage']))
    print("")


    # 配置 watch,创建watch 对象，然后，循环通过方法返回的事件流watch.stream
    # 我们必须为timout_seconds流设置超时值 ,通过将其设置为0，它会强制 HTTP 客户端与服务器保持长时间运行的连接，从而避免在程序接收到任何事件之前超时。
    w = watch.Watch()
    for item in w.stream(api.list_namespaced_persistent_volume_claim, namespace=ns, timeout_seconds=0):
        pvc = item['object']
        

        # 解析 PVC 事件
        # 新的 PVC 添加
        # 在循环内部，我们设置 if 语句来检查从服务器检索到的每个监视项。如果事件类型为“ADDED”，则表示已创建新的 PVC
        if item['type'] == 'ADDED':
            size = pvc.spec.resources.requests['storage']
            claimQty = unit.Quantity(size)
            total_claims = total_claims + claimQty

            print("PVC 添加新的volume: %s; size %s" % (pvc.metadata.name, size))

        # 如果该总数大于阈值数量，max_claims则打印屏幕通知操作。
            if total_claims >= max_claims:
                print("\033[0;31m---------------------------------------------")
                print("WARNING: claim 达到负载; 预设最大值 %s; 当前值 %s" % (max_claims, total_claims))
                print("---------------------------------------------\033[0m")
        
        # PVC 删除
        # 当 PVC 被删除时，它应用相反的逻辑并减少运行的总claims。
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
