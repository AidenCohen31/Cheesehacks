import base64
import wave
import os
import subprocess
file = 0
for i in os.listdir("tests"):
    if(i.endswith(".txt")):
        with open(f"tests/{i}", "r") as f:
            a = f.read()
            if(len(a) > 0):

                a = base64.b64decode(a.split(",")[1][:-1])
            print(len(a))
            with open(f"tests/{file}.webm" , "wb+") as f:
                if(len(a) > 0):
                    f.write(a)
        subprocess.run(["ffmpeg" ,"-y","-i", f"tests/{file}.webm", "-vn", f"tests/{file}.wav"])
        
        file+=1


    # Save the wav's specification



