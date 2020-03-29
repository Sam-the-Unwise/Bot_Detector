import os # Import OS incase we need to use it 
from pymongo import MongoClient # Import pymongo for interacting with MongoDB
import re # import regular expressions so we can manipulate strings! 
import csv # import csv so that we can write to a CSV file

CSV_FILE = "github_comments.csv"
 
### SETTING UP THE DATABASE ###

# Connect to MongoDB and setup variables to our collections
if os.getpid() == 0:
    # Initial connection by parent process
    CLIENT = MongoClient('localhost', 27017) # Where are we connecting
else: 
    # No need to reconnect if we are connected
    CLIENT = MongoClient('localhost', 27017, connect=False)

DB = CLIENT.github_comments # The specific mongo database we are working with 
REPOS = DB.repos # collection for storing all of a repo's main api json information 
PULLS = DB.pulls # collection for storing all pull requests for all repos 

### EXTRACTING ALL COMMENTS ###

'''
a function that simply gets all our repos
'''
def get_all_repos():
    return REPOS.find({})

'''
a function that simply gathers all of our pulls
'''
def get_all_pull_requests():
    #return [pull for pull in PULLS.find({})]
    return [pull for pull in PULLS.find({})]

'''
function that will return a comment without
special unicode characters 
''' 
def purify_comment(comment):
    # certain websites might be mentioned -- replace these with a simple //https
    comment = re.sub(r'http\S+', '//http// ', comment)
    
    #taking out unnecessary pull_req/repo/issue references
    comment = re.sub(r'#(\w+)( |,|.)', '#0 ', comment) 
    
    #taking out unnecessary user references
    comment = re.sub(r'@(\S+)', '@X ', comment)
    
    #taking out unnecessay unicode characters
    # note that just using \s was taking out spaces as well
    return re.sub(r'\t+|\r+|\n+|(>\s+)', '', comment)

''' 
here we will create a function that will extract necessary information 
from a single pull request from our data set
'''
def extract_comment_list_from_pull_request(pull_request):
    comments_list = pull_request['comments'] #will be saved as a list of a single dictionary
    return comments_list

'''    
storing the values that we need in a dictionary
this dictionary will be returned to and called by write_data_to_CSV
NOTE: here is where we will clean the comment
'''
def store_author_and_comment_in_dict(comment_dict):
    cleaned_comment = purify_comment(comment_dict.get('comment'))
    return {'author': comment_dict.get('author_login'), 'comment': cleaned_comment}


################ MAIN FUNCTION ################

'''
our main function that will write the data to the CSV
mostly acts by calling other functions
'''
def write_data_to_CSV(csv_file_name):
    
    with open(csv_file_name, mode = 'w') as github_comments_csv_file:
        
        fieldnames = ['author_name', 'comment_content']
        writer = csv.DictWriter(github_comments_csv_file, fieldnames = fieldnames)

        writer.writeheader()
        
        all_pulls = get_all_pull_requests()
        
        #for loop that will parse through all of our pull requests
        for pull in all_pulls:
            
            # get all the comment lists from them
            current_comment_list = extract_comment_list_from_pull_request(pull)
            
            #for loop that parses though all of the comment lists and gets the individual comment info from hem
            for comment_info in current_comment_list:
                
                # get the author and comment in purified form
                current_comment_dict = store_author_and_comment_in_dict(comment_info)
                
                # wite these to CSV
                writer.writerow({'author_name': current_comment_dict.get('author'), 'comment_content': current_comment_dict.get('comment')})
        
        print ("CSV file", csv_file_name, "succesfully written")
        return True
    
    print("Error writing to", csv_file_name, ". Operation terminating")
    return False



write_data_to_CSV(CSV_FILE)