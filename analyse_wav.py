#!/usr/bin/env python
import sys
import struct
import wave
from chunk import Chunk

#wf = wave.open("0 Saw/36.wav", "r")
#>>> wf.getframerate()
#44100
#>>> wf.getnframes()
#8764

#pi@raspberrypi:~/Documents/SamplerBox $ python analyse_wav.py 0\ Saw/36.wav
#fmt
#data
#sample
#1
#loop 0 [0:8763]

# duration in Audacity 00h00m00.199s
# nframes/framerate
#>>> 8764.0 / 44100
#0.19873015873015873


if len(sys.argv) != 2 :
    print("Usage: " + sys.argv[0] + " <sample.wav>")
    exit()

wf = wave.open(sys.argv[1], "r")
print wf.getnframes()
print wf.getframerate()
   
f = open(sys.argv[1], "r")

cf = Chunk(f, bigendian=0)

if cf.getname() != 'RIFF':
    raise Error, 'file does not start with RIFF id'
   
if cf.read(4) != 'WAVE':
    raise Error, 'not a WAVE file'
        
while 1:
    try:
        chunk = Chunk(f, bigendian=0)
    except EOFError:
        break
    chunkname = chunk.getname()
    print chunkname
    if chunkname == 'smpl':
        manuf, prod, sampleperiod, midiunitynote, midipitchfraction, smptefmt, smpteoffs, numsampleloops, samplerdata = struct.unpack(
            '<iiiiiiiii', chunk.read(36))
        print numsampleloops
        for i in range(numsampleloops):
            cuepointid, type, start, end, fraction, playcount = struct.unpack('<iiiiii', chunk.read(24))
            print "loop " + str(i) + " [" + str(start) + ":" + str(end) + "]"
#           self._loops.append([start, end])
    chunk.skip()
