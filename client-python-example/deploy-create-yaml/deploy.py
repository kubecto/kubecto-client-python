#!/usr/local/bin/python3.8
from os import path

import yaml

from kubernetes import client, config


def main():
    config.load_kube_config()
#读取当前目录下的nginx-deployment.yaml，并创建
    with open(path.join(path.dirname(__file__), "nginx-deployment.yaml")) as f:
        dep = yaml.safe_load(f)
        k8s_apps_v1 = client.AppsV1Api()
        resp = k8s_apps_v1.create_namespaced_deployment(
            body=dep, namespace="default")
        print("Deployment created. status='%s'" % resp.metadata.name)


if __name__ == '__main__':
    main()
