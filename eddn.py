import ast
import json
import zlib
import zmq
import simplejson
import sys
import time

"""
 "  Configuration
"""
__relayEDDN = 'tcp://eddn.edcd.io:9500'
__timeoutEDDN = 600000

"""
 "  Start
"""


def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)

    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    subscriber.setsockopt(zmq.RCVTIMEO, __timeoutEDDN)

    while True:
        try:
            subscriber.connect(__relayEDDN)

            while True:
                __message = subscriber.recv()

                if __message == False:
                    subscriber.disconnect(__relayEDDN)
                    break

                __message = zlib.decompress(__message)
                __dict = json.loads(__message.decode('utf-8'))

                # call dumps() to ensure double quotes in output
                yield __dict
                sys.stdout.flush()

        except zmq.ZMQError as e:
            print('ZMQSocketException: ' + str(e))
            sys.stdout.flush()
            subscriber.disconnect(__relayEDDN)
            time.sleep(5)


if __name__ == '__main__':
    main()