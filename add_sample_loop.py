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


if len(sys.argv) != 3 :
    print("Usage: " + sys.argv[0] + " <sample.wav> <audacity-markers.txt>")
    exit()

wf = wave.open(sys.argv[1], "r")
print wf.getnframes()
print wf.getframerate()

framerate = wf.getframerate()

markers = open(sys.argv[2], "r")

nloops = 0
loops = []   
line = markers.readline()
while line:
    info = line.split("\t")
    starttime = info[0]
    endtime = info[1]
    print "Loop times[" + starttime + ":" + endtime + "]"
    startframe = int(round(float(info[0]) * framerate))
    endframe = int(round(float(info[1]) * framerate))
    print "Loop frames[" + str(startframe) + ":" + str(endframe) + "]"
    loops.append([startframe, endframe])
    nloops+=1
    line = markers.readline()

print str(nloops) + " sample loops found"

resultf = open(sys.argv[1], "rw+")
# RIFF
chunk = Chunk(resultf, bigendian=0)
# WAVE
resultf.read(4)
# skip existing chunks
while 1:
    try:
        chunk = Chunk(resultf, bigendian=0)
    except EOFError:
        break
    chunk.skip()

# write smpl chunk
resultf.write("smpl")
chunksize = 36 + 24 * nloops
encodedsize = struct.pack("<i", chunksize)
resultf.write(encodedsize)
header = struct.pack('<iiiiiiiii', 0, 0, 0, 0, 0, 0, 0, nloops, 0)
resultf.write(header)
sampleinfo = struct.pack('<iiiiii', 0, 0, startframe, endframe, 0, 0)
resultf.write(sampleinfo)

# update wavefile length
resultsize = resultf.tell() - 8
resultf.seek(4)
encodedsize = struct.pack("<i", resultsize)
resultf.write(encodedsize)

resultf.close()
