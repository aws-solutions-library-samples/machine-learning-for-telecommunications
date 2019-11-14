#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################################################################################################
#  Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                           #
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

from setuptools import setup, find_packages

setup(
    name='local_solution_helper',
    version='1.0.0',
    description='AWS Solution Helper Custom Resource',
    author='AWS Solutions Builder',
    license='Apache 2.0',
    zip_safe=False,
    packages=['local_solution_helper', 'pycfn_custom_resource'],
    package_dir={'local_solution_helper': '.', 'pycfn_custom_resource': './pycfn_custom_resource'},
    install_requires=[
        'requests>=2.22.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
)
