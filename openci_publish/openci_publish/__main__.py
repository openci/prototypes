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
  -s <subscription_type>, --subscription_type=<subscription_type>
                            Type of subscription, can be topic or queue.
                            [default='topic']
  -n <subscription_name>, --subscription_name=<subscription_name>
                            Name of topic or queue where to subscribe.
  -S <protocol_version>, --protocol=<protocol_version>
                            Set the STOMP protocol version. [default: 1.1]
  -ssl                      Enable SSL connection
  -b, --body=<event_body>   JSON blob with the message body to publish
"""

import stomp
import sys
import time

from docopt import docopt
from openci_publish import publisher

__version__ = (1, 0, 0)
version_string = '%s.%s.%s' % __version__

def main():
    arguments = docopt(__doc__, version=version_string)

    if arguments['--subscription_type'] not in ('topic', 'queue'):
        print("Subscription type can only be 'topic' or 'queue'.")
        sys.exit(1)

    if arguments['--subscription_name'] is None:
        print("Please specify the subscription name to connect.")
        sys.exit(1)

    use_ssl = ('--ssl' in arguments)

    publisher.send_message(arguments['--host'], arguments['--port'],
                           arguments['--user'], arguments['--password'],
                           arguments['--protocol'], use_ssl,
                           arguments['--body'],
                           arguments['--subscription_type'],
                           arguments['--subscription_name'])

if __name__ == '__main__':
    try:
        main()
    except:
        pass
