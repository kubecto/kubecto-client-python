#!/usr/local/bin/python3.8
import datetime

import pytz

from kubernetes import client, config

DEPLOYMENT_NAME = "kubecto-nginx-deployment"


def create_deployment_object():
    # 配置Pod模板容器
    container = client.V1Container(
        name="nginx",
        image="nginx:1.15.1",
        ports=[client.V1ContainerPort(container_port=80)],
        resources=client.V1ResourceRequirements(
            requests={"cpu": "100m", "memory": "200Mi"},
            limits={"cpu": "500m", "memory": "500Mi"},
        ),
    )

    # 创建并配置规范部分
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
        spec=client.V1PodSpec(containers=[container]),
    )

    # 创建部署规范
    spec = client.V1DeploymentSpec(
        replicas=3, template=template, selector={
            "matchLabels":
            {"app": "nginx"}})

    # 实例化部署对象
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec,
    )

    return deployment


def create_deployment(api, deployment):
    # 创建 deployement
    resp = api.create_namespaced_deployment(
        body=deployment, namespace="default"
    )

    print("\n[INFO] deployment `kubecto-nginx-deployment` created.\n")
    print("%s\t%s\t\t\t%s\t%s" % ("NAMESPACE", "NAME", "REVISION", "IMAGE"))
    print(
        "%s\t\t%s\t%s\t\t%s\n"
        % (
            resp.metadata.namespace,
            resp.metadata.name,
            resp.metadata.generation,
            resp.spec.template.spec.containers[0].image,
        )
    )

def main():
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()

    deployment = create_deployment_object()

    create_deployment(apps_v1, deployment)

if __name__ == "__main__":
    main()
