#imports
from Tkinter import *;
import sys;


#-------
#Utilities class. Has functions that need to be called across the program.
#No specific function other than to provide utilities
#-------

class Util:
    
    #constructor. No parameters
    def __init__(self):
        pass;
    
    #tool for asking the user for a number question (i.e. input("") ) 
    def number_qus(self, query): 
        
        try:
            #NOTE: Rather than using raw_input, this solution needed to be used. TKInter liked to crash when calling raw_input in a seperate
            #thread :/
            
            #print the question
            print query;
            
            #get result.
            result = int(sys.stdin.readline()); 
            
        except:
            
            #if a error occurs, re-call the function
            print "Error. Revived a non-number type!"; 
            result = self.number_qus(query);
        
        #return the result
        return result;
    
    #tool for asking the user for a string question (i.e. raw_input("") ) 
    def string_qus(self, query):
        
        try:
            print query;
            result = sys.stdin.readline() #get result
        except:
            
            #if a error occurs, re-call the function
            print "Error occurred!"; 
            result = self.string_qus(query);
        
        return result;
    
    def init_tinker(self, canvas):
        self.window = canvas;
    
    #---TKINTER TOOLS---

    #create a new, standard button for tkinter window
    def button(self, x, y, txt, wdth, command):
        
        #create a new button and configure it
        button = Button(self.window, text=txt, comman=command, anchor=W); #create new button object
        button.configure(width=wdth);
        
        #create a window for the button to allow for it to show on a canvas 
        self.window.create_window(x, y, anchor=NW, window=button);
        
        #return the button
        return button;
    
    #create a new label for tkinter window
    def label(self, x, y, txt, colour):
        
        #create a new label with specified text and colour
        label = Label(self.window, text=txt, fg=colour);
        
        #create a new window to allow it to be visible on canvas
        self.window.create_window(x, y, anchor=NW, window=label);
        
        #return the label
        return label;
    
    #add a image to the tkinter window (.gif file format)
    def image(self, x, y, res):
        
        #create a new image object representing pulled gif file
        img = PhotoImage(file = res);
        
        #create a window for the image to be displayed on the canvas
        self.window.create_image(x, y, image=img, anchor=NW);
           
        #return the created image 
        return img;
    
    #Create a new text area
    def text_area(self, x, y, wdth, hght):
        
        #create a new Text object
        text = Text(self.window, height=wdth, width=hght);
        
        #create a new scrollbar for the text box
        scroll = Scrollbar(text);
        
        #create a veiwable window for the textbox
        self.window.create_window(x, y, anchor=NW, window=text);
        
        #return the created Text object
        return text;
    
    #Create a new text entry box
    def text_entry(self, x, y, wdth):
                
        #create a new Entry instance
        entry = Entry(self.window, width=wdth);
        
        #add the text entry to the canvas
        self.window.create_window(x, y, anchor=NW, window=entry);
        
        #return the create Text entry
        return entry;
    
    #Creates a new check box
    def check_box(self, x, y, callback):
                              
        #create new instance of the Checkbutton class
        check = Checkbutton(self.window, state=NORMAL, command=callback);
        
        #Create a new window to allow checkbox to appear on canvas
        self.window.create_window(x, y, anchor=NW, window=check);
                        
        #return the created check box
        return check;
    
    
            