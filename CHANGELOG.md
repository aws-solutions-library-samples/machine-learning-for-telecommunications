# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2019-11-01
### Added
- CHANGELOG file
- local Solution Helper python code (for CreateUniqueID, SendAnonymousData)
  and updated CloudFormation template to use it.

### Changed
- license to Apache License, Version 2.0
- NOTICE file to include list of third party components used.
- README.md file with editorial changes, improvements in getting
  started section and instructions for copying synthetic
  dataset.
- build S3 distribution script and CloudFormation template for better
  organization of global/regional assets for deployment.
- CloudFormation template for S3 custom resource bucket name.
- dependency on boto3 and botocore to latest version for python requirements.
- CloudFormation template Lambda resource from python 3.6 to python 3.7
- CloudFormation template Glue Job resource Glue version to 1.0 (Spark 2.4,
  Python 3) from Glue version 0.9 (Spark 2.2, Python 2)

### Fixed
- Typo in CloudFormation template for SendAnonymousData
- Jupyter Notebook for Ml-Telecom-TimeSeries-RandomForestClassifier-DeepAR
  for (a) formatting of date and time in dataset and (b) noting the need
  for conforming data values when setting time series frequency to 1 minute.
