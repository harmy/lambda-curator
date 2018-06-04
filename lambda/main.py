# coding=utf-8
from __future__ import print_function
import os
import re
import logging
import boto3
import curator

from curator.exceptions import NoIndices
from elasticsearch import Elasticsearch, RequestsHttpConnection
from aws_requests_auth.aws_auth import AWSRequestsAuth

logger = logging.getLogger()
logger.setLevel(logging.INFO)

UNIT_CONFIG = {
    'y': 8760,
    'm': 720,
    'w': 168,
    'd': 24,
    'h': 1
}


def find_actionable_domains():
    domains = []
    enabled_regions = set(boto3.session.Session().get_available_regions('es'))
    if os.environ.get('REGIONS'):
        enabled_regions &= set([x for x in re.split(',| ', os.environ.get('REGIONS')) if x != ''])

    for region in enabled_regions:
        es = boto3.client('es', region)
        for domain in es.list_domain_names()['DomainNames']:
            tags = []
            domain_info = es.describe_elasticsearch_domain(DomainName=domain['DomainName'])
            endpoint = domain_info['DomainStatus']['Endpoint']
            tags_info = es.list_tags(ARN=domain_info['DomainStatus']['ARN'])

            for tag in tags_info['TagList']:
                if re.match(r'\d+[y|m|w|d|h]', tag['Value']):
                    tags.append(tag)

            if tags:
                domains.append((region, endpoint, tags))

    return domains


def lambda_handler(event, context):
    actionable_domains = find_actionable_domains()

    deleted_indices = {}
    for region, endpoint, tags in actionable_domains:
        auth = AWSRequestsAuth(aws_access_key=os.environ.get('AWS_ACCESS_KEY_ID'),
                               aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                               aws_token=os.environ.get('AWS_SESSION_TOKEN'),
                               aws_host=endpoint,
                               aws_region=region,
                               aws_service='es')
        es = Elasticsearch(host=endpoint, port=80, connection_class=RequestsHttpConnection, http_auth=auth)

        deleted_indices[endpoint] = []

        curator_config = {}
        curator_default = ''

        for tag in tags:
            prefix = tag['Key']
            retention_period = tag['Value']
            if 'curator.default' in tag['Key']:
                curator_default = tag['Value']
                continue

            if not prefix.endswith('-'):
                prefix += '-'
            curator_config[prefix] = retention_period

        if curator_default != '':
            for index in es.indices.get('*'):
                if any([index.startswith(tag['Key']) for tag in tags]):
                    continue
                matched = re.match(r'(.*)-(\d{4}([-/.]w?\d{2}){,3})$', index)
                if not matched:
                    continue

                prefix, _ = matched.groups()
                if not prefix.endswith('-'):
                    prefix += '-'
                if prefix not in curator_config:
                    curator_config[prefix] = curator_default

        logger.info(curator_config)

        for prefix, retention_period in curator_config.items():
            index_list = curator.IndexList(es)
            matched = re.match(r'(\d+)([y|m|w|d|h])', retention_period)
            if not matched:
                continue
            p1, p2 = matched.groups()
            unit_count = int(p1) * UNIT_CONFIG[p2]
            try:
                index_list.filter_by_regex(kind='prefix', value=prefix)
                index_list.filter_by_age(source='creation_date', direction='older', unit='hours', unit_count=unit_count)
                curator.DeleteIndices(index_list).do_action()
                deleted_indices[endpoint].extend(index_list.working_list())
            except NoIndices:
                pass

    lambda_response = {'deleted': deleted_indices}
    logger.info(lambda_response)
    return lambda_response


if __name__ == '__main__':
    lambda_handler({}, {})
