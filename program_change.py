#!/usr/bin/env python
import sys
import rtmidi_python as rtmidi

if len(sys.argv) != 2 :
   print("Usage: " + sys.argv[0] + " <midi program number>")
   exit()

midi_out = rtmidi.MidiOut()

portnum = None

for idx in range(len(midi_out.ports) -1, -1, -1):
   if 'RtMidi Input Client:' in midi_out.ports[idx]:
      portnum = idx
      break

if portnum == None:
   print(sys.argv[0] + ": No RtMidi input client found")
   exit()

prognum = int(sys.argv[1], 10)

midi_out.open_port(portnum)
prog = [ 192 , prognum]
midi_out.send_message(prog)

