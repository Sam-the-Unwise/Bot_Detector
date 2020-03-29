import csv, sys

AUTHOR = 0
COMMENTS = 1
DICT_OF_AUTHORS_AND_COMMENTS = 1
csv.field_size_limit(sys.maxsize)

'''
function used to extract our author and comments from CSV
works by returning a dictionary of author: comment key:value pairs
note that the comments (the values) are in list form in order to assign multiple comments to one author
'''

'''
function used to extract our author and comments from CSV
works by returning a dictionary of author: comment key:value pairs
note that the comments (the values) are in list form in order to assign multiple comments to one author
'''

def extract_data_from_CSV(data_CSV_file):
    data_dict = {}
    
    with open(data_CSV_file,'rt') as file:
        
        #to avoid complications with the null byte
        data = csv.reader(x.replace('\0', '') for x in file)
        
        '''
        this will be a list of authors that we have already added to our dictionary
            if we have not already added them we will go into our first if statement
            if we have already added them, we will go into the else statement

        note: include "author" since we don't want to include the headings of the csv
        '''
        list_of_authors = []
        
        # get data from CSV
        for row in data:

            # check if we've already added this person
            if row[AUTHOR] not in list_of_authors:
                list_of_comments = [row[COMMENTS]]

                data_dict.update({row[AUTHOR]: list_of_comments})
                list_of_authors.append(row[AUTHOR])
                    
            # if so, simply add to their list of comments
            else:
                # get the current list assigned to that author
                current_comment_list = data_dict.get(row[AUTHOR])
                
                # add the new comment to the list and reassign that to the current author
                data_dict[row[AUTHOR]] = current_comment_list + [row[COMMENTS]]
                
                    
    return data_dict

