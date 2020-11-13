import sys
from PIL import Image
class Message:
    """
    Distractor: The picture which the message is being hidden in
    Secret: The secret message
    Encoded: The picture with the message encoded in it
    """
    def __init__(self, Distractor = None, Secret = None, Encoded = None):
        self.Distractor = Distractor
        if(Distractor != None):
            self.DistractorSize= self.Distractor.size[0] * self.Distractor.size[1]
        self.Secret = Secret
        if(Secret != None):
            self.SecretLength = len(self.Secret) * 8
        self.SecretLengthBits = ''
        self.SecretBits = ''
        self.Encoded = Encoded
        if(self.Encoded != None):
            self.EncodedSize = self.Encoded.size[0] * self.Encoded.size[1]
   
    """
    Name: WriteMessage
    Purpose: To write a bit of a secret message into a bit of r/g/b space
    Param Destination: The R, G, or B array which the bit is being stored in
    Param DestOffset: The offset inside of the R/G/B array to store the bit in
    Param SourceOffset: The offset inside of the secret message bit array to store in the picture
    Return: The r/g/b space of the picture
    Author: Samuel McManus
    """
    def WriteMessage(self, Destination, DestOffset, SourceOffset):
        #Mask out the low order bit
        Destination[DestOffset] = Destination[DestOffset] // 2
        Destination[DestOffset] = Destination[DestOffset] * 2
        #Replace it with the bit of the message array
        Destination[DestOffset] = Destination[DestOffset] + int(self.SecretBits[SourceOffset])
        return Destination[DestOffset]
    """
    Name: Encode
    Purpose: Encodes a picture with a secret message using steganography
    Author: Samuel McManus
    """
    def Encode(self):
        #Gets the length of the secret message in bits and the size of the picture in pixels
        self.DistractorSize= self.Distractor.size[0] * self.Distractor.size[1]
        #If there are more bits in the message than R/G/B spaces in the picture, then exit
        if(self.SecretLength > (self.DistractorSize*3)):
            print("Your message is too long for this picture ")
            exit(0)
        elif (self.SecretLength > ((2**33) - 1)):
            print("Your message is too long")
            exit(0)

        #Split the image's pixels into R/G/B, then convert the R/G/B into 
        #lists of every R/G/B space in the picture
        r, g, b = self.Distractor.split()
        r = list(r.getdata())
        g = list(g.getdata())
        b = list(b.getdata())
        #Transforms the length of the message to a 32-bit binary
        self.SecretLengthBits = bin(self.SecretLength)[2:].rjust(32, "0") 
        #Transforms the message to a string of 8-bit binary numnbers
        for char in (self.Secret):
            self.SecretBits += bin(ord(char))[2:].rjust(8, "0")
        #Embed the length of the message in the first R bits
        for i in range(32):
            r[i] = r[i]//2
            r[i] = r[i] * 2
            r[i] = r[i] + int(self.SecretLengthBits[i])
        Iterations = 0
        #Continue embedding the message in the remaining R bits
        for i in range(self.DistractorSize - 32):
            if(Iterations >= self.SecretLength):
                break
            r[i+32] = self.WriteMessage(r, i+32, i)
            Iterations += 1
        #Continue embedding the message in the G bits
        for i in range(self.DistractorSize):
            if(Iterations >= self.SecretLength):
                break
            r[i] = self.WriteMessage(g, i, Iterations)
            Iterations += 1
        #Continue embedding the message in the B bits
        for i in range(self.DistractorSize):
            if(Iterations >= self.SecretLength):
                break
            r[i] = self.WriteMessage(b, i, Iterations)
            Iterations += 1
        #Create the new R/G/B images
        NewRed = Image.new("L", (self.Distractor.size[0], self.Distractor.size[1]))
        NewRed.putdata(r)
        NewGreen = Image.new("L", (self.Distractor.size[0], self.Distractor.size[1]))
        NewGreen.putdata(g)
        NewBlue = Image.new("L", (self.Distractor.size[0], self.Distractor.size[1]))
        NewBlue.putdata(b)
        self.Encoded = Image.merge('RGB', (NewRed, NewGreen, NewBlue))

    """
    Name: Decode
    Purpose: To retrieve a secret message from an encoded image
    Author: Samuel McManus
    """
    def Decode(self):
        #Split the image's pixels into R/G/B, then convert the R/G/B into 
        #lists of every R/G/B space in the picture
        r, g, b = self.Encoded.split()
        r = list(r.getdata())
        g = list(g.getdata())
        b = list(b.getdata())
        #Get the length of the message from the red pixels' space
        for i in range(32):
            if(r[i] % 2 == 1): 
                self.SecretLengthBits += '1'
            else:
                self.SecretLengthBits += '0'
        #Converts the length of the message to an integer
        self.SecretLength = int(self.SecretLengthBits, 2)
        self.SecretBits = '0'
        self.Secret = ''
        Iterations = 0
        #Retrieve the message from the R space in the pixels
        for i in range(self.EncodedSize - 32):
            if(Iterations > self.SecretLength):
                break
            if(Iterations % 8 == 0):
                self.Secret += chr(int(self.SecretBits, 2))
                self.SecretBits = ''
            if(r[i + 32] % 2 == 1):
                self.SecretBits += '1'
            else:
                self.SecretBits += '0'
            Iterations += 1
        #Retrieve the remainder of the message from the G space in the pixels
        for i in range(self.EncodedSize):
            if(Iterations > self.SecretLength):
                break
            if(Iterations % 8 == 0):
                self.Secret += chr(int(self.SecretBits, 2))
                self.SecretBits = ''
            if(g[i] % 2 == 1):
                self.SecretBits += '1'
            else:
                self.SecretBits += '0'
            Iteration += 1
        #Retrieve the remainder of the message from the B space in the pixels
        for i in range(self.EncodedSize):
            if(Iterations > self.SecretLength):
                break
            if(Iterations % 8 == 0):
                self.Secret += chr(int(self.SecretBits, 2))
                self.SecretBits = ''
            if(b[i] % 2 == 1):
                self.SecretBits += '1'
            else:
                self.SecretBits += '0'
            Iteration += 1
