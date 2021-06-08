import logging
import time

from config import ConfigSections, ConfigGeneral, ConfigLog, ConfigKubernetes
from k8s.client import Client
from metrics.factory import MetricsFactory
from utils import config_reader, parse_bool

if __name__ == '__main__':
    # Read configuration
    parser = config_reader()

    # Setup logging
    logging.basicConfig(level=logging.getLevelName(parser[ConfigSections.log.name][ConfigLog.level.name]))

    # Build the metric server
    metric_server = MetricsFactory.create_instance(parser)

    # Build the kubernetes client
    k8s_client = Client(in_cluster=parse_bool(parser[ConfigSections.kubernetes.name][ConfigKubernetes.in_cluster.name]),
                        dry_run=parse_bool(parser[ConfigSections.kubernetes.name][ConfigKubernetes.dry_run.name]))

    wait_time_in_seconds = int(parser[ConfigSections.general.name][ConfigGeneral.wait_timeout_in_seconds.name])
    threshold = int(parser[ConfigSections.general.name][ConfigGeneral.threshold.name])
    operator = parser[ConfigSections.general.name][ConfigGeneral.operator.name]
    increase_multiplier = float(parser[ConfigSections.general.name][ConfigGeneral.increase_multiplier.name])
    while True:
        entity_values = metric_server.get_metrics()
        for entity in entity_values.keys():
            if eval(f"{entity_values[entity]} {operator} {threshold}"):
                logging.info(f"The following entity {entity} has reached the threshold, we need to change the "
                             f"resource")
                k8s_client.update_pvc(entity, increase_multiplier)
            else:
                logging.info(
                    f"The following entity {entity} has not reached the threshold, ignoring the entity")
        time.sleep(wait_time_in_seconds)

