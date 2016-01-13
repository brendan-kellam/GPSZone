
#imports
import math;
import string;
import random;
import thread;
from time import sleep;

#------
#Holds a latitude/longitude location to allow for processing
#Also holds a radius to allow for a circle around the coordinate to be created
#------
class Location:
    
    #Constructor.
    #Accepts: a latitude, longitude and radius, all float values
    def __init__(self, frame, name, message, lat, long, radius, raw_location, dynamic):
        
        #initializations: 
        self.frame = frame;
        self.name = name;
        self.message = message;
        self.lat = lat;
        self.long = long;
        self.radius = radius; #Note: Radius is in Km units
        self.raw_location = raw_location;
        self.dynamic = dynamic;
        
        #the sleeping boolean indicates if the location is currently waiting to tweet again (only applies to dynamic locations)
        self.sleeping = False;
    
    #Equal function
    def __eq__(self, id):
        
        #returns if the two locations have the same id's (see __repr__)
        return self.id == id;
    
    #Represent function        
    def __repr__(self):
        
        #generate a new alpha-numerical id that allows for the user to access a location
        return self.generate_id();

    #generates a new alpha-numerical id for representation
    def generate_id(self):
        
        #length of 3 for all id's
        length = 3;
        
        #create a new null string that will hold the id
        self.id = "";
        
        #loop through the length of id
        for i in range(length):
            
            #generate a random case for either a letter or number (50/50 chance)
            type = random.randint(0, 1);
            
            #if the type is integer
            if(type == 0):
                
                #generate a random number between 0 and 9 and append to id
                self.id += str(random.randint(0, 9));
                
            #if the type is letter
            else:
                
                #get all ascii letters, randomly grab one and append to id
                letters = string.ascii_letters;
                index = random.randint(0, len(letters)-1);
                self.id += letters[index];
              
        #return the created id
        return self.id;
    
    #if the user has entered this location, this function will be called (see: Frame.update_gps)
    def within(self):

        #if the location is not dynamic
        if(not self.dynamic):
            
            #tweet the message and simply delete the location from the application
            self.frame.delete_location(self);
            self.frame.tweet(self.message);
            return;
        
        if(not self.sleeping):
            
            #tweet the message
            self.frame.tweet(self.message);
            
            #start the clock
            thread.start_new_thread(self.clock, ());
            
            self.sleeping = True;
    
    
    #(---!!!THIS FUNCTION IS CALLED IN SEPERATE THREAD!!!---)
    #handles all dynamic locations. #essentially is a clock counting up to final time to tweet again
    def clock(self):
        
        #grab the delay from the Frame class and convert to seconds
        delay = self.frame.delay*60*60;
        
        #sleep for alloted amount of time
        sleep(delay);
        
        #set sleeping to False and re-tweet
        self.sleeping = False;
    
            
    #compares this location to a latitude longitude point to see if said point is in the location  
    def is_within(self, lat, long):
        
        #get the distance by calling the haversine function
        distance = self.haversine(lat, long);
        
        #return a True or False statement dependent on if the distance is less or equal to the defined radius
        return distance <= self.radius;
        
    #the haversine function uses the Haversine formula to calculate the distance between two lat long points
    #has a effectiveness rate of within 0.2%
    #see: @link: http://www.movable-type.co.uk/scripts/latlong.html
    def haversine(self, lat, long):
        
        #Radius of the Earth (km)
        R = 6371.0;
                
        #pull the latitudes from location and point and convert from degrees to radians
        lat1 = math.radians(self.lat);
        lat2 = math.radians(lat);
        
        #calculate the change in latitude and change in longitude between the two given points
        delta_lat = math.radians(lat - self.lat)
        delta_long = math.radians(long - self.long);
        
        #initially calculate the square of half the cord length between the two points 
        a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + math.cos(lat1) * math.cos(lat2) * math.sin(delta_long/2) * math.sin(delta_long/2);
        
        #calculate the angular distance (in radians)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
        
        #calculate the final distance (in km)
        d = R * c;
        
        #return the calculated distance
        return d;
            
        