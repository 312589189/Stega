from PIL import Image
import os
import CommandLine
import Steganography
import Cryptography
import optparse
import MyIO

#Gets the different command line options
parser = optparse.OptionParser()
parser.add_option("-i", "--input", dest="Source", help="The name of the file to hide your message in")
parser.add_option("-o", "--output", dest="Destination", 
        help="The name of the file to output your steganographic message to")
parser.add_option("-m", "--message", dest="Message",
        help="The file holding the text you want to hide")
parser.add_option("-e", action="store_false", help="Used to encode the file")
parser.add_option("-d", action="store_false", help="Used to decode the file")
parser.add_option("-p", "--password", dest="Password", help="The password used to encrypt the plaintext")
(options, args) = parser.parse_args()
#If the user didn't choose the necessary options, then tell them how to use the program and exit
if((options.e == None and options.d == None) or (options.e != None and options.d != None)
        or options.Source == None or options.Destination == None):
    os.system('python main.py -h')
    exit(0)
#If the user is trying to encode without passing in the message as an argument, then exit
if(options.e != None and options.Message == None):
    os.system('python main.py -h')
    exit(0)

#Encoding procedure
if(options.e != None):
    TextToHide = MyIO.ReadFile(options.Message)
    #If there is a password being passed, then encrypt the text using that password in the cipher
    if(options.Password != None):
        TextToHide = Cryptography.Encrypt(options.Password, TextToHide)
        TextToHide = str(TextToHide)
    #Open the file that you're hiding your message in
    Source = Image.open(options.Source, 'r')
    #Creates a message object with the source file and the hidden text
    Message = Steganography.Message(Source, TextToHide)
    Message.Encode()
    Message.Encoded.save(options.Destination)
#Decoding procedure
else:
    #Open the file with the hidden message
    Source = Image.open(options.Source, 'r')
    #Create a message object with the encoded message
    Message = Steganography.Message(None, None, Source)
    Message.Decode()
    #If there was a password being passed, then decrypt the text using that password in the cipher
    if(options.Password != None):
        Message.Secret = Message.Secret[1:]
        Message.Secret = eval(Message.Secret)
        Message.Secret = Cryptography.Decrypt(options.Password, Message.Secret)
    MyIO.WriteFile(options.Destination, Message.Secret)
