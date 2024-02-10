from pydub import AudioSegment
from pydub.playback import play



def riproduci_rumore():
    # for playing wav file
    print("DEBUG: MAa")
    song = AudioSegment.from_wav("white_noise.wav")
    print('DEBUG: rumore bianco')
    play(song)
    
