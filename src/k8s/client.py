import re
import logging
from kubernetes import client, config

from kubernetes.client import V1PersistentVolumeClaimList, V1PersistentVolumeClaim


class Client:
    def __init__(self, in_cluster: bool, dry_run: bool):
        if in_cluster:
            config.load_incluster_config()
        else:
            config.load_kube_config()  # not sure we need to do this on a pod
        self.client = client.CoreV1Api()
        self.dry_run = dry_run

    def update_pvc(self, pvc_name, increase_amount):

        pvcs = self.client.list_persistent_volume_claim_for_all_namespaces()
        for pvc in pvcs.items:
            if pvc.metadata.name == pvc_name:
                try:
                    parsed_current_storage = re.search("(\\d+)(.*)", pvc.spec.resources.requests['storage'], re.IGNORECASE).groups()
                    new_space = f"{round(int(parsed_current_storage[0])*(1+increase_amount))}{parsed_current_storage[1]}"

                    body = {
                        "spec": {
                            "resources": {
                                "requests": {
                                    "storage": new_space
                                }
                            }
                        }
                    }

                    if self.dry_run:
                        self.client.patch_namespaced_persistent_volume_claim(name=pvc.metadata.name,
                                                                             namespace=pvc.metadata.namespace,
                                                                             body=body,
                                                                             dry_run="All")
                    else:
                        self.client.patch_namespaced_persistent_volume_claim(name=pvc.metadata.name,
                                                                             namespace=pvc.metadata.namespace,
                                                                             body=body)
                    logging.info(f"We have increased PVC {pvc_name} by {increase_amount}, resulting in {new_space}")
                except Exception as ex:
                    logging.error(ex)
