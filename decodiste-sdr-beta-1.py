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



import usb
import time
from os import pipe, wait
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


icone = PhotoImage(file='antenne.gif')
fenetreprincipale.iconphoto(False, icone)


############
#  texte   #
############

text0 = Text(fenetreprincipale, border=4)
text0.place(x=180, y=0, height=180, width=420)
text1 = Text(fenetreprincipale, border=4)
text1.place(x=180, y=180, height=180, width=420)


###########################################
# class Idusb: le device est il present ? #
########################################### 

class Idusb:
   
#class des idvendeur et idproducteur
    
    
    def __init__(self, id_vendeur, id_producteur, _tunner, device_name):        
        
        self.idvendeur = id_vendeur
        self.idproducteur = id_producteur
        self.tunner =_tunner
        self.devicename = device_name

idusb00 = Idusb(0x0bda, 0x2832, "all of them", "Generic RTL2832U (e.g. hama nano)") 
idusb01 = Idusb(0x0bda, 0x2838, "E4000",       "ezcap USB 2.0 DVB-T/DAB/FM dongle") 
idusb02 = Idusb(0x0ccd, 0x00a9, "FC0012",      "Terratec Cinergy T Stick Black (rev 1)") 
idusb03 = Idusb(0x0ccd, 0x00b3, "FC0013", 	   "Terratec NOXON DAB/DAB+ USB dongle (rev 1)") 
idusb04 = Idusb(0x0ccd, 0x00d3, "E4000", 	   "Terratec Cinergy T Stick RC (Rev.3)") 
idusb05 = Idusb(0x0ccd, 0x00e0, "E4000", 	   "Terratec NOXON DAB/DAB+ USB dongle (rev 2)") 
idusb06 = Idusb(0x185b, 0x0620, "E4000",       "Compro Videomate U620F") 
idusb07 = Idusb(0x185b, 0x0650, "E4000",	   "Compro Videomate U650F") 
idusb08 = Idusb(0x1f4d, 0xb803, "FC0012", 	   "GTek T803") 
idusb09 = Idusb(0x1f4d, 0xc803, "FC0012", 	   "Lifeview LV5TDeluxe") 
idusb10 = Idusb(0x1b80, 0xd3a4, "FC0013", 	   "Twintech UT-40") 
idusb11 = Idusb(0x1d19, 0x1101, "FC2580",      "Dexatek DK DVB-T Dongle (Logilink VG0002A)") 
idusb12 = Idusb(0x1d19, 0x1102, "?", 	       "Dexatek DK DVB-T Dongle (MSI DigiVox mini II V3.0)") 
idusb13 = Idusb(0x1d19, 0x1103, "FC2580",      "Dexatek Technology Ltd. DK 5217 DVB-T Dongle") 
idusb14 = Idusb(0x0458, 0x707f, "?", 	       "Genius TVGo DVB-T03 USB dongle (Ver. B)") 
idusb15 = Idusb(0x1b80, 0xd393, "FC0012",      "GIGABYTE GT-U7300") 
idusb16 = Idusb(0x1b80, 0xd394, "?", 	       "DIKOM USB-DVBT HD") 
idusb17 = Idusb(0x1b80, 0xd395, "FC0012",      "Peak 102569AGPK") 
idusb18 = Idusb(0x1b80, 0xd39d, "FC0012",      "SVEON STV20 DVB-T USB & FM")
idusb19 = Idusb(0x0bda, 0x2838, "FC0012",      "Realtek Semiconductor Corp. RTL2838 DVB-T")

def interrogeusb():

    interroge = usb.core.find(idVendor=idusb19.idvendeur, idProduct=idusb19.idproducteur)  
    if interroge is None:
        text1.delete("1.0","end")
        text1.insert(INSERT, "device non trouvé !", "\n")
     
    else:
        text1.delete("1.0","end")
        text1.insert(INSERT, "Device trouvé ! " + "\n" + str(idusb19.tunner) + "\n" + str(idusb19.devicename) + "\n")



#####################################################################
#            class    parametres par default                        #
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
    interrogeusb()
    startoutput = subprocess.Popen(args="rtl_fm -M "+ str(demodulation0) +" -f "+ str(frequence0.get()) +" -s "+ str(sample_rate0.get()) +" -p "+ str(ppm0.get()) + " | play -r 32k -t raw -e s -b 16 -c 1 -V1 -", 
    shell = True, text = True) 
    text0.delete("1.0","end")
    text0.insert(INSERT, "terminal:" "\n") 
    text0.insert(INSERT,"parametres utiliser: demodulation "+ str(demodulation0)+"\n")
    text0.insert(INSERT,"parametres utiliser: frequences   "+ str(frequence0.get())+"\n")
    text0.insert(INSERT,"parametres utiliser: samprate     "+ str(sample_rate0.get())+"\n")
    text0.insert(INSERT,"parametres utiliser: ppm          "+ str(ppm0.get())+"\n")

def restart(Event):
    start_rtl_fm(demodulation0[0], frequence0, sample_rate0, ppm0)
    time.sleep(1.5)
    
frequence0.bind("<ButtonRelease-1>", restart)
sample_rate0.bind("<ButtonRelease-1>", restart)
ppm0.bind("<ButtonRelease-1>", restart)



#    startoutput = subprocess.Popen(args="rtl_fm -M wbfm -f 100M -s 250000 -r 32k | play -r 32k -t raw -e s -b 16 -c 1 -V1 -", 
#    shell = True, text = True)    
    
   
# ajoute volume , mute




#################################
###      -  waterfall  -      ###
#################################



#################################
#  fenetreprincipale.mainloop() #
#################################

fenetreprincipale.mainloop()
