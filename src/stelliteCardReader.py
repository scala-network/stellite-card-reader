# Copyright (c) 2014-2018, The Stellite Project
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of
#    conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
#    of conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be
#    used to endorse or promote products derived from this software without specific
#    prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__author__ = 'ereddon'

from smartcard.System import readers
from smartcard import Exceptions
from stelliteCardComm import *
import sys
import requests
import json
import ctypes


# configure your merchant information here

MERCHANT_ADDR = "Se3NS696nhRVk4Ye9vH9QQ7i6LdMXSFQd93GaeirdbUicnefP2GrVKnMhvsMgjaMCwDvNGTMzgEYDa2Ke7Pm1NJa2pK2eAbM5"

# app configuration

url= 'http://localhost:4000/transfer'
headers = {'User-Agent': 'Mozilla/5.0'}
cardVersion = "StelliteCard-v1.0"

# exit message

def exit_message(input_text):
    print(input_text + ' press q to exit')
    while sys.stdin.readline() != 'q\n':
        print("\n")
        print('press q to exit...')
    sys.exit()
    
    
# main program
print("#########################################################")
print("##                                                     ##")
print("##                                                     ##")
print("##       StelliteCard One Time TXS Merchant App        ##")
print("##                  By : Ereddon                       ##")
print("##                discord : @reddon                    ##")
print("##                                                     ##")
print("##                                                     ##")
print("#########################################################")
print("\n")
print("MERCHANT ADDRESS : " + MERCHANT_ADDR)
print("\n")

# bypass transaction type for now

'''
# polling for transaction type
key_input = False
print('Transaction available: ')
txsType = ["pay using XTL", "top up XTL balance"]
# show the reader list
for i in range(0, len(txsType)):
    print(str(i) + '. ' + str(txsType[i]))
txsSelected = 0
while not key_input:
    i = 0
    print('Choose transaction type...')
    char = sys.stdin.readline()
    try:
        charint = int(char)
    except:
        print('something is wrong with your input...')
    else:
        sys.stdin.flush()
        for i in range(len(txsType)):
            if charint == i:
                key_input = True
                txsSelected = i
                break
'''

txsSelected=0

if txsSelected==0:
	txsAmount = input("<INFO > Enter amount to pay: \n")
else:
	txsAmount = input("<INFO > Enter amount to top up to: ")

print("\n")
print("<INFO > TRANSACTION DETAILS ")
#print('transaction type: ' + str(txsType[i])) 
print('<INFO > amount: ' + ' ' + str(txsAmount) + ' XTL') 
if txsSelected==0:
	print('<INFO > destination: ' + str(MERCHANT_ADDR)) 
else:
	print('<INFO > destination: your stellitePay account') 	
print("\n")

# auto scan available readers
readers_avail = list_readers()
activeReader = None
scanAttempt = 0
for i in range (0, len(readers_avail)):
	scanAttempt+=1
	sys.stdout.write("<INFO > SCANNING: " + str(readers_avail[i]))
	try:
		activeReader = activate_card(readers_avail[i])
	except Exceptions.NoCardException:
		sys.stdout.write(" FAIL!\n")
		continue
	if stelliteCard_select(activeReader) == False:
		sys.stdout.write(" FAIL!\n")
		continue	
	result = stelliteCard_scanReaders(activeReader)
	result = [ctypes.c_ubyte(i).value for i in result]
	result = ''.join(chr(i) for i in result)
	if result != cardVersion:
		sys.stdout.write(" Wrong card version!\n")
	else:
		sys.stdout.write(" " + result + " FOUND!\n")	
		break		
if scanAttempt == len(readers_avail):
	print("<ERROR> NO READER/CARD FOUND!") 
	sys.exit()
	
# request to encrypt txs	
result = stelliteCard_reqTxsEncrypt(activeReader, MERCHANT_ADDR, txsSelected, int(txsAmount))	
if result == False:
	print('<ERROR> CARD ENCRYPT ERROR!')
else:
	print('<INFO > CARD ENCRYPT OK!')
	print('<INFO > CIPHERED DATA FROM CARD: ')
	print("\n" + ''.join(chr(i) for i in result) + "\n")
	

# TODO send encrypted data to server
'''	
payload = {"cipherTxsRequest":json.dumps(result)}
resp=requests.post(url,data=payload,headers=headers)
print(resp.__dict__)
print(resp.content)
if(resp.status_code!=200):
	exit_message('ERROR when sending request...')
else:
	signature = resp.content
'''

# dummy signature for now
signature = "afahchfhudshfkashdkhaskfhddu67f863rgf7t7t37tf78387f7tf2c7t47rct3ch7ct7c6t36htcf673ct763ccgt67ft36xh3tf673tf763t6xt36ft64tf67ht36fxt36tf67t346ftxh672t673tf76hx346jyxwfebtbfxfytdftefwxcqnxyxgyfq364n4623c4296tt2f364c63cn6t32nxuwrygfc82g467gfc64y6f738y7fnhx7y1"

# send txs signature to card
result = stelliteCard_verifyTxs(activeReader, signature)
if result == False:
	print('<ERROR> SIGNATURE VERIFICATION PROCESS FAIL!')
else:
	print('<INFO > SIGNATURE VERIFICATION PROCESS OK!')
	print('<INFO > CIPHERED DATA FROM CARD: ')
	print("\n" + ''.join(chr(i) for i in result) + "\n")
	
# TODO send encrypted data to server
'''	
payload = {"cipherTxsRequest":json.dumps(result)}
resp=requests.post(url,data=payload,headers=headers)
print(resp.__dict__)
print(resp.content)
if(resp.status_code!=200):
	exit_message('ERROR when sending request...')
else:
	signature = resp.content
'''






	
