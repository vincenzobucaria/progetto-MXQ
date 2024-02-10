import threading
import customtkinter
from tkinter import ttk
from PIL import Image, ImageTk
import os
import time
from record import *
from fft import * 






#CLASSE THREAD (serve per far avanzare la progress bar)


get_devices()

app = customtkinter.CTk()
app.geometry("800x600")
app.title("ANC measure software")

plot_flag = False


def start_measure():
    global nome_misura
    global nome_cuffie
    global modello_cuffie
    nome_misura = nome_misura_entry.get()
    modello_cuffie = nome_cuffie.get()
    print("DEBUG: avvio misura")
    global record_device 
    record_device = get_devices().index(seleziona_mic.get())
    print("COMBOBOX:", record_device)
    global new_finestra
    new_finestra = customtkinter.CTkToplevel(app)
    new_finestra.geometry("800x600")
    new_finestra.title("Misura senza cuffie")
    new_finestra.attributes("-topmost", True)
    global label_instructions
    label_instructions = customtkinter.CTkLabel(new_finestra, text="Assicurati che la cuffia sia disinserita dall'orecchio, quindi clicca MISURA per iniziare")
    label_instructions.pack(padx=20, pady=200)
    new_finestra.resizable(False, False)
    global first_meas_button
    first_meas_button = customtkinter.CTkButton(master=new_finestra, text="MISURA", command=start_measure_wout_headphones)
    first_meas_button.pack(pady=0)
  

def avanza_progress_bar(filename, stage):
    record_audios(filename, record_device)
    my_progress.stop()
    my_progress.pack_forget()
    label_working_measure.pack_forget()
    if(stage == 1):
        label_instructions = customtkinter.CTkLabel(new_finestra, text="La misura senza cuffie è terminata")
    
    if(stage == 2):
        label_instructions = customtkinter.CTkLabel(new_finestra, text="La misura con le cuffie è terminata")
    if(stage == 3):
        label_instructions = customtkinter.CTkLabel(new_finestra, text="La misura con ANC attiva è terminata")   
    label_instructions.pack(padx=20, pady=200)
    time.sleep(3)
    new_finestra.destroy()
    if(stage == 1 ):
        initialize_measure_with_headphones()
    if(stage == 2 ):
        initialize_measure_with_ANC()
    if(stage == 3):
        global plot_flag
        plot_flag = True    
    
    


def start_measure_wout_headphones():
    global my_progress
    global label_working_measure
    label_instructions.pack_forget()
    my_progress = customtkinter.CTkProgressBar(new_finestra, orientation="horizontal", mode="determinate", progress_color="white")
    first_meas_button.pack_forget()
    label_working_measure = customtkinter.CTkLabel(new_finestra, text="Misura in corso")
    label_working_measure.pack(padx=0, pady=200)
    # Mostra la barra di avanzamento
    my_progress.pack(pady=0)
    my_progress.configure(determinate_speed=0.49)
    my_progress.set(0)
    global filename1
    filename1 = "MOD_"+modello_cuffie+"_MEAS_"+nome_misura+"_MODE_"+"SENZA"
    thread_progress_bar = threading.Thread(target=avanza_progress_bar, args=(filename1,1,))
    thread_progress_bar.start()
    my_progress.start()
    
def initialize_measure_with_headphones():
    print("DEBUG: avvio misura")
    
    global new_finestra
    new_finestra = customtkinter.CTkToplevel(app)
    new_finestra.geometry("800x600")
    new_finestra.title("Misura con cuffie, ANC OFF")
    new_finestra.attributes("-topmost", True)
    global label_instructions
    label_instructions = customtkinter.CTkLabel(new_finestra, text="Assicurati che la cuffia sia inserita nell'orecchio e che la ANC sia disattivata, quindi clicca MISURA per iniziare")
    label_instructions.pack(padx=20, pady=200)
    new_finestra.resizable(False, False)
    global first_meas_button
    first_meas_button = customtkinter.CTkButton(master=new_finestra, text="MISURA", command=start_measure_with_headphones)
    first_meas_button.pack(pady=0)
        
def start_measure_with_headphones():
    global my_progress
    global label_working_measure
    label_instructions.pack_forget()
    my_progress = customtkinter.CTkProgressBar(new_finestra, orientation="horizontal", mode="determinate", progress_color="white")
    first_meas_button.pack_forget()
    label_working_measure = customtkinter.CTkLabel(new_finestra, text="Misura in corso")
    label_working_measure.pack(padx=0, pady=200)
    # Mostra la barra di avanzamento
    my_progress.pack(pady=0)
    my_progress.configure(determinate_speed=0.49)
    my_progress.set(0)
    global filename2
    filename2 = "MOD_"+modello_cuffie+"_MEAS_"+nome_misura+"_MODE_"+"CUFFIE"
    thread_progress_bar = threading.Thread(target=avanza_progress_bar, args=(filename2,2,))
    thread_progress_bar.start()
    my_progress.start()
    
def initialize_measure_with_ANC():
    print("DEBUG: avvio misura")
    
    global new_finestra
    new_finestra = customtkinter.CTkToplevel(app)
    new_finestra.geometry("800x600")
    new_finestra.title("Misura con cuffie, ANC ON")
    new_finestra.attributes("-topmost", True)
    global label_instructions
    label_instructions = customtkinter.CTkLabel(new_finestra, text="Assicurati che la cuffia sia inserita nell'orecchio e che la ANC sia ATTIVATA, quindi clicca MISURA per iniziare")
    label_instructions.pack(padx=20, pady=200)
    new_finestra.resizable(False, False)
    global first_meas_button
    first_meas_button = customtkinter.CTkButton(master=new_finestra, text="MISURA", command=start_measure_with_anc)
    first_meas_button.pack(pady=0)


def start_measure_with_anc():
    global my_progress
    global label_working_measure
    label_wrong_file.place_forget()
    label_instructions.pack_forget()
    my_progress = customtkinter.CTkProgressBar(new_finestra, orientation="horizontal", mode="determinate", progress_color="white")
    first_meas_button.pack_forget()
    label_working_measure = customtkinter.CTkLabel(new_finestra, text="Misura in corso")
    label_working_measure.pack(padx=0, pady=200)
    # Mostra la barra di avanzamento
    my_progress.pack(pady=0)
    my_progress.configure(determinate_speed=0.3)
    my_progress.set(0)
    global filename3
    filename3 = "MOD_"+modello_cuffie+"_MEAS_"+nome_misura+"_MODE_"+"ANC"
    thread_progress_bar = threading.Thread(target=avanza_progress_bar, args=(filename3,3,))
    thread_progress_bar.start()
    my_progress.start()
    




def mostra_grafici():
    
    print("SONO QUI")
    nome_misura = nome_misura_entry.get()
    modello_cuffie = nome_cuffie.get()
    generic_filename = os.path.join("measures","MOD_"+modello_cuffie+"_MEAS_"+nome_misura+"_MODE_")
    print(generic_filename)
    filename_1 = generic_filename + "SENZA"
    filename_2 = generic_filename + "CUFFIE"
    filename_3 = generic_filename + "ANC"
    print(filename_1+"_0dB.mp3")
    
    
    if (os.path.exists(filename_3+"_0dB.mp3")):
        print("STO CALC")
        calcola_le_fft(modello_cuffie, filename_1, filename_2, filename_3)
        label_wrong_file.place_forget()
    else:
        label_wrong_file.place(relx=0.22,rely=0.85)
        
    
    
    
    



left_frame = customtkinter.CTkFrame(master=app, width=400, height=600)
left_frame.pack(padx=0, pady=0, side="left")

label_wrong_file = customtkinter.CTkLabel(left_frame, text="Non ho trovato la misura selezionata")
start_button = customtkinter.CTkButton(master=left_frame, text="Misura", command=start_measure)
start_button.place(relx=0.3, rely=0.7)





nome_cuffie = customtkinter.CTkEntry(master=left_frame, placeholder_text="Nome cuffie ANC",  width=300, height=40)
nome_cuffie.place(relx=0.1, rely=0.1)

nome_misura_entry = customtkinter.CTkEntry(master=left_frame, placeholder_text="Nome misura", width=300, height=40)
nome_misura_entry.place(relx=0.1, rely=0.25)

plot_button = customtkinter.CTkButton(master=left_frame, text="Mostra i grafici", command=mostra_grafici)
plot_button.place(relx=0.3, rely=0.8)

global seleziona_mic
seleziona_mic = customtkinter.CTkComboBox(master=left_frame, values=get_devices(), text_color="white")
seleziona_mic.place(relx=0.3, rely=0.55)

image_frame = customtkinter.CTkFrame(master=app)
image_frame.pack(side="right", fill="both", expand=True, padx=10)


image_path = "earbuds.png"  
if os.path.exists(image_path):
    image = Image.open(image_path)
    image = ImageTk.PhotoImage(image)
    image_label = customtkinter.CTkLabel(master=image_frame, image=image, bg_color="blue")
    image_label.image = image
    image_label.pack_forget()
    image_label.pack(fill="both", expand=True)
    
if(plot_flag==True):
    calcola_le_fft(modello_cuffie,filename1,filename2,filename3)
    plot_flag = False


app.mainloop()

