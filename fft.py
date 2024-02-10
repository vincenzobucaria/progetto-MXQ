import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy import signal

volumi = ["_0dB.mp3", "_-3dB.mp3", "_-6dB.mp3", "_-9dB.mp3"]


def calcola_le_fft(modello_cuffie, filename_1, filename_2, filename_3):
   
   
   mode_vector = ["Trasparenza", "ANC OFF", "ANC ON"]
   color_vector = ["green", "red", "blue"]
   
   
   for volume in volumi:
        plt.figure(volumi.index(volume),figsize=(12, 6))
        
        print(filename_2)
        
        for i in range(1, 4):
            
            if(i==1):
                    y, sr = librosa.load(filename_1+volume, sr=None)
            if(i==2):
                    y, sr = librosa.load(filename_2+volume, sr=None)
            if(i==3):
                    y, sr = librosa.load(filename_3+volume, sr=None)
            
            
            
            fft_result = np.fft.fft(y)
            frequencies = np.fft.fftfreq(len(fft_result), 1/sr)
            fft_result_db = librosa.amplitude_to_db(np.abs(fft_result))

            positive_frequencies = frequencies[:len(frequencies)//2]
            positive_fft_result = 2.0/len(y) * np.abs(fft_result[:len(fft_result)//2])
            positive_fft_result_db = librosa.amplitude_to_db(np.abs(positive_fft_result))
            freq_mask = (positive_frequencies >= 100) & (positive_frequencies <= 10000)
            low_freq_positive_fft_result_db = positive_fft_result_db[freq_mask]   
            mean_value_low_freq = np.mean(low_freq_positive_fft_result_db)
            
            plt.semilogx(positive_frequencies, positive_fft_result_db, label=mode_vector[i-1], color=color_vector[i-1])
            
            plt.axhline(y=mean_value_low_freq, linestyle='--', label='Valore medio (LF) '+mode_vector[i-1], color= color_vector[i-1])
        plt.title(modello_cuffie+volume)
        plt.xlabel('Frequenza (Hz)')
        plt.ylabel('Ampiezza(dB)')
        plt.xlim([70, 20000])
        plt.ylim(-110, 0)
        plt.legend()
        

        plt.tight_layout()
   plt.show()
   



    
