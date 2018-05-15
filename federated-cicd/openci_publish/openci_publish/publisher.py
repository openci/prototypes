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

# sends a message to the message broker provider. It relies on STOMP protocol
import json
import stomp
import sys

class OpenCIListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, headers, message):
        pass

    def on_message(self, headers, message):
        print("on message")
        print(headers)
        print(message)
        pass

    def on_disconnected(self):
        connect_and_subscribe(self.conn)

MANDATORY_FIELDS = [ 'type', 'id', 'time', 'buildUrl', 'branch' ]
TYPES_SCHEMA = {
    'ArtifactPublishedEvent': [ 'artifactLocation', 'confidenceLevel' ],
    'CompositionDefinedEvent': [ 'compositionName', 'compositionMetadataUrl' ],
    'ConfidenceLevelModifiedEvent': [ 'compositionName',
                                      'compositionMetadataUrl',
                                      'confidenceLevel' ]
}
# validates passed json
def validate_json_message(json_body):
    # first we validate type
    if 'type' not in json_body or json_body['type'] not in TYPES_SCHEMA.keys():
        return False, ('You must provide a valid type (%s)' %
                       ', '.join(TYPES_SCHEMA.keys()))

    # now validate that we have the mandatory fields depending on the type
    missing_fields = []
    for field in MANDATORY_FIELDS + TYPES_SCHEMA[json_body['type']]:
        if field not in json_body:
            missing_fields.append(field)

    if missing_fields:
        return False, "Missing mandatory field(s): %s" % (', '.
                                                          join(missing_fields))

    return True, ''

def send_message(host='localhost', port=61613, user='', password='', ver='1.1',
                 use_ssl=False,  body='', subscription_type='topic',
                 subscription_name=''):

    # before connecting, validate that the message is valid
    try:
        json_body = json.loads(body)
    except:
        print("Invalid body provided, needs to be a JSON file")
        sys.exit(1)

    result, error_message = validate_json_message(json_body)
    if not result:
        print("Validation error: %s" % error_message)
        sys.exit(1)

    try:
        # establish the right stomp connection
        if ver == '1.0':
            conn = stomp.Connection10([(host, port)])
        elif ver == '1.1':
            conn = stomp.Connection11([(host, port)])
        elif ver == '1.2':
            conn = stomp.Connection12([(host, port)])
        elif ver == 'multicast':
            conn = MulticastConnection()

        if use_ssl:
            conn.set_ssl([(host, port)])

        conn.set_listener('', OpenCIListener(conn))
        conn.start()

        # connect and send message
        conn.connect(user, password, wait=True)
        txid = conn.begin()
        conn.send(destination='/%s/%s' % (subscription_type, subscription_name),
                  body=body, headers={'JMSType': json_body['type']},
                  transaction=txid)
        conn.commit(txid)
        conn.disconnect()
    except Exception as e:
        print("There has been an error processing your message: %s" % str(e))
        sys.exit(1)
