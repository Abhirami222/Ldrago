import os
import numpy as np
from flask import Flask
app = Flask(__name__)
from flask import render_template, request
from datetime import datetime
import librosa as lr
from glob import glob
import matplotlib.pyplot as plt
import pygame

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method=="POST":
        file = request.files["file"]
        file.save(os.path.join('uploads',file.filename))
        data_dir='./uploads'
        audio_file = glob(data_dir +'/*.wav')
        audio, sfreq=lr.load(audio_file[0])
        x=lr.get_duration(y=audio, sr=sfreq)
        x=int(len(audio)/x)
        print(x)
        time = np.arange(0, len(audio)) / sfreq
        pygame.mixer.init()
        my_sound = pygame.mixer.Sound(audio_file[0])
        my_sound.play()
        fig, ax = plt.subplots()
        plt.show(block=False)
        for i in range(0, len(audio), x):
            pygame.time.wait(820)
            chunk = audio[i:i + x]
            t = time[i:i + x] 
            ax.plot(t, chunk)
            ax.set(xlabel='Time(s)',ylabel='Sound Amplitude')
            fig.canvas.draw()
            fig.canvas.flush_events()

        os.remove(audio_file[0])
       

        return render_template("index.html",message="sucess")
    return render_template("index.html",message="Upload")
if __name__ == '__main__':
    app.run(debug=True) 