
#imports
import math;

#-------
#The decoder module contains the decode class
#decode is responsible of taking the GPS NMEA 0183 protocol and parsing it into a understood format
#-------

class Decode:
    
    #constructor
    def __init__(self):
        
        #initialize variables:
                
        self.GGA = "GGA"; #String representation of the header for Global Positioning System Fixed Data
        
        self.identifiers = {self.GGA : self.decode_GGA}; #A dictionary of all sentence identifiers implemented
        
        self.lat = 0;
        self.long = 0;
        
    
    def NMEA_0183(self, message):
        
        self.message = message; #assign a class scope on message 
        
        identifier = message[3:6]; #get the sentence identifier by parsing from the message. (see: datasheet for NMEA 0183 structure)
        
        #try except needed for unsupported sentence identifiers
        try:
            
            #call the identifiers function
            return self.identifiers[identifier]();
        except:
            pass #just continue with program
        
        
    def get_direction(self, dir): #converts the direction to negative/positive relations. (use for representing coordinates)
        
        if(dir == "S" or dir == "W"): #return -1 if South or West
            return -1.0;
        
        return 1.0; #return 1 if North or East


    def decode_GGA(self): #decode GPS data when identifier is GGA (Global Positioning System)
        
        data = self.message.split(","); #get the data from the String by splitting at all commas
            
        validation = int(data[6]); #get the Position Fix Indicator (essentially tells if the gps has a good signal. [1 is good] )
              
        if(validation != 1): #if the validation if not 1, then stop decoding
            return;
        
        
        #Get the latitude and longitude
        #----IN Degree, Minute.Minute FORMAT----       
        lat = float(data[2]);
        long = float(data[4]);
        
        
        #convert the latitude, longitude coordinates to Decimal-degree format and apply the direction offsets (see: self.get_direction)
        lat = self.convert_DM_to_degrees(lat) * self.get_direction(data[3]);
        long = self.convert_DM_to_degrees(long) * self.get_direction(data[5]);
        
        return lat, long;
      
        
    def convert_DM_to_degrees(self, DM): #converts from decimal-minutes to degrees using the formula: d = D + m/60
        
        #convert the decimal-minute data to a string
        data = str(DM);
               
        #set the offset of where the initial degree data is found 
        offset = 2;
        
        #if the Coordinate point is negative (W/S), add one to offset to acount for "-" symbol
        if("-" in data):
            offset+=1;
        
        #parse the string to determine the Degree and Minute values
        D = float(data[:offset]);
        M = float(data[offset:]);
       
        #return the decimal-degree representation of the inputed decimal-minute value     
        return float(D + M/60);
    
    #takes a google maps link and pulls latitude and longitude information
    def decode_maps_data(self, data): 
        
        #if the main header is not present in the data, return
        if("https://www.google.com/maps/dir//" not in data):
            return;
        
        #replace the front and end of the url
        data = data.replace("https://www.google.com/maps/dir//", "");
        data = data.split("/", 1)[0];
        
        #return a tuple of the latitude and longitude
        return tuple(data.split(","));
        