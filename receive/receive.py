from os import environ
from Crypto.Cipher import AES
import zmq

# cipher function with runtime injected KEY and Salt
cipher = AES.new(environ['TRANSFER_SECRET_KEY'], AES.MODE_CBC, environ['TRANSFER_IV456'])

# zero MQ as transport
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# end of invocation
EOI = bytes('STOP', 'ascii')

print('Waiting for files ...')
while True:

    # wait for a request
    message = socket.recv(copy=True)

    # all transfers complete
    if message == EOI:
        break

    # split the header and the contents
    payload = message.split(b'\n', maxsplit=1)

    # decode the header bytes to utf-8
    filename = payload[0].decode('utf-8')

    # decode and decrypt the contents
    contents = cipher.decrypt(payload[1]).decode('utf-8').lstrip()

    print("Received file: %s" % filename)

    # write to disk
    with open("/tmp/%s" % filename, 'w') as file_out:
        file_out.write(contents)
        file_out.close()

    # ack message
    socket.send(b'ack')

print("Transfers complete - shutting down")