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

"""
openci_publish command-line client

Usage: openci_publish [options]

Options:
  -h, --help                Show this help message and exit
  -H <host>, --host=<host>  Hostname or IP address to connect to. [default: localhost]
  -P <port>, --port=<port>  Port providing stomp protocol connections. [default: 61613]
  -U <user>, --user=<user>  Username for the connection
  -p <password>, --password=<password>
                            Password for the connection
  -t <type>, --type=<type>  Set the subscription type (topic or queue). [default: topic]
  -n <name>, --name=<subscription_name>
                            Name of topic or queue where to subscribe.
  -S <protocol_version>, --protocol=<protocol_version>
                            Set the STOMP protocol version. [default: 1.1]
  -ssl                      Enable SSL connection
  -b, --body=<event_body>   JSON blob with the message body to publish
  -c <config_file>, --config_file=<config_file>
                            Accepts the path for a config file, that will
                            contain all the connection options
"""

import os.path
import stomp
import sys
import time

from ConfigParser import SafeConfigParser
from docopt import docopt
from openci_publish import publisher

__version__ = (1, 0, 0)
version_string = '%s.%s.%s' % __version__
MANDATORY_CONFIG_ARGUMENTS = [ 'host', 'user', 'password' ]

def main():
    arguments = docopt(__doc__, version=version_string)

    if '--config_file' in arguments:
        # read all the connection arguments from there
        if not os.path.isfile(arguments['--config_file']):
            print("Cannot find the config file '%s'" %
                  arguments["--config_file"])
            sys.exit(1)

        try:
            parser = SafeConfigParser()
            parser.read(arguments['--config_file'])
            for argument in MANDATORY_CONFIG_ARGUMENTS:
                if not parser.has_option('default', argument):
                    print("Missing setting '%s' on config file" % argument)
                    sys.exit(1)

        except Exception as e:
            print(str(e))

    if arguments['--type'] not in ('topic', 'queue'):
        print("Subscription type can only be 'topic' or 'queue'.")
        sys.exit(1)

    if arguments['--name'] is None:
        print("Please specify the subscription name to connect.")
        sys.exit(1)

    use_ssl = ('--ssl' in arguments)

    publisher.send_message(arguments['--host'], arguments['--port'],
                           arguments['--user'], arguments['--password'],
                           arguments['--protocol'], use_ssl,
                           arguments['--body'],
                           arguments['--type'],
                           arguments['--name'])

if __name__ == '__main__':
    try:
        main()
    except:
        pass