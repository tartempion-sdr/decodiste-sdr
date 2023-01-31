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
from cgitb import text
from select import select
from tkinter import *
import tkinter 
import subprocess
import time
import threading
import sys
from typing import Literal
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
text0.place(x=180, y=0, height=135, width=500)

#####################################################################
#            class    parametres par default                        #
#####################################################################

demodulation0 = ["wbfm", "wbfm", "fm" , "am", "lsb", "usb", "raw" ]
freq = int(94.2e6)

sample_rate = int(2400e2)
re_sample_rate = int(32000)
ppm0 = int(1)  #not 0 for spectrum

############
#   Menu   #
############

fenetreprincipalemenu = tkinter.Menu(fenetreprincipale)

premiermenu = tkinter.Menu(fenetreprincipalemenu, tearoff=0)
deuxiememenu = tkinter.Menu(fenetreprincipalemenu, tearoff=0)
troixiememenu = tkinter.Menu(fenetreprincipalemenu, tearoff=0)
quatriememenu = tkinter.Menu(fenetreprincipalemenu, tearoff=0)
cinquiememenu = tkinter.Menu(fenetreprincipalemenu, tearoff=0)

demodulationmenu = tkinter.Menu(premiermenu, tearoff=0)
frequencemenu = tkinter.Menu(premiermenu, tearoff=0)
ppmmenu = tkinter.Menu(premiermenu, tearoff=0)
sampleratemenu = tkinter.Menu(premiermenu, tearoff=0)
resampleratemenu = tkinter.Menu(premiermenu, tearoff=0)

devicemenu = tkinter.Menu(deuxiememenu, tearoff=0)
spectummenu = tkinter.Menu(troixiememenu, tearoff=0)
kernelmenu = tkinter.Menu(quatriememenu, tearoff=0)
infosmenu = tkinter.Menu(cinquiememenu, tearoff=0)


deuxiememenu.add_command(label="lancer la recherche usb...", command=lambda:interrogeusb())
troixiememenu.add_command(label="lancer le spectre", command=lambda:spectrum())

quatriememenu.add_command(label="debug", command=lambda:kernel_re())
cinquiememenu.add_command(label="dev tartempion-sdr")

fenetreprincipalemenu.add_cascade(label="paramètres", menu=premiermenu)

premiermenu.add_cascade(label="demodulation :", menu=demodulationmenu)


fenetreprincipalemenu.add_cascade(label="device ?", menu=deuxiememenu)
fenetreprincipalemenu.add_cascade(label="spectrum", menu=troixiememenu)
fenetreprincipalemenu.add_cascade(label="kernel debug", menu=quatriememenu)
fenetreprincipalemenu.add_cascade(label="infos", menu=cinquiememenu)


demoduleselect= IntVar()
demodulationmenu0 = demodulationmenu.add_radiobutton(label="wbfm", variable=demoduleselect, value=1, 
command=lambda:[change0demodulationwbfm(), wbfm0.select(),
stop_rtl_fm(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
## dedaut wbfm ##
demoduleselect.set(1)

demodulationmenu1 = demodulationmenu.add_radiobutton(label="fm", variable=demoduleselect, value=2, 
command= lambda:[change0demodulationfm(), fm0.select(), 
stop_rtl_fm(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])

demodulationmenu2 = demodulationmenu.add_radiobutton(label="am", variable=demoduleselect, value=3, 
command=lambda:[change0demodulationam(), am0.select(),
stop_rtl_fm(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])

demodulationmenu4 = demodulationmenu.add_radiobutton(label="lsb", variable=demoduleselect, value=4, 
command=lambda:[change0demodulationlsb(), lsb0.select(),
stop_rtl_fm(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])

demodulationmenu3 = demodulationmenu.add_radiobutton(label="usb", variable=demoduleselect, value=5, 
command=lambda:[change0demodulationusb(), usb0.select(),
stop_rtl_fm(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])

demodulationmenu5 = demodulationmenu.add_radiobutton(label="raw", variable=demoduleselect, value=6, 
command=lambda:[change0demodulationraw(), raw0.select(),
stop_rtl_fm(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])


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
            text0.delete("1.0","end")
            text0.insert(INSERT, "Liste de Devices interogés ... " + " |" + str(appareil.keysymbole) + str(appareil.keysymbolefin) + "|"
            +  "\n" 
            + " nombre de devices DVB-T interogé = " + str(appareils.index(appareil)+1) + "\n"  )
            
            text0.insert(INSERT,  " idvendeur = " + str(hex(appareil.idvendeur)) + "\n" 
                            + " idproducteur = " + str(hex(appareil.idproducteur)) + "\n"    
                            + " tunner = " + str(appareil.tunner) + "\n"  
                            + " device name = " + str(appareil.devicename) + "\n" 
                            + " Device DVB-T non trouvé ou incompatible" + "\n"  )           
            time.sleep(0.2)

        else:
            #nommé une variable == a appareil trouvé
            text0.delete("1.0","end")
            text0.insert(INSERT, "====-> Device trouvé !! <-====" + "\n" )            
            text0.insert(INSERT,  " idvendeur = " + str(hex(appareil.idvendeur)) + "\n"   
                            + " idproducteur = " + str(hex(appareil.idproducteur))+ "\n"    
                            + " tunner = " + str(appareil.tunner) + "\n"    
                            + " device name = " + str(appareil.devicename) + "\n" + "\n" )
                            
            
            break

#############################
####          pyaudio    ####
#############################
#print(sys.stdout.read)
#plt.specgram(A, NFFT=1024 )
#plt.title('Spectrogram rtlsdr')  
#plt.show()

#################################
###      -  waterfall  -      ###
#################################
############
# spectrum #
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




#######################################################################
# bouton  demodulation0 = ["wbfm", "fm" , "am", "lsb", "usb", "raw" ] #
#######################################################################


wbfm0 =  Radiobutton(fenetreprincipale, indicatoron=False, value=0, variable=0, command=lambda: 
[change0demodulationwbfm(), demoduleselect.set(1),
stop_rtl_fm(),
start_rtl_fm(demodulation0[1], frequence0, sample_rate0, re_sample_rate0, ppm1)], text="wbfm", activebackground='green', background='purple')
wbfm0.place(x=0, y=30, width=60, height=35)
# wbfm0.select() met le radiobutton wfm0 actif par defaut en blanc ###
wbfm0.select()

fm0 = Radiobutton(fenetreprincipale, indicatoron=False, value=1, variable=0, command=lambda: 
[change0demodulationfm(), demoduleselect.set(2),
stop_rtl_fm(),
start_rtl_fm(demodulation0[2], frequence0, sample_rate0, re_sample_rate0, ppm1)], text="fm", activebackground='green', background='purple')
fm0.place(x=60, y=30, width=60, height=35)


am0 = Radiobutton(fenetreprincipale, indicatoron=False, value=2, variable=0, command=lambda: 
[change0demodulationam(), demoduleselect.set(3),
stop_rtl_fm(), 
start_rtl_fm(demodulation0[3], frequence0, sample_rate0, re_sample_rate0, ppm1)], text="am  ", activebackground='green', background='purple')
am0.place(x=120, y=30, width=60, height=35)


lsb0 = Radiobutton(fenetreprincipale, indicatoron=False, value=3, variable=0, command=lambda:  
[change0demodulationlsb(), demoduleselect.set(4),
stop_rtl_fm(), 
start_rtl_fm(demodulation0[4], frequence0, sample_rate0, re_sample_rate0, ppm1)], text="lsb ", activebackground='green', background='purple')
lsb0.place(x=0, y=60, width=60, height=35)

usb0 = Radiobutton(fenetreprincipale, indicatoron=False, value=4, variable=0, command=lambda: 
[change0demodulationusb(), demoduleselect.set(5),
stop_rtl_fm(), 
start_rtl_fm(demodulation0[5], frequence0, sample_rate0, re_sample_rate0, ppm1)], text="usb ", activebackground='green', background='purple')
usb0.place(x=60, y=60, width=60, height=35)

raw0 = Radiobutton(fenetreprincipale, indicatoron=False, value=5, variable=0, command=lambda:  
[change0demodulationraw(), demoduleselect.set(6),
stop_rtl_fm(),
start_rtl_fm(demodulation0[6], frequence0, sample_rate0, re_sample_rate0, ppm1)], text="raw ", activebackground='green', background='purple')
raw0.place(x=120, y=60, width=60, height=35)




###################################################
# bouton scale + ajust frequence, ppm, sample_rate #
###################################################


frequence0 = Scale(fenetreprincipale, label="frequence", 
from_=22000000, to=900000000, resolution=1, orient=HORIZONTAL, activebackground="yellow", 
background="green")
frequence0.set(freq)
frequence0.place(x=0, y=195, width=500 , height=60)


   



freqplus1 =  Button(fenetreprincipale, text="freq +1", activebackground='green', background='red', 
command=lambda: [freqplusvar1(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus1.place(x=0, y=135, width=60, height=30  )

def freqplusvar1():
    global freq
    freq += 1
    frequence0.set(freq)
    

freqplus2 =  Button(fenetreprincipale, text="+10", activebackground='green', background='red',
command=lambda: [freqplusvar2(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus2.place(x=60, y=135, width=30, height=30)

def freqplusvar2():
    global freq
    freq += 10
    frequence0.set(freq)
    

freqplus3 =  Button(fenetreprincipale, text="+100", activebackground='green', background='red',
command=lambda: [freqplusvar3(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus3.place(x=90, y=135, width=40, height=30)

def freqplusvar3():
    global freq
    freq += 100
    frequence0.set(freq)
    

freqplus4 =  Button(fenetreprincipale, text="+1 000", activebackground='green', background='red',
command=lambda: [freqplusvar4(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus4.place(x=130, y=135, width=55, height=30)

def freqplusvar4():
    global freq
    freq += 1000
    frequence0.set(freq)
    
freqplus5 =  Button(fenetreprincipale, text="+10 000", activebackground='green', background='red',
command=lambda: [freqplusvar5(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus5.place(x=185, y=135, width=65, height=30)

def freqplusvar5():
    global freq
    freq += 10000
    frequence0.set(freq)
    

freqplus6 =  Button(fenetreprincipale, text="+100 000", activebackground='green', background='red',
command=lambda: [freqplusvar6(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus6.place(x=250, y=135, width=70, height=30)

def freqplusvar6():
    global freq
    freq += 100000
    frequence0.set(freq)


freqplus7 =  Button(fenetreprincipale, text="+1 000 000", activebackground='green', background='red',
command=lambda: [freqplusvar7(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqplus7.place(x=320, y=135, width=80, height=30)

def freqplusvar7():
    global freq
    freq += 1000000
    frequence0.set(freq)
    



freqmoins1 =  Button(fenetreprincipale, text="freq -1", activebackground='green', background='blue',
command=lambda: [freqmoinsvar1(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins1.place(x=0, y=165, width=60, height=30)

def freqmoinsvar1():
    global freq
    freq -= 1
    frequence0.set(freq)


freqmoins2 =  Button(fenetreprincipale, text="-10", activebackground='green', background='blue',
command=lambda: [freqmoinsvar2(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins2.place(x=60, y=165, width=30, height=30)

def freqmoinsvar2():
    global freq
    freq -= 10
    frequence0.set(freq)


freqmoins3 =  Button(fenetreprincipale, text="-100", activebackground='green', background='blue',
command=lambda: [freqmoinsvar3(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins3.place(x=90, y=165, width=40, height=30)

def freqmoinsvar3():
    global freq
    freq -= 100
    frequence0.set(freq)


freqmoins4 =  Button(fenetreprincipale, text="-1 000", activebackground='green', background='blue',
command=lambda: [freqmoinsvar4(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins4.place(x=130, y=165, width=55, height=30)

def freqmoinsvar4():
    global freq
    freq -= 1000
    frequence0.set(freq)


freqmoins5 =  Button(fenetreprincipale, text="-10 000", activebackground='green', background='blue',
command=lambda: [freqmoinsvar5(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins5.place(x=185, y=165, width=65, height=30)

def freqmoinsvar5():
    global freq
    freq -= 10000
    frequence0.set(freq)

freqmoins6 =  Button(fenetreprincipale, text="-100 000", activebackground='green', background='blue',
command=lambda: [freqmoinsvar6(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins6.place(x=250, y=165, width=70, height=30)

def freqmoinsvar6():
    global freq
    freq -= 100000
    frequence0.set(freq)


freqmoins7 =  Button(fenetreprincipale, text="-1 000 000", activebackground='green', background='blue',
command=lambda: [freqmoinsvar7(), start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1)])
freqmoins7.place(x=320, y=165, width=80, height=30)

def freqmoinsvar7():
    global freq
    freq -= 1000000
    frequence0.set(freq)
    

# samplerate

sample_rate0 = Scale(fenetreprincipale, label="sample_rate", 
from_=0, to=3000000, length=750, orient=HORIZONTAL, activebackground="yellow", background="green")
sample_rate0.set(sample_rate)
sample_rate0.place(x=0, y=255, width=500 , height=60)


re_sample_rate0 = Scale(fenetreprincipale, label="re_sample_rate", 
from_=0, to=44100, length=750, orient=HORIZONTAL, activebackground="yellow", background="green")
re_sample_rate0.set(re_sample_rate)
re_sample_rate0.place(x=0, y=315, width=500 , height=60)


ppm1 = Scale(fenetreprincipale, label="ppm",  
from_=-200, to=200, orient=HORIZONTAL, activebackground="yellow", background="green")
ppm1.set(ppm0)
ppm1.place(x=0, y=375, width=500 , height=60)



    
    




#######################################
#       boutons: start et stop        #
#######################################




start = Button(fenetreprincipale, text='start', activebackground='blue', 
command=lambda: 
start_rtl_fm(demodulation0[0], frequence0, sample_rate0, re_sample_rate0, ppm1))
start.place(x=0, y=0)

stop = Button(fenetreprincipale, text='stop', activebackground='red', 
command=lambda: stop_rtl_fm())
stop.place(x=58, y=0)

kernel = Button(fenetreprincipale, text='kernel', activebackground='red', 
command=lambda:  kernel_re(), padx=8)
kernel.place(x=115, y=0)


devices = Button(fenetreprincipale, text='devices', activebackground='red', 
command=lambda:  thread1_start())
devices.place(x=70, y=95)

spectre = Button(fenetreprincipale, text='spectre', activebackground='red', 
command=lambda:  spectrum() )
spectre.place(x=0, y=95)





    
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
    text0.delete("1.0","end")
    text0.insert(INSERT, "terminal:" "\n") 
    text0.insert(INSERT,"parametres utiliser: demodulation "+ str(demodulation0[0])+"\n")
    text0.insert(INSERT,"parametres utiliser: frequences   "+ str(frequence0.get())+"\n")
    text0.insert(INSERT,"parametres utiliser: sample-rate     "+ str(sample_rate0.get())+"\n")
    text0.insert(INSERT,"parametres utiliser: re-sample-rate     "+ str(re_sample_rate0.get())+"\n")
    text0.insert(INSERT,"parametres utiliser: ppm          "+ str(ppm1.get())+"\n")
    


#################################
#  fenetreprincipale.mainloop() #
#################################

fenetreprincipale.config(menu=fenetreprincipalemenu)
fenetreprincipale.mainloop()

