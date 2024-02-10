import pyaudio
import winsound
import wave
import audioop
import math
import numpy as np
import customtkinter
from tkinter import ttk
from PIL import Image, ImageTk
import os
import time
import threading
import sounddevice as sd
from pydub import AudioSegment
from pydub.playback import play









chunk = 1024  
sample_format = pyaudio.paInt16  #Numero di bit per campione
channels = 1
fs = 44100  # Frequenza di campionamento
seconds = 5 #Durata della registrazione

type_of_noise = "plane_" 



def get_devices(): #Restituisce la lista dei dispositivi audio 
    
    device_list = list()
    
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()
    for i in range(0, device_count):
        info = p.get_device_info_by_index(i)
        device_list.append("Device {} = {}".format(info["index"], info["name"]))
    return device_list
    




def record_audios(filename, device_index):

    
    for elements in ["0dB", "-3dB", "-6dB", "-9dB"]: #Ciclo for per fare 4 misure con 4 livelli di rumore differenti
        
        path_white_noise = os.path.join("noise",type_of_noise+elements+".wav" )
        
        winsound.PlaySound(path_white_noise,winsound.SND_ASYNC | winsound.SND_ALIAS ) #Riproduce il rumore di test
        #Ho introdotto 1 secondo di delay per assicurarmi che la registrazione avvenga sicuramente dopo l'inizio della riproduzione dell'audio di test    
        

        p = pyaudio.PyAudio() 
        
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        input_device_index=device_index,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  

        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            max = audioop.max(data, 2)
            print(20*math.log10(max)-91.28, max)
            frames.append(data)

        
        stream.stop_stream()
        stream.close()
        
        p.terminate()

        measure_path = os.path.join("measures",filename+"_"+elements+".mp3")
        print(measure_path)
        wf = wave.open(measure_path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        winsound.PlaySound(None, winsound.SND_ASYNC)
        time.sleep(2)