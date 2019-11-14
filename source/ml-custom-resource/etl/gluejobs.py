#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################################################################################################
#  Copyright 2018-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                      #
#                                                                                                                    #
#  Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance    #
#  with the License. A copy of the License is located at                                                             #
#                                                                                                                    #
#      http://www.apache.org/licenses/LICENSE-2.0                                                                    #
#                                                                                                                    #
#  or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES #
#  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    #
#  and limitations under the License.                                                                                #
######################################################################################################################

import boto3
import os
import logging
import time
from custom.custom_base import Custom

log = logging.getLogger()
log.setLevel(logging.INFO)


class GlueJobs(Custom):
    def __init__(self, event, context, job_name, database=None, data_location=None, bucket=None, s3_prefix_artifacts=None, output_path=None):
        super().__init__(event, context,bucket,s3_prefix_artifacts)
        self.glue_client = boto3.client('glue')
        self.kms = boto3.client('kms')
        self.s3 = boto3.client('s3')
        self.invoke_gluejob = self.event["ResourceProperties"]["InvokeGlueJob"]
        self.region = os.environ['AWS_DEFAULT_REGION']
        self.account_id = os.environ['AWS_ACCOUNT_ID']
        self.job_name = job_name
        self.data_location = data_location
        self.bucket = bucket
        self.s3_prefix_artifacts = s3_prefix_artifacts
        self.database = database
        self.output_path = output_path

    def __call__(self):
        self.put_data_catalog_encryption()
        self.create_table(self.database, self.bucket, self.data_location)
        if self.invoke_gluejob == "true":
            self.start_job()
            return {'PhysicalResourceId': self.event["LogicalResourceId"]}

    def __delete__(self):
        self.delete_job()

    def create_table(self,database,bucket,data_location,classification='csv'):

        try:
            catalog_id = self.account_id
            artifacts = super().get_artifactJson()

            schema_file = artifacts['artifacts']['schema']['custom-schema']
            custom_schema = self.get_columns(schema_file)

            for table_name, value in artifacts['artifacts']['files'].items():
                location = "s3://{}/{}/{}/".format(bucket,data_location,table_name)

                columns = custom_schema['schema'][table_name]['columns']
                response = self.glue_client.create_table(
                    CatalogId=catalog_id,
                    DatabaseName=database,
                    TableInput={
                        'Name': table_name,
                        'StorageDescriptor': {
                            'Columns': columns,
                            'Location': location,
                            'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                            'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                            'Compressed': True,
                            'SerdeInfo': {
                                'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
                                'Parameters': {
                                    'field.delim': ','
                                }
                            }
                        },
                        'TableType': 'EXTERNAL_TABLE',
                        'Parameters': {
                            'classification': classification
                        }
                    }
                )
        except Exception as e:
            print('An error occurred: {}.'.format(e))
            raise e

        return response

    def put_data_catalog_encryption(self):
        try:
            catalog_id = self.account_id
            response = self.glue_client.put_data_catalog_encryption_settings(
                CatalogId=catalog_id,
                DataCatalogEncryptionSettings={
                    'EncryptionAtRest': {
                        'CatalogEncryptionMode': 'SSE-KMS'
                    }
                }
            )
            return response

        except Exception as e:
            print('An error occurred: {}.'.format(e))
            raise e

    def get_columns(self,schema_file):
        try:
            key = "{}/schema/{}".format(self.s3_prefix_artifacts, schema_file)
            schema_json = super().read_json(self.bucket, key)
            return schema_json

        except Exception as e:
            print('An error occurred: {}.'.format(e))
            raise e

    def start_job(self):
        print('File Transformation started on {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        try:

            # Start Glue job
            response = self.glue_client.start_job_run(
                JobName=self.job_name,
                Arguments={
                    '--region': self.region,
                    '--database': self.database,
                    '--outputPath': self.output_path
                }
            )

            print('Glue ETL job {} started on {}'.format(response['JobRunId'],
                                                         time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

            print('File Transformation completed on {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
        except Exception as e:
            print('An error occurred: {}.'.format(e))
            raise e

        return response

    def delete_job(self):
        try:
            # Delete Glue job
            response = self.glue_client.delete_job(
                JobName=self.job_name
            )
            log.info('Response = %s', response)
        except Exception as e:
            print('No Job to Delete or An error occurred: {}.'.format(e))
