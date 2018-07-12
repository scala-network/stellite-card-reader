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
import struct

# list all available readers
def list_readers():
    """

    :rtype : object
    """
    r = readers()
    return r

# activate selected readers
def activate_card(reader):
    connection = reader.createConnection()
    connection.connect()
    return connection

def reader_c_apdu(connection, apdu):
    """
    :param connection: connection that active now
    :param apdu: apdu string
    :return: R-APDU
    """
    conn = connection.transmit(apdu)
    return conn


def deactivate_all_reader():
    reader_list = list_readers()
    try:
        for i in range(0, len(reader_list)):
            connection = reader_list[i].createConnection()
            connection.disconnect()
    except:
        print("\n")
        print('error disconnecting')
    else:
        print("\n")
        print('disconnect success')
    return
    
def stelliteCard_select(connection):
    apdu = [0x00, 0xA4, 0x04 , 0x00 , 0x05 , 0x78 , 0x74 , 0x6C , 0x61 , 0x70 , 0x00]
    for j in range(4):
        try:
            result = reader_c_apdu(connection, apdu)
        except:
            if j == 3:
                return False
        else:
            break        
    response = [result[1]] + [result[2]]
    if response != [0x90, 0x00]:
        return False
    else:
        return True 
        
def stelliteCard_getVersion(connection):
	apdu = [0xB0, 0x30 , 0x00 , 0x00 , 0x00]
	for j in range(4):
		try:
			result = reader_c_apdu(connection, apdu)
		except:
			if j == 3:
				return False
		else:
			break       
	response = [result[1]] + [result[2]]
	if response != [0x90, 0x00]:
		return False
	else:
		return result[0]          
        
def stelliteCard_reqTxsEncrypt(connection, destAddress, txsType, txsAmount):
	txsAmount = list(struct.pack(">I", int(txsAmount)))
	txsAmount = [ord(i) for i in txsAmount]

	destAddress = list(destAddress)
	destAddressInt = []	
	for i in range(0,len(destAddress)):
		destAddressInt.append(ord(destAddress[i]))	
	apdu = [0xB0, 0x31 , 0x00 , 0x00 , 0x66] +  [txsType] + txsAmount + destAddressInt
	for j in range(4):
		try:
			result = reader_c_apdu(connection, apdu)
		except:
			if j == 3:
				return False
		else:
			break       
	response = [result[1]] + [result[2]]
	if response != [0x90, 0x00]:
		return False
	else:
		return result[0]  
		
def stelliteCard_verifyTxs(connection, txsSignature):
	apdu = [0xB0, 0x32 , 0x00 , 0x00 , 0x80] + txsSignature[0:128]
	for j in range(4):
		try:
			result = reader_c_apdu(connection, apdu)
		except:
			if j == 3:
				return False
		else:
			break       
	response = [result[1]] + [result[2]]
	if response != [0x90, 0x00]: 		
		return False
	else:		
		apdu = [0xB0, 0x32 , 0x00 , 0x01 , 0x80] + txsSignature[128:256]
		for j in range(4):
			try:
				result = reader_c_apdu(connection, apdu)
			except:
				if j == 3:
					return False
			else:
				break
		response = [result[1]] + [result[2]]
		if response != [0x90, 0x00]:	
			return False
		else:		 		
			return result[0]  		       
        
