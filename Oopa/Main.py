
#imports:
import serial
import sys;
import math;
import Queue;
import Locations;
import Frame;
import Serial_Communication;
import threading;
from Decoder import Decode;
from time import sleep;
from Util import Util;
import thread;

#-------
#The Main module is the start for the GPS program
#Responsible for invoking the Frame class
#-------
class Main:
    
    
    #constructor
    def __init__(self):
        
        #create a new instance of frame
        frame = Frame.Frame();
    

#create a new instance of Main
Main();
