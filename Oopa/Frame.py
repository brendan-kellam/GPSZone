
#imports:
from Tkinter import *;
from Util import Util;
from time import sleep;
import Serial_Communication; 
import ttk;
import Decoder;
import Locations;
import tkMessageBox;
import thread;
import Twitter;
import XML;

#-------
#The Frame class is responsible for handling, updating, and maintaing the main frame.
#It also updates, tweets and creates new location
#It is the primary core of the program
#-------
class Frame:

    #constructor
    def __init__(self):
        self.run();                
                
    #initialize classes
    def initialize(self):
            
        #create a new instance of Decoder
        self.decode = Decoder.Decode();
        
    #initialize frame
    def run(self):
        
        #create a new TKinter Instance and set title
        self.app = Tk();
        self.app.wm_title("GPS Zone Setter");
        
        #initialize the gps application
        self.initialize();
        
        #initialize the window canvas
        self.window = Canvas(self.app, width = 420, height = 385, bg="white", cursor = "coffee_mug");
        self.window.pack();
        
        #initialize the Util module for use of TKinter functions
        self.util = Util();
        self.util.init_tinker(self.window);
        
        #Create a new instance of the Twitter class
        self.twitter = Twitter.Twitter();
        
        #Create a new instance of the XML class
        self.XML = XML.XML();
        
        #create a new locations list. Assinged to all cached locations in the xml file
        #to allow for saving
        self.locations = self.XML.read_locations(self);
                        
        #list that holds each line of the location table
        self.table = [];
        
        #the user's twitter username
        self.username = self.XML.twitter_user();
        
        #the default delay setting for dynamic tweets
        self.delay = self.XML.get_delay();
        
        #set the gps communication to False;
        self.gps_communication = False;
                
        #---FRAME CODE---
        
        #create a label and status image for the connectivity status of the Gps module.
        #will initially show (red) apon start-up.
        self.util.label(5, 5, "Gps Status:", "black");
        self.check_gps_status();
        
        
        #create a label and status image for the status of the Twitter connection
        #will initially show (red) apon start-up.
        self.util.label(5, 30, "Twitter:", "black");
        self.check_twitter_status();
        
        
        #Create labels that display the current latitude and longitude coordinate points
        self.status = self.util.label(5, 65, "Current Position:", "black");
        self.lat_status = self.util.label(8, 85, "Lat: ", "black");
        self.long_status = self.util.label(8, 105, "Long:", "black");
        
        #Create a new concurrent thread that calls the self.update_gps function. 
        thread.start_new_thread(self.update_gps, ());
    
        #Create new settings button
        self.util.button(5, 140, "Settings", 10, self.open_settings);
        
        #create labels that explain what the table of Locations essentially shows (i.e location and ID)
        self.util.label(150, 10, "Location:", "black");
        self.util.label(300, 10, "ID:", "black");
         
        #create a new text area that will show the cached locations to the user. 
        #text box used because nothing is better in Tkinter! **throws keyboard :( 
        self.table_locations = self.util.text_area(150, 30, 10, 30);
        self.table_locations.configure(state=DISABLED);
        
        #add any cached locations to the table (see: XML and top of this function)
        for location in self.locations:
            self.table_add(location);
        
        #create a new button that allows for users to add a button
        self.util.button(325, 200, "+", 2, self.add_location);
        
        #Label and text area that allow for users to enter in ID of location to edit
        self.util.label(150, 200, "ID:", "black");
        self.id = self.util.text_entry(180, 200, 4);
        
        #button to allow for location to be eddited
        self.util.button(230, 200, "Edit", 2, self.edit_location);
    
        #Set dimensions and default location of frame
        self.app.geometry("420x385+500+150");       
        
        #set frame to appear above all other open programs
        self.app.call('wm', 'attributes', '.', '-topmost', '1');
        
        #main loop
        self.app.mainloop();
    
    #pulls the current location from the GPS module. (---!!!THIS FUNCTION IS CALLED IN SEPERATE THREAD!!!---)
    def update_gps(self):
        
        #create a new instance of Serial_Communication
        comm = Serial_Communication.Communication(); 
        
        #set the communication boolean to true as communication has begun
        self.gps_communication = True;       
        
        #The serial loop. Responsible for polling the gps and pulling data
        while True:
            
            #try:except incase a error occurs while communicating with gps module
            try:
                #pull data from the gps module and translate data from NMEA to computable information
                data = comm.pull_data();
                data = self.decode.NMEA_0183(data);
            
            #except error
            except:
                
                #set communication to False, update indicators and show error message
                self.gps_communication = False;
                self.check_gps_status();
                tkMessageBox.showinfo("Error", "A error occurred while communicating with the gps module.\nRestart the program and try again.");
                break;  
            
            #if data was produced
            if(data != None):
                
                #get the longitude and latitude from the data
                lat = float(data[0]);
                long = float(data[1]);
                
                #loop through all locations
                for location in self.locations:
                    
                    #if the user is within a location
                    if(location.is_within(lat, long)):

                        #tell the location the user is within
                        location.within();
                
                #processes and prints the latitude info to the frame
                lat_str = "Lat: " + str(lat);
                self.lat_status.configure(text=lat_str);
               
                #processes and prints the longitude info to the frame
                long_str = "Long: " + str(long);
                self.long_status.configure(text=long_str);
                
                self.check_gps_status();
                
    #update the gps status indicator (the red/green circle)         
    def check_gps_status(self):
        
        #create a new string to hold path
        status = "";
        
        #if the gps module is not responding, set image to red
        if(not self.gps_communication):
            status = "res/status_red.gif";
        
        #if it is, set immage to green
        else:
            status = "res/status_green.gif";
        
        #add the image to the image container
        self.gps_status = self.util.image(85, 12, status); 
          
    #update the twitter status indicator
    def check_twitter_status(self):
        
        #create a new string to hold path
        status = "";
        
        #if the username is not null (space in this case due to xml) set status to green
        if(self.username != " "):
            status = "res/status_green.gif";
            
        #if not, set status to red
        else:
            status = "res/status_red.gif";
        
        #update the twitter status image
        self.twt_status = self.util.image(85, 37, status);
    
    #allows for the locations to tweet their status message
    def tweet(self, message):
        
        #call the Twitter tweet function and pass in username and message
        self.twitter.tweet(message, self.username);
        
    #Allow for the user to open a new settings frame        
    def open_settings(self):
        Settings(self.settings_callback, self);
        
    #callback for the Settings pane to add data back into main program (see: Settings.add_data)
    def settings_callback(self, name, delay):
        
        #assign variables to class wide variables
        self.username = name;
        self.delay = delay;
        
        #write the changes to the xml document
        self.XML.edit_twitter_user(name);
        self.XML.edit_delay(delay);
        
        #update the twitter status indicator
        self.check_twitter_status();
        
    #allows for the user to add a new location
    def add_location(self):        
        Manip_Location(self.add_location_callback, None);

    #allows for the user to edit a pre-existing location
    def edit_location(self):
        
        #get the entered id from the user
        id = self.id.get();
        
        #loop through all cached id's
        for location in self.locations:
            
            #if the location referenced is found then continue
            if(location == id):
                
                self.id.delete(0, END);
                Manip_Location(self.edit_location_callback, location);
                return;
        
        #if the entered id cannot be found, open a new prompt window telling the user the error
        tkMessageBox.showerror("Error", "This Location does not exist");

        
    #allows for the Manip_Location class to add a location (see: Manip_Location.add_data)
    def add_location_callback(self, name, message, lat, long, radius, raw_location, dynamic_state):
                
        #create a new location instance with the data received
        location = Locations.Location(self, name, message, float(lat), float(long), float(radius), raw_location, dynamic_state);
        
        #append the newly location to the locations list and write to locations table
        self.locations.append(location);
        self.table_add(location);
        
        #add the location to the xml file
        self.XML.write_location(location);
        
    #allows for the Manip_Location class to edic a location     
    def edit_location_callback(self, location, deletion, name, message, lat, long, radius, raw_location):
        
        #if the edit is not a deletion
        if(not deletion):
            
            #store the previous name of the location
            prev_name = location.name;
            
            #initially, delete the specific location 
            self.table_del(location);
            
            #edit the data of the location to the inputed information
            location.name = name;
            location.message = message;
            location.lat = float(lat);
            location.long = float(long);
            location.radius = float(radius);
            location.raw_location = raw_location;
            
            #re-add the edited location to the table
            self.table_add(location);
            
            #add new data to the xml
            self.XML.edit_location(prev_name, location);
       
        #if the location is being deleted
        else:
            
            #delete the specific location
            self.delete_location(location);
            
    #deletes the location from the cached list
    def delete_location(self, location):
        
        #remove from the locations list
        self.locations.remove(location);
        
        #get the name and id from the location        
        name = location.name;
        id = location.id;
        
        #format the name and id to the poper table format. 
        data = self.format_data(name, id);
        
        #remove location from table
        self.table.remove(data);
        
        #re-write the locations table to make changes
        self.table_write();
                
        #delete the location from the stored xml file
        self.XML.delete_location(location);
        
    
    #Clear the locations table
    def table_clear(self):
        
        #simply enables editing, deletes all text and disables again. 
        self.table_locations.configure(state=NORMAL);
        self.table_locations.delete(1.0, END);
        self.table_locations.configure(state=DISABLED);
        
    
    #deletes a specific location from the table
    def table_del(self, location):
        
        #get the name and id from the location        
        name = location.name;
        id = location.id;
        
        #format the name and id to the poper table format. 
        data = self.format_data(name, id);
        
        #search the table and remove the location
        self.table.remove(data);
        
        #write to the table
        self.table_write();
    
    #adds a new location to the locations table 
    def table_add(self, location):
        
        #get the name and id from the location
        name = location.name;
        id = location;
        
        #format the data 
        data = self.format_data(name, id);
        
        #append the new formated location
        self.table.append(data);
        
        #write to the table
        self.table_write();
        
    #Formats and writes to the location table
    def table_write(self):
        
        #initially, clear all data from the table
        self.table_clear();
        
        #create a new null data string that will hold the formated information
        data = "";
        
        #loop through the range of the cached data (found in the list self.table)
        for i in range(len(self.table)):
            
            #append the location at the current index to the data string
            data += self.table[i];
            
            #if the current iteration is not the last
            if(i != len(self.table) -1 ):
                
                #append a newline character for formating purposes 
                data += "\n"
                
        #set the state of the table to editable, write the data and disable table
        self.table_locations.configure(state=NORMAL);
        self.table_locations.insert(END, data)
        self.table_locations.configure(state=DISABLED);
        
        
        
    #format location data to allow for use in locations table
    def format_data(self, name, id):
        #set the space offset by taking 21 spaces (distance from start of table to Id column) from the length of the location name
        offset = 21 - len(name);
        
        #create a data string that starts with a new line character (to allow for spacing)
        data = "";
        
        #add the name to the data
        data += name;
        
        #loop through the length of the offset, adding a space for each index
        for i in range(offset):
            data += " ";
        
        #add the id 
        data += str(id);
                        
        #return the formated data
        return data;
        
#----HANDLES ADDING AND EDITING LOCATION EVENT-----
class Manip_Location:
    
    #constructor. Accepts a callback function to allow transfer data from this class to Frame, edit_location allows for a pre-existing location to be
    #edited
    def __init__(self, callback, edit_location):
        
        #initialize callback to class scope
        self.callback = callback;
        
        self.edit_location = edit_location;
        
        #initialize the frame
        self.run();
    
    #initializes the frame
    def run(self):
        
        #create new TkInter instance and set title
        self.app = Tk();
        self.app.wm_title("Add Location");
        
        #initialize the window canvas
        window = Canvas(self.app, width = 420, height = 385, bg="white", cursor = "coffee_mug");
        window.pack();
        
        #create a new instance of Decoder
        self.decode = Decoder.Decode();
        
        #initialize the Util module for use of TKinter functions
        self.util = Util();
        self.util.init_tinker(window);   
        
        #Create a new boolean to hold the state of the dynamic checkbox
        self.dynamic_state = False;     
        
        #---FRAME CODE---
        
        #Set a label and text entry area for user to set name of location
        self.util.label(5, 5, "Location Name:", "black");
        self.location = self.util.text_entry(110, 5, 13);
                   
        #Set a label and text entry area for user to set message for the location
        self.util.label(5, 35, "Message:", "black");
        self.message = self.util.text_entry(110, 35, 13);

        #Set a label and text entry area for google maps data
        self.util.label(5, 65, "Position:", "black");
        self.position = self.util.text_entry(110, 65, 13);
        
        #create a help (?) button for positon
        self.util.button(230, 65, "?", 1, self.help_position);
        
        
        #Set a label and text entry of radius 
        self.util.label(5, 95, "Radius (km)", "black");
        self.radius = self.util.text_entry(110, 95, 3);

        #Create a add button allowing for user to add data to Location
        self.util.button(160, 95, "Add", 5, self.add_data);  
        
        #if a location already exists, then continue
        if(self.edit_location != None):
            
            #change the title of the frame
            self.app.wm_title("Edit Location");
            
            #create a new delete button 
            self.util.button(160, 120, "Delete", 5, self.delete_data);
            
            #pull data from existing location
            name = self.edit_location.name;
            msg = self.edit_location.message;
            pos = self.edit_location.raw_location;
            rad = self.edit_location.radius;
            
            #insert the data into the existing field (just for convenience for the user)
            self.location.insert(END, name);
            self.message.insert(END, msg);
            self.position.insert(END, pos);
            self.radius.insert(END, rad);
        
        #if a new location is being created, dynamic settings need to be shown
        else:
            
            #Create a new check box for user to have options on if it dynamic or not
            self.util.label(5, 125, "Dynamic:", "black");
            self.dynamic = self.util.check_box(70, 125, self.dynamic_check_set);    
                        
            #also add a question help button so users know what the hell the dynamic option is
            self.util.button(100, 125, "?", 1, self.help_dynamic);

            
        #Set dimensions and default location of frame
        self.app.geometry("300x165+550+200");       
        
        #set frame to appear above all other open programs
        self.app.call('wm', 'attributes', '.', '-topmost', '1');
        
        #main loop
        self.app.mainloop();  
    
    #gets the current state of the dynamic check box
    def dynamic_check_set(self):
        
        #if the boolean dynamic_state is False, change to True
        if(not self.dynamic_state):
            self.dynamic_state = True;
            return;
        
        #If not, set dynamic_state to False
        self.dynamic_state = False;
        
    #Add location back into main program
    def add_data(self):
          
        #get the information from all entry boxes
        name = self.location.get();
        message = self.message.get();
        position = self.position.get();
        radius = self.radius.get();
        
        #checks if the location name is null (throw error and return if this occurs)
        if(name == ""):
            tkMessageBox.showerror("Error", "The Location Name is empty");
            return;
            
        #check if the message is null
        if(message == ""):
            tkMessageBox.showerror("Error", "You have no message");
            return;
        
        #checks if message is greater than the 140 character limit
        if(len(message) > 140):
            tkMessageBox.showerror("Error", "Your message cannot exceed the 140 character limit set by twitter");
            return;
            
        #check if the position data is null
        if(position == ""):
            tkMessageBox.showerror("Error", "The Position is empty");
            return;
        
        #try except employed to ensure errors with decoding are handled
        try:
            
            #get the latitude and longitude data by decoding the google maps data
            lat, long = self.decode.decode_maps_data(position);
        
        #catch the error 
        except:
            tkMessageBox.showerror("Error", "The Position data entered is not valid");
            return; 
        
        #check if the radius data is null
        if(radius == ""):
            tkMessageBox.showerror("Error", "The radius is empty");
            return;
    
        #try except used incase radius is non-integer/float value
        try:
            
            #convert the entered radius to float
            radius = float(radius);
            
        #catch the error
        except:
            tkMessageBox.showerror("Error", "Radius invalid");
            return;

        #destroy the window
        self.app.destroy();
        
        #if no pre-existing location exists, continue
        if(self.edit_location == None):
                
        
            #callback to the main application with the data (see: Frame.add_location()).
            self.callback(name, message, lat, long, radius, position, self.dynamic_state);
            
        else:
            #callback to the main application with the edited data (see: Frame.edit_location())
            self.callback(self.edit_location, False, name, message, lat, long, radius, position);
        
    #handles the user deleting the current location
    def delete_data(self):
        
        #destroy the window
        self.app.destroy();
        
        #callback to main aplication. sends a True boolean to allow for deletion 
        self.callback(self.edit_location, True, None, None, None, None, None, None);
    
    #sDisplays a help pop-up window to help with knowing what dynamic setting is
    def help_dynamic(self):    
        
        #The help message
        help = "The dynamic setting allows this:\n\n";
        help += "1. Locations wont be deleted right after you enter a location\n"
        help += "2. A Tweet will be sent to you every delay (look in settings) rather than once\n"
        help += "3. Allows you to remind yourself if you are forgetful...like me >.<"
        
        #creates a new pop-up widget with the help message
        tkMessageBox.showinfo("Help", help);  
        
        
    #Displays a help pop-up window to help with the position inputing
    def help_position(self):
        
        #The help message
        help = "The position input is just asking you the coordinates of the desired location\n\n";
        help += "Follow these steps:\n";
        help += "1. Go to maps.google.com\n";
        help += "2. Find the desired location, right click and hit \"Directions to here\"\n"
        help += "3. Copy the link and paste it into the Position box\n"
        help += "All done :)"
        
        #creates a new pop-up widget with the help message
        tkMessageBox.showinfo("Help", help);  
        

#----HANDLES THE SETTINGS FRAME----
class Settings():
    
    def __init__(self, callback, frame):
        
        #assign the callback function to a local variable
        self.callback = callback;
        
        #assign the frame instance to call back to the Frame class
        self.frame = frame;
        
        #initialize the frame
        self.run();
    
    
    #initializes the frame
    def run(self):
        
        #create new TkInter instance and set title
        self.app = Tk();
        self.app.wm_title("Settings");
        
        #initialize the window canvas
        window = Canvas(self.app, width = 420, height = 385, bg="white", cursor = "coffee_mug");
        window.pack();
        
        #create a new instance of Decoder
        self.decode = Decoder.Decode();
        
        #initialize the Util module for use of TKinter functions
        self.util = Util();
        self.util.init_tinker(window);        
        
        #---FRAME CODE---
        
        #Create label and entry box to allow user to enter in Twitter credentials
        self.util.label(10, 10, "Twitter Username:", "black");
        self.username = self.util.text_entry(130, 10, 13);
        
        #if the username is not null (in this case null is " " due to xml errors)
        if(self.frame.username != " "):
            self.username.insert(END, self.frame.username);
    

        #Create label and entry box to allow user to set delay on auto tweets
        self.util.label(10, 40, "Delay (h):", "black");
        self.delay = self.util.text_entry(80, 40, 3);
        self.delay.insert(END, self.frame.delay);
        
        #create a help (?) button for delay input
        self.util.button(120, 40, "?", 1, self.help_delay);
        
        #allows for the user to confirm and input data
        self.util.button(160, 40, "Ok", 2, self.add_data);
            
        #Set dimensions and default location of frame
        self.app.geometry("300x100+550+200");       
        
        #set frame to appear above all other open programs
        self.app.call('wm', 'attributes', '.', '-topmost', '1');
        
        #main loop
        self.app.mainloop();  
    
    #When the Ok button is called, the data will be processed, called-back and the frame will be closed
    def add_data(self):
        
        #pull the data from the entry boxes
        name = self.username.get();
        delay = self.delay.get();
        
        #checks if the delay is a non-float value
        try:
            
            #convert delay from string to float
            delay = float(delay);
        except:
            tkMessageBox.showerror("Error", "The delay is a non-valid input");
            return;
        
        #if the delay is greater than 24.0 hours, throw error
        if(delay > 24.0):
            tkMessageBox.showerror("Error", "Cannot set delay for more than 24 hours");
            return;
        
        #if the delay is less than 30 mins, throw error
        if(delay < 0.50):
            tkMessageBox.showerror("Error", "Cannot set delay for less than 30 minutes");
            return;
        
        #destroy the window
        self.app.destroy();
        
        #set safe-guards for the xml manipulation
        if(name == ""):
            name = " ";
        
        if(delay == ""):
            delay = 0.5;
        
        #call the callback to send data back to the main program
        self.callback(name, delay);
        
        
    #opens new help prompt for user. Describes the delay input
    def help_delay(self):
        #The help message
        help = "The delay allows you to set a time on all automatic outgoing tweets. (if the location is dynamic)\n\n";
        help += "If you are in a location and do not leave, a tweet will be sent every time the delay expires.\n\n"
        help += "So just input a time in hours for the delay :)";

        
        #creates a new pop-up widget with the help message
        tkMessageBox.showinfo("Help", help);  
        