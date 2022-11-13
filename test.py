from pyogg.opus import OpusDecoder
import base64
import wave
import os
a = ""
opus_decoder = OpusDecoder()

wave_write = wave.open("a.wav", "wb")

    # Save the wav's specification
a = ""
with open("a.opus","rb") as f:
    a = f.read()
    
wave_write.setnchannels(2)
wave_write.setframerate(44100)
wave_write.setsampwidth(4)
pcm = opus_decoder.decode(a)
wave_write.writeframes(pcm)


    # Save the wav's specification



