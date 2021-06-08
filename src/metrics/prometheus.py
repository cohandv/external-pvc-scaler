import logging
import requests


class Prometheus(object):
    def __init__(self, url: str, query, entity) -> object:
        self.url = f'{url}/api/v1/query'
        self.query = query
        self.entity = entity

    def get_metrics(self):
        values = {}
        try:
            response = requests.get(self.url, params=f'query={self.query}')
            response.raise_for_status()
            body = response.json()
            if 'data' in body:
                for metric in body['data']['result']:
                    # Values [0] is the timestamp of that serie
                    values[metric['metric'][self.entity]] = metric['value'][1]
        except Exception as ex:
            logging.error(ex)
        finally:
            return values

