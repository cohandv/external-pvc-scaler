# External pvc scaler

This app is a simple process that relies on Kubernetes CSI Driver and Prometheus to automatically scale up Persistent Volume Claims.

# Usage

* Install this pod a a single instance in `kube-system` (recommended) using this template. if you want to override this, attach the config as volume at /app/config.ini

# Configuration
This is all the settings that support this tool
```ini
[general]
metric_type=prometheus
wait_timeout_in_seconds=1
threshold=60
operator=<
increase_multiplier=0.15

[kubernetes]
in_cluster=yes
dry_run=no

[log]
level=INFO

[prometheus]
url=http://prometheus:9090
query=max by (persistentvolumeclaim) (kubelet_volume_stats_available_bytes)*100/max by (persistentvolumeclaim) (kubelet_volume_stats_capacity_bytes)
entity=persistentvolumeclaim
```
* This file can be mounted in `/app/config.ini` otherwise will take the default values in the `default.ini` file
* The only entity supported now is a PVC 

### Query DOES NOT GO WITH QUOTES! and consider that it travels on the query string, so store it with the appropiate format
