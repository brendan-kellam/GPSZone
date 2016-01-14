import tweepy;
import tkMessageBox;

#-------
#The Twitter class is responsible for all communications with Twitter
#-------
class Twitter:
    
    #constructor
    def __init__(self):
        
        
        #---APP INFORMATION--- do not steal pls :/
        
        #consumer key and consumer secret
        consumer_key = "rMocCNM3jRPzZJbZh7wJgVSEG";
        consumer_secret = "lMh32kug5ubgM9Mo8sZmOw3ex05CwZ7A8Eravi9quOQRLBtCfe";

        #access token and access token secret
        access_token = "2929065220-fLBnmTKeODyDAJaNmWnjmz8S0aNDH0fKmvDByjG";
        access_token_secret = "fU5vkvzzTSxHTx4dhcvhaShi2t8fr91yTEqS4D2LRFiiG";
        
    
        #call to twitter so the aunthentication process can occure with the provided app information (see above^)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret);
        
        #set authentication to secure
        auth.secure = True
        
        #set the access token and access token secret for the application
        auth.set_access_token(access_token, access_token_secret);
                
        #create a new api object using the authentication data (this object will allow for posts to occur)
        self.api = tweepy.API(auth);
        
    
    #tweet function. Simply just tweets to the user
    def tweet(self, message, username):
        
        #add a @ symbol to refrence the user and the message following
        data = "@" + username + " " + message;
        
        #try except employed incase error occures
        try:
            
            #update the status
            self.api.update_status(data);
        except:
            
            #if a error occurs, show error popup
            tkMessageBox.showinfo("Error", "It seems one of your tweets failed to upload \nthis may be caused by a repeat message.\n sorry :/");  
            
