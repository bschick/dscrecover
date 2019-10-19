#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import serial

SERIALDEVICE = '/dev/ttyUSB0'

def complete(payload):
   '''add checksum and CR LF to payload to make is a valid command'''
   # such a strange checksum process
   s = sum(payload) & 0xFF
   high, low = s >> 4, s & 0xF
   chars = f"{high:x}{low:x}".upper()
   return payload + bytes([ord(chars[0]), ord(chars[1]), 0xd, 0xa])

POLL = complete(bytes([0x30,0x30,0x30]))
STATUS = complete(bytes([0x30,0x30,0x31]))
LABELS = complete(bytes([0x30,0x30,0x32]))
BREAK = complete(bytes([0x30,0x37,0x30,0x5E]))


def eat(ser):
   while True:
      result = ser.readline()
      if not result:
         break

def wait(ser):
   while True:
      result = ser.readline()
      if result[:3] == bytes('500','ascii'):
         break
      elif result[:3] == bytes('501','ascii'):
         print('!! bad checksum')
      elif result[:3] == bytes('502','ascii'):
         print(f'!! error: {result[3:6]}')

def is_code(ser):
    while True:
      result = ser.readline()
      if not result or 'Invalid Access  Code' in result.decode('ascii'):
         return False
      elif 'Enter Section   ---' in result.decode('ascii'):
         return True 

def press(ser, key):
   command = complete(bytes([0x30,0x37,0x30,ord(key)]))
   ser.write(command)
   ser.flush()
   wait(ser)
   ser.write(BREAK)
   ser.flush()
   wait(ser)

with serial.Serial(SERIALDEVICE, baudrate=9600, timeout=2) as ser:
   print("clearing")
   eat(ser)

   for code in range(0, 10000):
      guess = f'{code:04}'
      press(ser, '#')
      press(ser, '*')
      press(ser, '8')
      for i in range(4):
         press(ser, guess[i])
      if is_code(ser):
         print(f'{code} is the code')
         break
      else:
         print(f'{code} is invalid')
         eat(ser)

