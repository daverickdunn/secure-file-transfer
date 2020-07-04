from os import environ
from Crypto.Cipher import AES
from json2xml import json2xml
import zmq
import json

# cipher function with runtime injected KEY and Salt
cipher = AES.new(environ['TRANSFER_SECRET_KEY'], AES.MODE_CBC, environ['TRANSFER_IV456'])

# zero MQ as transport
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://receiver:5555")

for in_filename in environ['FILENAMES'].split():

    print("Reading file: %s" % in_filename)

    with open("/tmp/%s" % in_filename, mode="r", encoding="utf-8") as file_in:

        # read file contents
        data = file_in.read()

        # parse json
        parsed = json.loads(data)

        # convert to xml
        xml = json2xml.Json2xml(parsed).to_xml()

        # calculate required buffer for blockchain
        padding = len(xml) + 16 - ( len(xml) % 16 )

        # pad string
        padded = xml.rjust(padding)

        # encrypt
        ciphertext = cipher.encrypt(padded)

        # change file extension
        out_filename = in_filename.replace(".json", ".xml")

        # prefix with a filename header using '\n' as delimiter
        message = b''.join([bytes(out_filename + '\n', 'utf-8'), ciphertext])

        print("Sending file: %s" % out_filename)

        # send message
        socket.send(message)

        # display reply
        reply = socket.recv()
        print("File sent!")

# end of transfers
socket.send(bytes('STOP', 'ascii'))

print("Transfers complete - shutting down")