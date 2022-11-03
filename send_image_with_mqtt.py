# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 13:22:41 2022

@author: joseph@艾鍗學院

base64 encode binary file

"""

# use base64 to encode image file
import base64

def encode_base64(file):
    # rb meaning open with read/binary mode
    with open(file, "rb") as f:
        encoded_string = base64.b64encode(f.read())
    
    return encoded_string.decode('utf-8')



if __name__ == '__main__' :
    
    c=encode_base64('lin.jpg')
    print(c)
    # import datetime
    # filename=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+'.png'
    # with open(filename, "wb") as save_file:
    #     save_file.write(base64.decodebytes(encoded_string))


