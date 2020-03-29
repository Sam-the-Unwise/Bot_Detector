'''
AUTHOR: Samantha Muellner
VERSION: 3.4.2
RECENT CHANGES: combined comparing_two_comments_using_cosine and comment_to_vector --
    this resulted in a speed of 15 minutes faster
'''

import re, math, csv, time
#from collections import Counter
from statistics import mean
from extracting_from_csv import extract_data_from_CSV

# allows for cosine comparison
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

WORD = re.compile(r'\w+')
CSV_FILE = "github_comments.csv"

def comparing_two_comments_using_cosine(vector_1, vector_2):
    # form a set containing keywords of both strings  
    rvector = vector_1.union(vector_2)

    l1 =[]
    l2 =[]
  
    for w in rvector: 
        if w in vector_1: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in vector_2: l2.append(1) 
        else: l2.append(0) 
    
    numerator = 0
  
    # cosine formula  
    for index in range(len(rvector)): 
            numerator += l1[index]*l2[index] 

    denominator = float((sum(l1)*sum(l2))**0.5)
    cosine_similarity = numerator / denominator 

    return cosine_similarity


def turn_comment_into_vector(sentence):
    # tokenization 
    list_of_words = word_tokenize(sentence.lower())  
  
    # sw contains the list of stopwords 
    # sw = stopwords.words('english')  
    
    # remove stop words from string 
    set_of_words = {w for w in list_of_words} #if not w in sw}  

    return set_of_words

'''
DESCRIPTION: function that will get all the comments in the rang length/2 - length*2 of the length-of-curr-comment
RETURN: a list that contains the comments (from the same author) that are in the range of length - log_[length*2](length//2)
'''
def get_comments_in_range(like_comments_dict, length_of_curr_comment):
    list_of_comments_in_range = []

    lowest_comparison = length_of_curr_comment//2
    highest_comparison = length_of_curr_comment*2

    if lowest_comparison > 1:
        # get the length of our max string to compare by taking a log base (n/2) of n*2 
        #       where n = length_of_current_comment
        #       note: this is helpful when we start to get into really large comments
        highest_comparison = int(length_of_curr_comment*math.log(length_of_curr_comment*2, lowest_comparison))
    

    # loop though like_comment_dict from range lowest_comp to highst_comp
    for index in range(length_of_curr_comment, highest_comparison):

        if index in like_comments_dict:
            
            # grab each individual comment from the value list
            for comment in like_comments_dict[index]:
                
                list_of_comments_in_range += [comment]

    return list_of_comments_in_range

'''
DESCRIPTION: function that will compare all the comments that are provided from the list_of_main_comments to the
    comments in the list_of_comments_in_range
RETURN: a list that contains all the cosines from the comparisons
'''
def compare_comments_in_range(list_of_comments_in_range, list_of_main_comments):
    
    list_of_cosines = []
    
    for main_comment in list_of_main_comments:
        
        for compare_comment in list_of_comments_in_range:
            
            list_of_cosines += [comparing_two_comments_using_cosine(main_comment, compare_comment)]
    
    return list_of_cosines


'''
DESCRIPTION: creates dict of comments of that have the same length, where the key is the length of the comment
    and the value is a list of comments that have that length
RETURN: dict as described above
'''
def separate_like_comments_into_dict(general_list_of_comments):
    lengths_aleady_found = []
    dict_of_comments = {}
    
    for item in general_list_of_comments:

        # IF this is a new length, create a new key:value pair
        if len(item) not in lengths_aleady_found:
            dict_of_comments[len(item)] = [turn_comment_into_vector(item)]
            lengths_aleady_found.append(len(item))
        
        # ELSE this isn't a new length, update the existing key's value
        else:
            current_list_of_comments = dict_of_comments.get(len(item))
            dict_of_comments[len(item)] = current_list_of_comments + [turn_comment_into_vector(item)]
    
    return dict_of_comments



'''
DESCRIPTION: main function that will mainly just call all other functions
RETURN: dictionay containing {author: bot_percentage} pairs
NOTE: in here, we will also create a second dictionary that will hold the final result of our cosine comp.s
'''
def getting_bot_percentage(dict_of_authors_and_comments):
    start = time.process_time()
    dict_of_bot_percentage = {}
    
    # loop through author, comment in dict_of_authors_and_comments.items()
    for author, comment_list in dict_of_authors_and_comments.items():
        list_of_all_cosines = []

        # 3 or less comments is not enough to accurate calculate a bot
        #  thus, only analyze if the user has posted more than 3 comments
        if len(comment_list) > 3:

            # comments are sorted into lists of same size 
            #   in form {author: {length_1 : [comments], length_2: [comments]}, author_2: {...}, ...}
            #   comments in lists are returned in vector form
            like_comments_vector_dict = separate_like_comments_into_dict(comment_list)

            for length, like_comments_list in like_comments_vector_dict.items():
                
                # elimate no comments, 'K', 'Ok', an emoji, etc.
                if(length > 2):
                    list_of_comments_in_range = get_comments_in_range(like_comments_vector_dict, length)
                    
                    # IF there are more than one comment in the range, compare
                    if(len(list_of_comments_in_range) > 1):

                        list_of_cosines = compare_comments_in_range(list_of_comments_in_range, like_comments_list)
                        list_of_all_cosines += list_of_cosines
                        
                    # ELSE add 0 to the list of cosines since this comment won't match any others
                    else:
                        list_of_all_cosines += [0]

        if(len(list_of_all_cosines) > 0):
            # condense list_of_cosines into single-mean value and place in our dict
            dict_of_bot_percentage[author] = round(mean(list_of_all_cosines), 4)
        else:
            dict_of_bot_percentage[author] = 0

    
    print("Bot percentage calculation complete.")
    e1 = time.process_time() - start 
    print("Time elapsed: ", e1)

    return dict_of_bot_percentage


'''
DESCRIPTION: simple function that will sort out authors who have a 50% or more possibility of being a bot
RETURN: boolean if file was successfully created/edited
'''
def get_the_top_75_percent_of_possible_bots(full_dict_of_bot_percentage):

    with open("top_75.csv", mode = 'w') as percentage_output_file:

        fieldnames = ['author name', "percentage"]
        writer = csv.DictWriter(percentage_output_file, fieldnames = fieldnames)

        writer.writeheader()
    
        for author, percent in full_dict_of_bot_percentage.items():
            if percent > .75:
                writer.writerow({'author name': author, 'percentage': percent*100})

        print("top_75.csv complete")
        return True
    
    print("failed to write to top_75.csv")
    return False


'''
DESCRIPTION: simple function that will sort out authors who have a 50% or more possibility of being a bot
RETURN: boolean if file was successfully created/edited
'''
def get_comments_50_to_74_percent_of_possible_bots(full_dict_of_bot_percentage):

    with open("50_to_74_comments.csv", mode = 'w') as percentage_output_file:

        fieldnames = ['author name', "percentage"]
        writer = csv.DictWriter(percentage_output_file, fieldnames = fieldnames)

        writer.writeheader()
    
        for author, percent in full_dict_of_bot_percentage.items():

            if percent > .49 and percent < .75:
                writer.writerow({'author name': author, 'percentage': percent*100})

        print("50_to_74_comments.csv.csv complete")
        return True
    
    print("failed to write to 50_to_74_comments.csv.csv")
    return False


'''
DESCRIPTION: simple function that will store all our data in a CSV
RETURN: boolean if file was successfully created/edited
'''
def write_to_CSV_file(full_dict_of_bot_percentage):
    with open("cosine_output_v3.csv", mode = 'w') as percentage_output_file:

        fieldnames = ['author name', 'percentage']
        writer = csv.DictWriter(percentage_output_file, fieldnames = fieldnames)

        writer.writeheader()
    
        for author, percent in full_dict_of_bot_percentage.items():
            writer.writerow({'author name': author, 'percentage': percent*100})

        print("cosine_output_v3.csv complete")
        return True
    
    print("failed to write to cosine_output_v3.csv")
    return False




### CALLING OUR FUNCTIONS ###

# get all of our comments in necessary dictionary
dict_of_comments_and_authors = extract_data_from_CSV(CSV_FILE)

# analyze our comments and produce dictionary of cosine results
dict_of_bot_percentage = getting_bot_percentage(dict_of_comments_and_authors)

# create CSV's of desired data
get_the_top_75_percent_of_possible_bots(dict_of_bot_percentage)
get_comments_50_to_74_percent_of_possible_bots(dict_of_bot_percentage)

write_to_CSV_file(dict_of_bot_percentage)