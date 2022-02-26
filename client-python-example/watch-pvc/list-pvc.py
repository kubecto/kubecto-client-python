#!/usr/local/bin/python3.8
import os

from kubernetes import client, config, watch

def main():    
    ns = os.getenv("K8S_NAMESPACE")
    if ns is None:
        ns = ""
    
    # 加载本地的.kube/config
    config.load_kube_config()
    
    # https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md
    # 包中 Swagger 生成的类型client包括版本化 API 对象类和序列化器类，它们提供对 API 操作的访问
    api = client.CoreV1Api()
    pvcs = api.list_namespaced_persistent_volume_claim(
      namespace=ns)

    print("")
    print("---- 监听PVC的变化 ---")
    #  取出list过后的值放入对应的表格中
    print("%-30s\t%-20s\t%-40s\t%-6s" % ("StorageClass", "Name", "Volume", "Size"))
    for pvc in pvcs.items:
        print("%-16s\t%-16s\t%-40s\t%-6s" %
    # 取出list过后的值放入对应的表格中
              (pvc.spec.storage_class_name, pvc.metadata.name, pvc.spec.volume_name, pvc.spec.resources.requests['storage']))
    print("")

    # 持续Watch pvc的变化
    # 配置 watch,创建watch 对象，然后，循环通过方法返回的事件流watch.stream
    # 我们必须为timout_seconds流设置超时值 ,通过将其设置为0，它会强制 HTTP 客户端与服务器保持长时间运行的连接，从而避免在程序接收到任何事件之前超时。
    w = watch.Watch()
    for item in w.stream(api.list_namespaced_persistent_volume_claim, namespace=ns, timeout_seconds=0):
        pvc = item['object']


if __name__ == '__main__':
    main()
