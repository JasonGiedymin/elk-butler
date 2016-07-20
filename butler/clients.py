#
# ES Client Tools
#

from elasticsearch import Elasticsearch
import os


def info():
    es_host = os.environ.get('ES_HOST', 'localhost')
    es_port = os.environ.get('ES_PORT', 9200)
    use_ssl = False
    return {'host': es_host, 'port': es_port, 'use_ssl': use_ssl}


def create():
    return Elasticsearch([
        info()
    ])
