#imports
import xml.etree.ElementTree as et;
from xml.etree.ElementTree import Element, SubElement
from Locations import Location;

#-------
#The XML Class handles all translation from and to the main.xml file
#note: no comments are found in xml due to, well, python deleting them!!
#-------
class XML:
 
    
    #constructor
    def __init__(self):
        
        #set the main path of the xml
        self.xml_path = "res/main.xml";
        
        #instantiate the tree and root objects
        self.tree = et.parse(self.xml_path);
        self.root = self.tree.getroot();
        
        #get the locations child, allowing for appending a new location
        for l in self.root.iter("locations"):
            self.locations = l;
            
            
    #get the username of the twitter account for the user      
    def twitter_user(self):
        
        #pulls and returns the text found at the "twitter" element
        twitter = self.root.find("twitter");
        return twitter.text;
    
    
    #edit the users twitter username
    def edit_twitter_user(self, user):
    
        #gets the twitter element
        twitter = self.root.find("twitter");
        
        #re-assign the user name to the parameter
        twitter.text = user;
        
        #Write to the document
        self.tree.write(self.xml_path);
        
    #return the dynamic delay time
    def get_delay(self):
        
        #pulls and return the text found at the "delay" element
        delay = self.root.find("delay");
        return float(delay.text);
    
    #edit the delay set
    def edit_delay(self, period):
        
        #get the delay element
        delay = self.root.find("delay");
        
        #re-assign the delay to the provided period time
        delay.text = str(period);
        
        #write to the document
        self.tree.write(self.xml_path);
        
    #write a new location to the xml document
    def write_location(self, location):
        
        #pull the data from the location
        name = location.name;
        message = location.message;
        lat = str(location.lat);
        long = str(location.long);
        radius = str(location.radius);
        raw_location = location.raw_location;
        dynamic = str(location.dynamic);
        
        #Create a new Element with the given location information
        location = SubElement(self.locations, "location", {"name":name, "lat":lat, "long":long, "radius":radius, "raw_location":raw_location, "dynamic":dynamic});
        
        #set the main text to the message
        location.text = message;
        
        #Write the added Element to the document
        self.tree.write(self.xml_path);
    
    
    #converts a string to a boolean
    def str_to_bool(self, str):
        #if the string is "True" then return True, else False
        return str == "True";
    
    #pulls all cached locations from the xml file. (Used: Frame.run())
    def read_locations(self, frame):    
        
        locations = [];
        
        #loop through all locations
        for location in self.locations.findall("location"):
            
            #pull all information from each given location element and apply conversions where applicable
            name = location.get("name");
            message = location.text;
            lat = float(location.get("lat"));
            long = float(location.get("long"));
            radius = float(location.get("radius"));
            raw_location = location.get("raw_location");
            dynamic = self.str_to_bool(location.get("dynamic"));
            
            #Create a new location with the information gained from the xml
            location = Location(frame, name, message, lat, long, radius, raw_location, dynamic);
            
            #append the newly created location to a list
            locations.append(location);
        
        #return locations list
        return locations;
    
    
    #allows for the deletion of a location from the xml file.
    def delete_location(self, location):
        
        #loop through all locations
        for l in self.locations.findall("location"):
            
            #get the name of the location
            name = l.get("name");
            
            #if the name of the current element corresponds to the location, continue
            if(name == location.name):
                
                #remove the location
                self.locations.remove(l);
                
                #Write the changes to the document
                self.tree.write(self.xml_path);
                
                #return from the function and loop
                return;
    
    
    #allow for a location to be edited. Accepts: the previous name of the location, the updated location
    def edit_location(self, prev_name, location):
        
        #loop through all locations
        for l in self.locations.findall("location"):
            
            #get the name of the location
            name = l.get("name");
            
            #if the previous name is equal to the current name, a match has been found
            if(prev_name == name):
                
                #pull the data from the location
                name = location.name;
                message = location.message;
                lat = str(location.lat);
                long = str(location.long);
                radius = str(location.radius);
                raw_location = location.raw_location;
                dynamic = str(location.dynamic);
                
                #set the changes onto the original location
                l.set("name", name);
                l.set("lat", lat);
                l.set("long", long);
                l.set("radius", radius);
                l.set("raw_location", raw_location);
                l.set("dynamic", dynamic);
                l.text = message;
                
                #Write the added Element to the document
                self.tree.write(self.xml_path);
                
                #return out of function and loop
                return;
                                  