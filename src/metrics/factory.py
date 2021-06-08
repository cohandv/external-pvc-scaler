import configparser

from config import ConfigSections, ConfigGeneral, ConfigPrometheus
from metrics.prometheus import Prometheus


class MetricsFactory:

    @staticmethod
    def create_instance(parser: configparser):
        """
        Tries to instantiate the
        :param parser: A parsed configuration
        :return: A running instance
        """
        metric_type = parser[ConfigSections.general.name][ConfigGeneral.metric_type.name]
        if metric_type.lower() == "prometheus":
            return Prometheus(url=parser[ConfigSections.prometheus.name][ConfigPrometheus.url.name],
                              query=parser[ConfigSections.prometheus.name][ConfigPrometheus.query.name],
                              entity=parser[ConfigSections.prometheus.name][ConfigPrometheus.entity.name])
        else:
            raise NotImplemented



