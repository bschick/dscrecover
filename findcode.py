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


with serial.Serial(SERIALDEVICE, baudrate=9600, timeout=2) as ser:

   def eat():
      while True:
         result = ser.readline()
         if not result:
            break

   def wait():
      while True:
         result = ser.readline()
         if result:
            if result[:3] == bytes('500','ascii'):
               break
            elif result[:3] == bytes('501','ascii'):
               print('!! bad checksum')
            elif result[:3] == bytes('502','ascii'):
               print(f'!! error: {result[3:6]}')

   def was_code():
       while True:
         result = ser.readline()
         if not result or 'Invalid Access  Code' in result.decode('ascii'):
            return False
         elif 'Enter Section   ---' in result.decode('ascii'):
            return True 

   def press(key):
      command = complete(bytes([0x30,0x37,0x30,ord(key)]))
      ser.write(command)
      ser.flush()
      wait()
      ser.write(BREAK)
      ser.flush()
      wait()

   print("clearing response buffer")
   eat()

   for code in range(0, 10000):
      guess = f'{code:04}'
      press('#')
      press('*')
      press('8')
      for c in guess:
         press(c)

      if was_code():
         print(f'{guess} is the code')
         break
      else:
         print(f'{guess} is invalid')
         eat()
