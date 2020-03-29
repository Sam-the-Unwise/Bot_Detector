import os # Import OS incase we need to use it 
from pymongo import MongoClient # Import pymongo for interacting with MongoDB
import re # import regular expressions so we can manipulate strings! 
import csv # import csv so that we can write to a CSV file

OWNER = 0
DICT_OF_AUTHORS_AND_COMMENTS = 1

CSV_FILE_START = "Author_and_Comment_Dicts/"
 
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
Get all of our pull requests
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
Will get list of commenters from a pull, and store all of their comments into a dictionary
 with the author of the commenter as a key and the comments stored as a value in list format
'''

OWNER = 0
DICT_OF_AUTHORS_AND_COMMENTS = 1

def get_dict_of_authors_with_comments(pull, current_value_list):
    dict_of_comments_and_authors = {}
    list_of_authors = []
    
    if isinstance(current_value_list, list):
        # this means there's a previous dict of authors_and_comments we need to get first
        dict_of_comments_and_authors = current_value_list[DICT_OF_AUTHORS_AND_COMMENTS]
        
        # get keys from dict and save them into list_of_authors
        for author in dict_of_comments_and_authors.keys():
            list_of_authors.append(author)
            
            
    list_of_all_comments = pull['comments']
        
    # loop through comments and get information
    for comment_info in list_of_all_comments:
        comment = purify_comment(comment_info['comment'])
        author = comment_info['author_login']

        # check if we've already added this person
        if author not in list_of_authors:
                        
            dict_of_comments_and_authors.update({author: [comment]})
            list_of_authors.append(author)

        # if so, simply add to their list of comments
        else:
            # get the current list assigned to that author
            # current_comment_list = dict_of_comments_and_authors.get(author)

            # add the new comment to the list and reassign that to the current author
            dict_of_comments_and_authors[author].append(comment)
    
    return dict_of_comments_and_authors
                    
                    
'''
sorting out all the pulls by repo

This function will loop through all of the pulls in the passed-in value, storing the
correct pulls into a dictionary under the correct repo key
'''

def sort_pulls_by_repo(all_pull_requests):
    
    dict_of_pulls_in_repo = {}
    list_of_repos = []
    
    for pull in all_pull_requests:
        # get owner of repo
        owner = pull['owner']
            
        # get name of repo
        repo_name = pull['name']
            
        # check if we've already added this person
        if repo_name not in list_of_repos:
                
            #call DOCA with current pull and NULL (because there are no previous comments for this repo)
            dict_of_comments_and_authors = get_dict_of_authors_with_comments(pull, 0)
                
            dict_of_pulls_in_repo.update({repo_name: [owner, dict_of_comments_and_authors]})
            list_of_repos.append(repo_name)
                    
        # if so, simply add to their list of comments
        else:
            # get the current list assigned to that repo
            # note that list[0] is owner and list[1] is the comments_and_authors dict
            current_value_list = dict_of_pulls_in_repo.get(repo_name)
                
            # update comments_and_authors dict
            dict_of_comments_and_authors = get_dict_of_authors_with_comments(pull, current_value_list)
                
            dict_of_pulls_in_repo[repo_name] = [owner, dict_of_comments_and_authors]
        
    return dict_of_pulls_in_repo


def write_data_to_individual_CSV():
    # get all pulls
    all_pulls = get_all_pull_requests()
    dict_of_repos_and_owners = {}
    
    # get all pulls from same repo -- format is as follows:
    # {repo: [owner, {author: [comments], author_2: [comments], etc...}]}
    dict_of_all_pulls_for_repo = sort_pulls_by_repo(all_pulls)

    csv_file_name = ""

    for repo, dict_of_owner_and_comments in dict_of_all_pulls_for_repo.items():

        # dict_of_owner_and_comments = dict_of_all_pulls_for_repo[repo]
        owner = dict_of_owner_and_comments[OWNER]
        comments_and_authors = dict_of_owner_and_comments[DICT_OF_AUTHORS_AND_COMMENTS]

        dict_of_repos_and_owners.update({repo: owner})

        csv_file_name = CSV_FILE_START + repo + "_" + owner + "_" + "comments" + ".csv"
    
        with open(csv_file_name, mode = 'w') as repo_csv:

            fieldnames = ['author', 'comment']
            writer = csv.DictWriter(repo_csv, fieldnames = fieldnames)
            writer.writeheader()
            
            for author, comments in comments_and_authors.items():
                for comment in comments:

                    writer.writerow({'author': author, 'comment': comment})
        
        print ("CSV file", csv_file_name, "succesfully written")

    with open("csv_of_repos_and_owners.csv", mode = 'w') as repo_csv:

        fieldnames = ['repo name', 'owner']
        writer = csv.DictWriter(repo_csv, fieldnames = fieldnames)
        writer.writeheader()
            
        for repo, owner in dict_of_repos_and_owners.items():

            writer.writerow({'repo name': repo, 'owner': owner})

    print ("CSV file csv_of_repos_and_owners.csv succesfully written")


        
    
    

write_data_to_individual_CSV()
