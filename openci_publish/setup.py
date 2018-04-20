# Copyright 2018 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

setup(
    name='openci_publish',
    version='1.0.0',
    description='OpenCI utility to send message to message brokers using STOMP',
    license='Apache',
    url='https://gitlab.openci.io/openci/prototypes',
    author='Yolanda Robla',
    author_email='yroblamo@redhat.com',
    platforms=['any'],
    install_requires = ['docopt>=0.6.2', 'stomp.py>=4.1.19'],
    packages=['openci_publish'],
    entry_points={
        'console_scripts': [
            'openci_publish = openci_publish.__main__:main',
        ],
    },
    classifiers=[
         'Development Status :: 5 - Production/Stable',
         'Intended Audience :: Developers',
         'License :: OSI Approved :: Apache Software License',
         'Programming Language :: Python :: 2',
         'Programming Language :: Python :: 3'
    ]
)
