
#imports
import serial;
import glob;
import sys;
from Util import Util;
from threading import Thread;
from time import sleep;
from Decoder import Decode
import Locations;
import thread;

#-------
#Handles all communication to the serial interface
#-------
class Communication:
    
    #constructor
    def __init__(self):
        
        #initialize variables:
        
        self.util = Util(); #create a new Util class 
                                
        self.baud_rate = 4800; #initialize the baud rate to 4800 (the rate at which the GPS communicates)
        
        self.port = self.select_port(); #get the port from the user;
        
        self.ser = serial.Serial(); #create a new Serial object
        
        self.init_serial(); #initialize the serial communications
    
    #pulls data from the gps module
    def pull_data(self):
        
        #get the data, parse it to string and return
        data = str(self.ser.readline());  
        return data;
    
            
        
    #initializes the serial coms with the gps    
    def init_serial(self): 
        
        self.ser.timeout = 1; #set timeout to 1 second
        self.ser.baudrate = self.baud_rate; #set the baud rate
        self.ser.port = self.port; #set the port
                
        try:
            self.ser.open() #attempts to open the serial port
        except:
            print "A error has occured while attempting to connect to the gps\nTry a different port and check cables";
            return;
        
        if(self.ser.isOpen()):
            print "Serial port", self.port, "has been opened.\nNow communicating with gps...";
        
    #gives the user a prompt to select a port    
    def select_port(self): 
        
        ports = self.scan_ports(); #gets all available ports

        print "Please select the port the GPS is connected to.";
        
        #prints all available ports
        for i in range(len(ports)):
            print str(i) + ": " + ports[i];
            
        #get the user response
        result = self.util.number_qus("");
        
        #get the port corresponding to the index. try except employed incase of list index out of bound err
        try:
            return ports[result];
        except:
            print "That port does not exist!";
            return self.select_port(); #recall the function, returning its result
        
        
    
    def scan_ports(self): #return all ports that are open and ready to communicate
        
        ports = self.get_system_ports(); #get all ports open on the system
                
        result = []; #create a new list for the resultant ports
        
        #loop through possible ports
        for port in ports:
            
            try: #try-except for taken ports
                
                #get port and append its name to the result list
                s = serial.Serial(port)
                s.close()
                result.append(s.name)
                
            #if a error occurs when trying to call a port, just pass
            except (OSError, serial.SerialException):
                pass
        
        #return the result list
        return result;
    
    def get_system_ports(self): #gets all ports that a system may have (supports: Linux, Windows, Mac-osx)
        
        ports = []; #create new list to store ports
        
        system = sys.platform; #get system type
        
        if(system.startswith("win")): #for windows machines
            
            #loop through the 256 serial ports, appending each to the list
            for i in range(256):
                ports.append("COM" + str(i+1));
        
        elif(system.startswith("linux")): #for Linux machines
            
            #get all ports that are found under the /dev/tty prefix (i.e all Linux serial ports) 
            ports = glob.glob("/dev/tty[A-Za-z]*");
            
        elif(system.startswith("darwin")): #for Mac machines. (dont 
            
            #get all ports found under /dex/tty and /dec/cu prefix. Similar to linux because both OS's are based of unix
            ports = glob.glob("/dev/tty.*");
            ports = ports + glob.glob("/dev/cu.*");
            
        else: #handles unsupported operating systems
            print "Unsupported platform :/";
            sys.exit();
        
        return ports; #return the found ports

#print "here"
#c = Communication();    

#while True:
  #  print c.pull_data();
               
                