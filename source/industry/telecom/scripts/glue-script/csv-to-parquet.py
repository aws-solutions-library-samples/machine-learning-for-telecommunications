import sys

import boto3
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv,
                          ['JOB_NAME', 'region', 'database', 'outputPath'])

glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
database = args['database']
region = args['region']
glue_endpoint_url = "https://glue.{}.amazonaws.com".format(region)
glue = boto3.client(service_name='glue', region_name=region,
                    endpoint_url=glue_endpoint_url)

try:
    catalog_id = boto3.client('sts').get_caller_identity()['Account']
    response = glue.get_tables(
        CatalogId=catalog_id,
        DatabaseName=database,
    )

    for table in response['TableList']:
        outputPath = args['outputPath'] + "/{}".format(table['Name'])

        source_table = glue.get_table(Name=table['Name'], DatabaseName=database)
        source_s3_location = source_table['Table']['StorageDescriptor']['Location']
        source_s3_columns = source_table['Table']['StorageDescriptor']['Columns']

        columns = [d['Name'] for d in source_s3_columns if 'Name' in d]
        df = spark.read.option("header", "false").csv(source_s3_location)
        df.printSchema()
        df.repartition(100).write.parquet(outputPath, mode="append")

except Exception as e:
    print('An error occurred: {}.'.format(e))
    raise e

job.commit()
