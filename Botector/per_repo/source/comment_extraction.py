import re, math, csv, sys
#from make_csv import write_data_to_CSV

REPO = 0
OWNER = 1
AUTHOR = 2
COMMENT = 3

csv.field_size_limit(sys.maxsize)

'''
simple function that will find the author in the ac_dict, and add the comment to the existing list of comments
will return the new ac_dict of comments and authors
'''

def add_comment_to_ac_dictionary(comment, author, ac_dict):
    list_of_comments = ac_dict[author]
    
    list_of_comments += [comment]
    
    ac_dict[author] = list_of_comments
    
    return ac_dict

'''
function used to extract our author and comments from CSV
works by returning a dictionary of author:comment key:value pairs
note that the comments (the values) are in list form in order to assign multiple comments to one author
'''
def extract_comments(csv_file):
    
    with open(csv_file,'rt') as filehandler:
        #to avoid complications with the null byte
        data = csv.reader(x.replace('\0', '') for x in filehandler)
        
        list_of_repos = []
        # create dict that will hold an author/repo pair that can be checked when we are adding our
        #   author to the main dictionary -- if the author/repo pair is in here, we will handle
        #   our case accordingly
        #   IF they are not in here, then we simply just add them to the main dictionary without fuss
        author_repo_dictionary = {} 
        
        dict_of_repos = {}
        
        for row in data:
            repo = row[REPO]
            owner = row[OWNER]
            author = row[AUTHOR]
            comment = row[COMMENT]
                
            if repo not in list_of_repos:
                dict_of_repos.update({repo: [owner, {author: [comment]}]})
                author_repo_dictionary.update({author: repo})
                list_of_repos += [repo]
            else:
                value = dict_of_repos[repo]
                author_and_comment_dict = value[1] #value[0] = owner
                        
                # IF we find an author/repo pair in our dictionary, this means we've already added the
                #  author to this repo and must carefully add the comment to its dictionary
                if author in author_repo_dictionary and repo == author_repo_dictionary[author]:
                    new_ac_dict = add_comment_to_ac_dictionary(comment, author, author_and_comment_dict)
                        
                    dict_of_repos.update({repo: [owner, new_ac_dict]})
                        
                # ELSE we haven't yet had a comment from this author for this repo, so add to 
                #  author_comment_dict
                else:
                    author_and_comment_dict.update({author: [comment]})
                    dict_of_repos.update({repo: [owner, author_and_comment_dict]})
                        
                    author_repo_dictionary.update({author: repo})


    print("Comment extraction complete--Dictionary formed")                
    
    return dict_of_repos
