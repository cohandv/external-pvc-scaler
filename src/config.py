from enum import Enum


class ConfigSections(Enum):
    general = 1
    prometheus = 2
    log = 3
    kubernetes = 4


class ConfigGeneral(Enum):
    metric_type = 1
    wait_timeout_in_seconds = 2
    threshold = 3
    operator = 4
    increase_multiplier = 5


class ConfigKubernetes(Enum):
    in_cluster = 1
    dry_run = 2


class ConfigLog(Enum):
    level = 1


class ConfigPrometheus(Enum):
    url = 1
    query = 2
    entity = 3
