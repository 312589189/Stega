"""
Name: WriteFile
Purpose: Writes text to a file
Param Filename: The file to be written to 
Param Text: The text to be written to the file
Author: Samuel McManus
Used By: PrivateKey.Decrypt
Date: September 30, 2020
"""
def WriteFile(Filename, Text):
    f = open(Filename, "w")
    f.write(Text)
    f.close()
"""
Name: ReadFile
Purpose: Returns the text held in a file
Param Filename: The name of the file to be read
Return: The text held in the chosen file
Author: Samuel McManus
Used By: PublicKey.Encrypt
Date: September 30, 2020
"""
def ReadFile(Filename):
    try:
        f = open(Filename, "r")
        a = f.read()
        f.close()
        return a
    except FileNotFoundError:
        return ""
