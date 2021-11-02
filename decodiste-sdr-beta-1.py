#########################
# -*- coding: utf-8 -*- #
#   <- python 3.8.1 ->  #    

""" long commentaire
alt gr + 7 pour: ```
```python
discord
discord```


"""

#########################
#< ! DOCTYPE python>
#########################
#  interface - sdr - 2  #
#########################



import matplotlib
import time
from os import wait
import textwrap
from textwrap import *
import sys
from sys import *
import tkinter
from tkinter import *
import io
from io import *
import subprocess
from subprocess import *

######################
# titre du programme #
######################

fenetreprincipale = Tk()
fenetreprincipale.title('decodiste-sdr-beta-1.75-2021')


####################################
# taille de la fenetre par default #
####################################

fenetreprincipale.geometry("1600x800")


###################
# couleur de fond #
###################

fenetreprincipale.configure(bg='grey')

#########
# icone #
#########

fenetreprincipale.iconbitmap('@/home/tartempion/Documents/python/sdr/antenne.xbm')


#####################################################################
# 2               parametres par default                            #
#####################################################################

demodulation0 = ["wbfm", "wbfm", "fm" , "am", "lsb", "usb", "raw" ]
freq = "94200000"
sample_rate = "250000"
ppm = "0"
 

#############################################
# bouton slider frequence, ppm, sample_rate #
#############################################



frequence0 = Scale(fenetreprincipale, label="frequence", 
from_=88000000, to=108000000, resolution=1000, orient=HORIZONTAL, activebackground="yellow", 
background="green")
frequence0.set(freq)
frequence0.place(x=600, y=0, width=500 , height=60)


sample_rate0 = Scale(fenetreprincipale, label="sample_rate", 
from_=0, to=2000000, length=750, orient=HORIZONTAL, activebackground="yellow", background="green")
sample_rate0.set(sample_rate)
sample_rate0.place(x=600, y=60, width=500 , height=60)


ppm0 = Scale(fenetreprincipale, label="ppm", 
from_=0, to=200, orient=HORIZONTAL, activebackground="yellow", background="green")
ppm0.set(ppm)
ppm0.place(x=600, y=120, width=500 , height=60)

#######################################################################
# bouton  demodulation0 = ["wbfm", "fm" , "am", "lsb", "usb", "raw" ] #
#######################################################################


wbfm0 =  Radiobutton(fenetreprincipale, indicatoron=False, value=0, variable=0, command=lambda: 
[change0demodulationwbfm(),
stop_rtl_fm(),
start_rtl_fm(demodulation0[1], frequence0, sample_rate0, ppm0)], text="wbfm", activebackground='green', background='purple')
wbfm0.place(x=0, y=40, width=60, height=35)


fm0 = Radiobutton(fenetreprincipale, indicatoron=False, value=1, variable=0, command=lambda: 
[change0demodulationfm(),
stop_rtl_fm(),
start_rtl_fm(demodulation0[2], frequence0, sample_rate0, ppm0)], text="fm", activebackground='green', background='purple')
fm0.place(x=60, y=40, width=60, height=35)


am0 = Radiobutton(fenetreprincipale, indicatoron=False, value=2, variable=0, command=lambda: 
[change0demodulationam(),
stop_rtl_fm(), 
start_rtl_fm(demodulation0[3], frequence0, sample_rate0, ppm0)], text="am  ", activebackground='green', background='purple')
am0.place(x=120, y=40, width=60, height=35)


lsb0 = Radiobutton(fenetreprincipale, indicatoron=False, value=3, variable=0, command=lambda:  
[change0demodulationlsb(),
stop_rtl_fm(), 
start_rtl_fm(demodulation0[4], frequence0, sample_rate0, ppm0)], text="lsb ", activebackground='green', background='purple')
lsb0.place(x=0, y=75, width=60, height=35)

usb0 = Radiobutton(fenetreprincipale, indicatoron=False, value=4, variable=0, command=lambda: 
[change0demodulationusb(),
stop_rtl_fm(), 
start_rtl_fm(demodulation0[5], frequence0, sample_rate0, ppm0)], text="usb ", activebackground='green', background='purple')
usb0.place(x=60, y=75, width=60, height=35)

raw0 = Radiobutton(fenetreprincipale, indicatoron=False, value=5, variable=0, command=lambda:  
[change0demodulationraw(),
stop_rtl_fm(),
start_rtl_fm(demodulation0[6], frequence0, sample_rate0, ppm0)], text="raw ", activebackground='green', background='purple')
raw0.place(x=120, y=75, width=60, height=35)




#######################################
#       boutons: start et stop        #
#######################################




start = Button(fenetreprincipale, text='start', activebackground='blue', 
command=lambda: start_rtl_fm(demodulation0[0], frequence0, sample_rate0, ppm0))
start.place(x=0, y=0)

stop = Button(fenetreprincipale, text='stop', activebackground='red', 
command=lambda: stop_rtl_fm())
stop.place(x=60, y=0)




############
# fonction #
############

def change0demodulationwbfm():
    demodulation0[0] = "wbfm"

def change0demodulationfm():
    demodulation0[0] = "fm"


def change0demodulationam():
    demodulation0[0] = "am"

 
def change0demodulationlsb():
    demodulation0[0] = "lsb"   


def change0demodulationusb():
    demodulation0[0] = "usb"


def change0demodulationraw():
    demodulation0[0] = "raw"

def stop_rtl_fm():  
    stopoutput = subprocess.run(args="killall rtl_fm", 
    capture_output=True, shell = True, text = True)
    time.sleep(1.5)
    
    
    
   
    

def start_rtl_fm(demodulation0, frequence0, sample_rate0, ppm0): 
    stop_rtl_fm()
    startoutput = subprocess.Popen(args="rtl_fm -M "+ str(demodulation0) +" -f "+ str(frequence0.get()) +" -s "+ str(sample_rate0.get()) +" -p "+ str(ppm0.get()) + " | play -r 32k -t raw -e s -b 16 -c 1 -V1 -", 
    shell = True, text = True)
    text.delete("1.0","end")
    text.insert(INSERT, "terminal:" "\n") 
    text.insert(INSERT,"parametres utiliser: demodulation "+ str(demodulation0)+"\n")
    text.insert(INSERT,"parametres utiliser: frequences   "+ str(frequence0.get())+"\n")
    text.insert(INSERT,"parametres utiliser: samprate     "+ str(sample_rate0.get())+"\n")
    text.insert(INSERT,"parametres utiliser: ppm          "+ str(ppm0.get())+"\n")


def restart(Event):
    start_rtl_fm(demodulation0[0], frequence0, sample_rate0, ppm0)
    time.sleep(1.5)
    
frequence0.bind("<ButtonRelease-1>", restart)
sample_rate0.bind("<ButtonRelease-1>", restart)
ppm0.bind("<ButtonRelease-1>", restart)




#    startoutput = subprocess.Popen(args="rtl_fm -M wbfm -f 100M -s 250000 -r 32k | play -r 32k -t raw -e s -b 16 -c 1 -V1 -", 
#    shell = True, text = True)    
    
   
# ajoute volume , mute


############
#  texte 1 #
############

text = Text(fenetreprincipale, border=4)
text.place(x=180, y=0, height=180, width=420)


#################################
###      -  waterfall  -      ###
#################################



#################################
#  fenetreprincipale.mainloop() #
#################################

fenetreprincipale.mainloop()
