#########################
# -*- coding: utf-8 -*- #
#   <- python 3.8.1 ->  #    

""" long commentaire

alt gr + 7 pour: ```

```python
discord
discord```

help(pyaudio)

pip install pyrtlsdr
pip install pyusb
"""

#########################
#< ! DOCTYPE python>    #
#########################
#  interface - sdr - 2  #
#########################

from cProfile import label
import tkinter.font as tkFont
from ctypes.wintypes import SIZE
from distutils import command
from tkinter import *
import tkinter 
import subprocess
import time
import threading
import sys
import rtlsdr
from rtlsdr import rtlsdraio


import usb.core
import usb.util
import usb.control

from rtlsdr import *
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pyaudio

######################
# titre du programme #
######################

fenetreprincipale = tkinter.Tk()
fenetreprincipale.title('decodiste-sdr-beta-JAN-2022')

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
#  texte #
############


text0 = Text(fenetreprincipale, border= 4 )
text0.place(x=0, y=0, height=115, width=125)

    
text0.insert(INSERT,"demodulation:"+"\n")
text0.insert(INSERT,"frequences:"+"\n")
text0.insert(INSERT,"ppm:"+"\n")
text0.insert(INSERT,"sample-rate:"+"\n")
text0.insert(INSERT,"resample-rate:"+"\n")

    

text1 = Text(fenetreprincipale, border= 4 )
text1.place(x=125, y=0, height=115, width=100)

text2 = Text(fenetreprincipale, border= 4 )
text2.place(x=225, y=0, height=115, width=510)

text3 = Text(fenetreprincipale, border= 4 )
text3.configure(font=("Times New Roman", 20))
text3.place(x=0, y=200, height=50, width=225)


############
#   Menu   #
############

fenetreprincipalemenu = tkinter.Menu(fenetreprincipale)

startmenu        = tkinter.Menu(fenetreprincipalemenu)
stopmenu         = tkinter.Menu(fenetreprincipalemenu)
devicemenu       = tkinter.Menu(fenetreprincipalemenu)
spectummenu      = tkinter.Menu(fenetreprincipalemenu)

parametresmenu    = tkinter.Menu(fenetreprincipalemenu)

demodulationmenu = tkinter.Menu(parametresmenu)
frequencemenu    = tkinter.Menu(parametresmenu)
ppmmenu          = tkinter.Menu(parametresmenu)
sampleratemenu   = tkinter.Menu(parametresmenu)
resampleratemenu = tkinter.Menu(parametresmenu)

cartesonmenu     = tkinter.Menu(fenetreprincipalemenu)
kernelmenu       = tkinter.Menu(fenetreprincipalemenu)
infosmenu        = tkinter.Menu(fenetreprincipalemenu)



fenetreprincipalemenu.add_command(label="start", command=lambda:start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1))
fenetreprincipalemenu.add_command(label="stop", command=lambda:stop_rtl_fm())
fenetreprincipalemenu.add_command(label="device ?", command=lambda:thread1_start())
fenetreprincipalemenu.add_command(label="lancer le spectre", command=lambda:spectrum())

fenetreprincipalemenu.add_cascade(label="paramètres", menu=parametresmenu)

parametresmenu.add_cascade(label="demodulation", menu=demodulationmenu)
parametresmenu.add_cascade(label="frequence", menu=frequencemenu)
parametresmenu.add_cascade(label="ppm", menu=ppmmenu)
parametresmenu.add_cascade(label="samplerate", menu=sampleratemenu)
parametresmenu.add_cascade(label="re-samplerate", menu=resampleratemenu)



demodulationmenu.add_radiobutton(label="wbfm", command=lambda:[change0demodulationwbfm(),
stop_rtl_fm(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
demodulationmenu.add_radiobutton(label="fm", command=lambda:[change0demodulationfm(),
stop_rtl_fm(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
demodulationmenu.add_radiobutton(label="am", command=lambda:[change0demodulationam(),
stop_rtl_fm(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
demodulationmenu.add_radiobutton(label="usb", command=lambda:[change0demodulationusb(),
stop_rtl_fm(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
demodulationmenu.add_radiobutton(label="lsb", command=lambda:[change0demodulationlsb(),
stop_rtl_fm(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
demodulationmenu.add_radiobutton(label="raw", command=lambda:[change0demodulationraw(),
stop_rtl_fm(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
frequencemenu.add_command(label="fréquence")
ppmmenu.add_command(label="ppm")
sampleratemenu.add_command(label="sample-rate")
resampleratemenu.add_command(label="re-sample-rate")


fenetreprincipalemenu.add_command(label="carte-son")
fenetreprincipalemenu.add_command(label="debug", command=lambda:kernel_re())
fenetreprincipalemenu.add_command(label="dev tartempion-sdr")






#####################################################################
#            class    parametres par default                        #
#####################################################################

demodulation0 = ["wbfm", "wbfm", "fm" , "am", "lsb", "usb", "raw" ]
freq = int(94.2e6)
sample_rate = int(2400e2)
re_sample_rate = int(32000)
ppm0 = int(1)  #not 0 for spectrum

#################################################
# class Appareilusb: le device est il present ? #
################################################# 

class AppareilUsb:
   
#class des idvendeur et idproducteur
       
    def __init__(self, id_vendeur, id_producteur, _tunner, device_name, key_symbole, key_symbolefin):        

        self.idvendeur = id_vendeur
        self.idproducteur = id_producteur
        self.tunner =_tunner
        self.devicename = device_name
        self.keysymbole = key_symbole
        self.keysymbolefin = key_symbolefin

idusb01 = AppareilUsb(0x0bda, 0x2832, "all of them",      "Generic RTL2832U (e.g. hama nano)", "#", "\-------------------")
idusb02 = AppareilUsb(0x0ccd, 0x00a9, "FC0012",           "Terratec Cinergy T Stick Black (rev 1)", "##", "/------------------") 
idusb03 = AppareilUsb(0x0ccd, 0x00b3, "FC0013", 	      "Terratec NOXON DAB/DAB+ USB dongle (rev 1)", "###", "\-----------------") 
idusb04 = AppareilUsb(0x0ccd, 0x00d3, "E4000", 	          "Terratec Cinergy T Stick RC (Rev.3)", "####", "/----------------") 
idusb05 = AppareilUsb(0x0ccd, 0x00e0, "E4000", 	          "Terratec NOXON DAB/DAB+ USB dongle (rev 2)", "#####", "\---------------") 
idusb06 = AppareilUsb(0x185b, 0x0620, "E4000",             "Compro Videomate U620F", "######", "/--------------") 
idusb07 = AppareilUsb(0x185b, 0x0650, "E4000",	           "Compro Videomate U650F", "#######", "\-------------") 
idusb08 = AppareilUsb(0x1f4d, 0xb803, "FC0012", 	       "GTek T803", "########", "/------------") 
idusb09 = AppareilUsb(0x1f4d, 0xc803, "FC0012", 	       "Lifeview LV5TDeluxe", "#########", "\-----------") 
idusb10 = AppareilUsb(0x1b80, 0xd3a4, "FC0013", 	       "Twintech UT-40", "##########", "/----------") 
idusb11 = AppareilUsb(0x1d19, 0x1101, "FC2580",            "Dexatek DK DVB-T Dongle (Logilink VG0002A)", "###########", "\---------") 
idusb12 = AppareilUsb(0x1d19, 0x1102, "?", 	               "Dexatek DK DVB-T Dongle (MSI DigiVox mini II V3.0)", "############", "/--------") 
idusb13 = AppareilUsb(0x1d19, 0x1103, "FC2580",            "Dexatek Technology Ltd. DK 5217 DVB-T Dongle", "#############", "\-------") 
idusb14 = AppareilUsb(0x0458, 0x707f, "?", 	               "Genius TVGo DVB-T03 USB dongle (Ver. B)", "##############", "/------") 
idusb15 = AppareilUsb(0x1b80, 0xd393, "FC0012",            "GIGABYTE GT-U7300", "###############", "\-----") 
idusb16 = AppareilUsb(0x1b80, 0xd394, "?", 	               "DIKOM USB-DVBT HD", "################", "/----") 
idusb17 = AppareilUsb(0x1b80, 0xd395, "FC0012",            "Peak 102569AGPK", "#################", "\---") 
idusb18 = AppareilUsb(0x1b80, 0xd39d, "FC0012",            "SVEON STV20 DVB-T USB & FM", "##################", "/--")
idusb19 = AppareilUsb(0x0bda, 0x2838, "FC0012 ou E4000",   "Realtek Semiconductor Corp. RTL2838 DVB-T" + "\n" "               ou ezcap USB 2.0 DVB-T/DAB/FM dongle", "###################", "\-")
idusb20 = AppareilUsb(0x0bda, 0x2838, "E4000 ou FC0012",   "ezcap USB 2.0 DVB-T/DAB/FM dongle" + "\n" "               ou Realtek Semiconductor Corp. RTL2838 DVB-T", "####################", "/") 
idusb21 = AppareilUsb(0x0000, 0x0000, "introuvable",       "introuvable", "#####################", "") 

appareils = [
    idusb01,
    idusb02,
    idusb03,
    idusb04,
    idusb05,
    idusb06,
    idusb07,
    idusb08,
    idusb09,
    idusb10,
    idusb11,
    idusb12,
    idusb13,
    idusb14,
    idusb15,
    idusb16,
    idusb17,
    idusb18,
    idusb19,
    idusb20,
    idusb21]



def interrogeusb():
    for appareil in appareils: 
        interroge = usb.core.find(idVendor=appareil.idvendeur, idProduct=appareil.idproducteur)
        if interroge is None:
            text2.delete("1.0","end")
            text2.insert(INSERT, " nombre de devices DVB-T interogé = " + str(appareils.index(appareil)+1) + " |" + str(appareil.keysymbole) + str(appareil.keysymbolefin) + "|"
            +  "\n" )
            
            text2.insert(INSERT,  " idvendeur = " + str(hex(appareil.idvendeur)) + "\n" 
                            + " idproducteur = " + str(hex(appareil.idproducteur)) + "\n"    
                            + " tunner = " + str(appareil.tunner) + "\n"  
                            + " device name = " + str(appareil.devicename) + "\n" 
                            + " Device DVB-T non trouvé ou incompatible" + "\n"  )           
            time.sleep(0.2)

        else:
            #nommé une variable == a appareil trouvé
            text2.delete("1.0","end")
            text2.insert(INSERT, "====-> Device trouvé !! <-====" + "\n" )            
            text2.insert(INSERT,  " idvendeur = " + str(hex(appareil.idvendeur)) + "\n"   
                            + " idproducteur = " + str(hex(appareil.idproducteur))+ "\n"    
                            + " tunner = " + str(appareil.tunner) + "\n"    
                            + " device name = " + str(appareil.devicename) + "\n" + "\n" )
                            
            
            break

#############################
####          pyaudio    ####
#############################
#print(sys.stdout.read)
############

def spectrum():
    
        
        sdr = RtlSdr()
    
        # configure device
        sdr.sample_rate = sample_rate0.get()*10  # Hz
        sdr.center_freq = frequence0.get()  # Hz
        sdr.freq_correction = ppm0  # PPM
        sdr.gain = 'auto'

        fig = plt.figure()
        
        graph_out = fig.add_subplot(1, 1, 1)

        def animate(i):
            graph_out.clear()
            #samples = sdr.read_samples(256*1024)
            samples = sdr.read_samples(4*16384)
            # use matplotlib to estimate and plot the PSD
            graph_out.psd(samples, NFFT=1024, Fs=sdr.sample_rate /
            1e6, Fc=sdr.center_freq/1e6)
            #graph_out.xlabel('Frequency (MHz)')
            #graph_out.ylabel('Relative power (dB)')


        try:
            ani = animation.FuncAnimation(fig, animate, interval=10)
            plt.show()
        except KeyboardInterrupt:
            pass
        finally:
            sdr.close() 


###################
#  kernel detach  #
###################

def kernel_re():
    dev1 = usb.core.find(idVendor=0x0bda, idProduct=0x2838)
    if dev1.is_kernel_driver_active(0) is not None:
        print ("dev 1 is not none")
        dev1.reset()
        dev1.detach_kernel_driver(interface=0) 
        print("detache usb")
        


##################
#  threading  1   #
##################
thread1 = threading.Thread(target=interrogeusb)    

    
def thread1_start():
    thread1.start()




###################################################
# bouton scale + ajust frequence, ppm, sample_rate #
###################################################



frequence0 = Scale(fenetreprincipale, 
from_=22000000, to=900000000, resolution=1, orient=HORIZONTAL, activebackground="yellow", 
background="green")

frequence0.set(freq)
frequence0.place(x=0, y=115, width=225 , height=60)


freqplus1 =  Button(fenetreprincipale, text="+", activebackground='green', background='red', 
command=lambda: [freqplusvar1(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus1.place(x=0, y=175, width=25, height=25  )

def freqplusvar1():
    global freq
    freq += 1
    frequence0.set(freq)
    

freqplus2 =  Button(fenetreprincipale, text="+", activebackground='green', background='red',
command=lambda: [freqplusvar2(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus2.place(x=25, y=175, width=25, height=25)

def freqplusvar2():
    global freq
    freq += 10
    frequence0.set(freq)
    

freqplus3 =  Button(fenetreprincipale, text="+", activebackground='green', background='red',
command=lambda: [freqplusvar3(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus3.place(x=50, y=175, width=25, height=25)

def freqplusvar3():
    global freq
    freq += 100
    frequence0.set(freq)
    

freqplus4 =  Button(fenetreprincipale, text="+", activebackground='green', background='red',
command=lambda: [freqplusvar4(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus4.place(x=75, y=175, width=25, height=25)

def freqplusvar4():
    global freq
    freq += 1000
    frequence0.set(freq)
    
freqplus5 =  Button(fenetreprincipale, text="+", activebackground='green', background='red',
command=lambda: [freqplusvar5(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus5.place(x=100, y=175, width=25, height=25)

def freqplusvar5():
    global freq
    freq += 10000
    frequence0.set(freq)
    

freqplus6 =  Button(fenetreprincipale, text="+", activebackground='green', background='red',
command=lambda: [freqplusvar6(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus6.place(x=125, y=175, width=25, height=25)

def freqplusvar6():
    global freq
    freq += 100000
    frequence0.set(freq)


freqplus7 =  Button(fenetreprincipale, text="+", activebackground='green', background='red',
command=lambda: [freqplusvar7(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus7.place(x=150, y=175, width=25, height=25)

def freqplusvar7():
    global freq
    freq += 1000000
    frequence0.set(freq)
    

freqplus8 =  Button(fenetreprincipale, text="+", activebackground='green', background='red',
command=lambda: [freqplusvar8(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus8.place(x=175, y=175, width=25, height=25)

def freqplusvar8():
    global freq
    freq += 10000000
    frequence0.set(freq)
    
freqplus9 =  Button(fenetreprincipale, text="+", activebackground='green', background='red',
command=lambda: [freqplusvar9(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus9.place(x=200, y=175, width=25, height=25)

def freqplusvar9():
    global freq
    freq += 100000000
    frequence0.set(freq)




freqmoins1 =  Button(fenetreprincipale, text="-", activebackground='green', background='blue',
command=lambda: [freqmoinsvar1(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins1.place(x=0, y=250, width=25, height=25)

def freqmoinsvar1():
    global freq
    freq -= 1
    frequence0.set(freq)


freqmoins2 =  Button(fenetreprincipale, text="-", activebackground='green', background='blue',
command=lambda: [freqmoinsvar2(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins2.place(x=25, y=250, width=25, height=25)

def freqmoinsvar2():
    global freq
    freq -= 10
    frequence0.set(freq)


freqmoins3 =  Button(fenetreprincipale, text="-", activebackground='green', background='blue',
command=lambda: [freqmoinsvar3(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins3.place(x=50, y=250, width=25, height=25)

def freqmoinsvar3():
    global freq
    freq -= 100
    frequence0.set(freq)


freqmoins4 =  Button(fenetreprincipale, text="-", activebackground='green', background='blue',
command=lambda: [freqmoinsvar4(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins4.place(x=75, y=250, width=25, height=25)

def freqmoinsvar4():
    global freq
    freq -= 1000
    frequence0.set(freq)


freqmoins5 =  Button(fenetreprincipale, text="-", activebackground='green', background='blue',
command=lambda: [freqmoinsvar5(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins5.place(x=100, y=250, width=25, height=25)

def freqmoinsvar5():
    global freq
    freq -= 10000
    frequence0.set(freq)

freqmoins6 =  Button(fenetreprincipale, text="-", activebackground='green', background='blue',
command=lambda: [freqmoinsvar6(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins6.place(x=125, y=250, width=25, height=25)

def freqmoinsvar6():
    global freq
    freq -= 100000
    frequence0.set(freq)


freqmoins7 =  Button(fenetreprincipale, text="-", activebackground='green', background='blue',
command=lambda: [freqmoinsvar7(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins7.place(x=150, y=250, width=25, height=25)

def freqmoinsvar7():
    global freq
    freq -= 1000000
    frequence0.set(freq)
    

freqmoins8 =  Button(fenetreprincipale, text="-", activebackground='green', background='blue',
command=lambda: [freqmoinsvar8(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins8.place(x=175, y=250, width=25, height=25)

def freqmoinsvar8():
    global freq
    freq -= 10000000
    frequence0.set(freq)

freqmoins9 =  Button(fenetreprincipale, text="-", activebackground='green', background='blue',
command=lambda: [freqmoinsvar9(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins9.place(x=200, y=250, width=25, height=25)

def freqmoinsvar9():
    global freq
    freq -= 100000000
    frequence0.set(freq)
















#samplerate

sample_rate0 = Scale(fenetreprincipale, label="sample_rate", 
from_=0, to=3000000, length=750, orient=HORIZONTAL, activebackground="yellow", background="green")
sample_rate0.set(sample_rate)
sample_rate0.place(x=0, y=275, width=225 , height=60)


re_sample_rate0 = Scale(fenetreprincipale, label="re_sample_rate", 
from_=0, to=44100, length=750, orient=HORIZONTAL, activebackground="yellow", background="green")
re_sample_rate0.set(re_sample_rate)
re_sample_rate0.place(x=0, y=335, width=225 , height=60)


ppm1 = Scale(fenetreprincipale, label="ppm",  
from_=-200, to=200, orient=HORIZONTAL, activebackground="yellow", background="green")
ppm1.set(ppm0)
ppm1.place(x=0, y=395, width=225 , height=60)

    
############
# fonction #
############


               


def stop_rtl_fm():  
    stopoutput = subprocess.run(args="killall rtl_fm", 
    capture_output=True, shell = True, text = True)
    time.sleep(1.5)
    

   
def start_rtl_fm(demodulation0, frequence0, sample_rate0, re_sample_rate0, ppm1 ): 
    stop_rtl_fm()
    sdr1 = subprocess.Popen(args="rtl_fm -M "+ str(demodulation0) +" -f "+ str(frequence0.get()) +" -s "+ str(sample_rate0.get()) +" -r " + str(re_sample_rate0.get()) +" -p "+ str(ppm1.get()) + " - " + "| play -r 32k -t raw -e s -b 16 -c 1  -V1 - " 
    , shell = True, stdout=subprocess.PIPE, universal_newlines=True)
    affiche_variable()    
    
     
def restart(Event):
    
    start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)
    time.sleep(1.5)
    
frequence0.bind("<ButtonRelease-1>", restart)
sample_rate0.bind("<ButtonRelease-1>", restart)
re_sample_rate0.bind("<ButtonRelease-1>", restart)
ppm1.bind("<ButtonRelease-1>", restart)

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



def affiche_variable():
    text1.delete("1.0","end")
    text3.delete("1.0","end")
    text1.insert(INSERT, str("{:>11}".format( demodulation0[0]))+"\n")
    text1.insert(INSERT, str("{:>11}".format(frequence0.get()))+"\n")
    text3.insert(INSERT, str(frequence0.get()) + " Htz" + "\n")
    text1.insert(INSERT, str("{:>11}".format(ppm1.get()))+"\n")
    text1.insert(INSERT, str("{:>11}".format(sample_rate0.get()))+"\n")
    text1.insert(INSERT, str("{:>11}".format(re_sample_rate0.get()))+"\n")
    

affiche_variable()

#################################
#  fenetreprincipale.mainloop() #
#################################

fenetreprincipale.config(menu=fenetreprincipalemenu)
fenetreprincipale.mainloop()


