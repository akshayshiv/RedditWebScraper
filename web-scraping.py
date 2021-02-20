# Akshay Shivkumar

#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3
# All the imports that would be needed
import praw     #imports the PRAW API
import os
from prawcore import NotFound #imports the exception "NotFound" to be used when a subreddit isn't found
from twilio.rest import Client as twilio #Imports Twilio REST API

def main():
    user_agent = 'YourNumberHere'
     #Creates reddit object to scrape reddit with using PRAW
    reddit = praw.Reddit(client_id='YourClientIDHere', \
                         client_secret='YourClientSecretHere', \
                         user_agent=user_agent, \
                         username='YourUsernameHere', \
                         password='YourPasswordHere')
    account_sid = 'YourTwilioAccountSidHere' #Account ID for twilio Client
    auth_token = 'YourTwilioAccountAuthTokenHere' #Account Secret token for twilio Client
    client = twilio(account_sid, auth_token)    #Creates a twilio object
    scopes = ['read', 'submit']                 #The scope that we are permitted to use with our reddit account
    reddit.read_only = True                     # Makes it much faster, We want to be able to post so we will set this false if user selects to post 
    valid = True                                #Condition of the loop  
    returned_to_user = []                       #This is the body of the message we want to send to the user
    while(valid):                               #ensures that there is at least one successful attempt to fetch data
        to_do = input("What do you want to do? \"S: search, P: post, B: browse\" ") #Asks what user wants to do
        if to_do != "S" and to_do != "P" and to_do != "B":
            print("This is not a valid option please try again")    #Error message
            continue
        sub_input = input("Which sub? ")                #Asks what subreddit they want to go to
        try:
            subreddit = reddit.subreddit(sub_input)
            exists = reddit.subreddits.search_by_name(sub_input, exact =True)   #Ensures that there is a subreddit with this name
        except NotFound: 
            print("Please enter a valid Subreddit\n")
            continue
        if to_do == "S":                        #Option if user wants to serve
            search_info = input("What do you want to search for? ")
            for post in subreddit.search(search_info, syntax = "plain", limit = 5): #Gets the 5 search terms that match what the user wants
                returned_to_user.append("https://www.reddit.com" + post.permalink)
        elif to_do == "P":                      #Option if user wants to post
            reddit.read_only = False #Makes it so that you can post to a subreddit
            title = input("Title? ")    #Asks the user what the title and body of what they want to post is
            body = input("Body: ")
            reddit.validate_on_submit = True            #Makes sure that that the subreddit is valid to be posted
            try:
                subreddit.submit(title = title, selftext = body)        #Submit this post to the subreddit
            except Exception:
                print("There was an error in posting your post. Please check you are allowed to post on this sub")
            returned_to_user.append("Your post was sent successfully") #Returns to the user that it was a successful post
        elif to_do == "B":                                              #Checks to see if you want to browse a certain subreddit
            request = input("What do you want to browse for? T: top, H: hot ")      #Limitations on what you want to browse by
            if request == "H":                                              #Hits here if they want to browse "Hot"
                for post in subreddit.hot(limit = 5):
                    returned_to_user.append((post.title, "https://www.reddit.com" + post.permalink))
            elif request == "T":                                            #Hits here if they want to browse "Top"
                for post in subreddit.top(limit = 5):
                    returned_to_user.append((post.title, "https://www.reddit.com" + post.permalink))
            else: raise NotFound("This is not a valid option")
        valid = False

    for elem in returned_to_user:           #iterates through the elements of the list and sends it to a designated user
        message = client.messages\
            .create(
                body = elem,
                from_ = 'YourTwilioNumberHere',             #Twilio given number
                to = '+ThePersonYouSentThisToHere'                 #Number you want to send a message to
        )
        print("Sent, message ID:", message.sid)     #Prints the statement that it was succesfully processed
main()