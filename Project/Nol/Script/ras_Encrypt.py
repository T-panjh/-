#!/usr/bin/env python
# -*- coding : utf-8 -*-
# demo debug pjh

import rsa

class Encrypt(object):
    def __init__(self, exponent,modulus):
        self.e = exponent
        self.m = modulus

    def encrypt(self,message):
        m = int(self.m,16)
        e = int(self.e,16)
        rsa_pubkey =rsa.PublicKey(m,e)
        crypto = self._encrypt(message.encode,rsa_pubkey)
        return crypto.hex()

    def _pad_for_encryption(self,message,target_length):
        message = message[::1]
        max_msglength = target_length -11
        msglength = len(message)

        padding = b''
        padding_length = target_length - msglength -3

        for i in range(padding_length):
            padding += b'\x00'

        return b''.join([b'\x00\x00',padding,b'\x00',message])


    def _encrypt(self,message,pub_key):
        keylength = rsa.common.byte_size(pub_key.n)
        padded = self._pad_for_encryption(message,keylength)

        payload = rsa.transform.bytes2int(padded)
        encrypted = rsa.core.encrypt_int(payload,pub_key.e,pub_key.n)
        block = rsa.transorm.int2bytes(encrypted,keylength)

        return block