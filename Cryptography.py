import blowfish

"""
Name: Encrypt
Purpose: Encrypt the plaintext message using blowfish
Param password: The password used for blowfish encryption
Param plaintext: The plaintext being encrypted
Return: The ciphertext
Author: Samuel McManus
"""
def Encrypt(password, plaintext):
    #Create the blowfish cipher
    cipher = blowfish.Cipher(bytes(password, 'utf-8'))
    #If the plaintext isn't a multiple of the blocksize, pad the plaintext with spaces
    remainder = len(plaintext) % 8
    if(remainder != 0):
        while(remainder < 8):
            remainder += 1
            plaintext += ' '
    #Encrypt the plaintext using ecb mode
    ciphertext = b"".join(cipher.encrypt_ecb(bytes(plaintext, 'utf-8')))
    return ciphertext

def Decrypt(password, ciphertext):
    #Create the blowfish cipher
    cipher = blowfish.Cipher(bytes(password, 'utf-8'))
    #Decrypt the plaintext
    plaintext = b"".join(cipher.decrypt_ecb(ciphertext))
    plaintext.decode('utf-8')
    #Take the plaintext out of utf-8 and return it 
    return str(plaintext, 'utf-8')
