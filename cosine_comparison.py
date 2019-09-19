'''
AUTHOR: Samantha Muellner
VERSION: 2.2.0

RECENT CHANGES: combined comparing_two_comments_using_cosine and comment_to_vector --
    this resulted in a speed of 15 minutes faster
'''

# simple cosine comparison
import re, math, csv, time
from collections import Counter
from statistics import mean
from extracting_from_csv import extract_data_from_CSV

WORD = re.compile(r'\w+')
CSV_FILE = "github_comments.csv"


'''
DESCRIPTION: will get the cosine difference between the two provided vectors
RETURN: the cosine difference between the two vectors
'''
def get_cosine_of_two_comment_vectors(vector_1, vector_2):

    intersection = set(vector_1.keys()) & set(vector_2.keys())

    # the numerator is the sum of the multiplication of all intersection vector points
    numerator = sum([vector_1[point] * vector_2[point] for point in intersection])

    # determine the sum of all the vector points in each vector
    sum_1 = sum([vector_1[point]**2 for point in vector_1.keys()])
    sum_2 = sum([vector_2[point]**2 for point in vector_2.keys()])

    denominator = math.sqrt(sum_1) * math.sqrt(sum_2)

    # if no or invalid denominator, return 0 as there isn't a correlation at all
    if not denominator:
        return 0.0

    # else, return the correlation amount
    return float(numerator) / denominator


'''
DESCRIPTION: receive two comments, turn them into vectors, and calculate their cosine value
RETURN: the cosine comparison of the two comments
'''
def comparing_two_comments_using_cosine(comment_one, comment_two):
    vector_one = Counter(WORD.findall(comment_one))
    vector_two = Counter(WORD.findall(comment_two))

    return get_cosine_of_two_comment_vectors(vector_one, vector_two)

'''
DESCRIPTION: function that will compare all comments in a list against each other by cosine-comparison
RETURN: list of cosine values, with the self-compared values taken out
NOTE: that since we are doing this with a nested for loop, without certain conditions, we will be comparing
 the same comments to each other
'''
def compare_comments_in_list(comment_list):
    list_of_cosines = []
    
    for comment in comment_list:
        
        # creating list of comments that only succeed the current commen
        succeeding_comment_list = list(comment_list[comment_list.index(comment) + 1:])
        
        for second_comment in succeeding_comment_list:
            #print("comparing", comment, "with", second_comment)
            list_of_cosines += [comparing_two_comments_using_cosine(comment, second_comment)]
            
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
        # if this is a new length, create a new key:value pair
        if len(item) not in lengths_aleady_found:
            dict_of_comments[len(item)] = [item]
            lengths_aleady_found.append(len(item))
        
        # if this isn't a new length, update the existing key's value
        else:
            current_list_of_comments = dict_of_comments.get(len(item))
            dict_of_comments[len(item)] = current_list_of_comments + [item]
    
    return dict_of_comments


######### MAIN FUNCTION #########

'''
DESCRIPTION: main function that will mainly just call all other functions
RETURN: dictionay containing {author: bot_percentage} pairs
NOTE: in here, we will also create a second dictionary that will hold the final result of our cosine comp.s
'''
def getting_bot_percentage(dict_of_authors_and_comments):
    start = time.process_time()
    dict_of_bot_percentage = {}
    count = 0
    
    # loop through author, comment in dict_of_authors_and_comments.items()
    for author, comment_list in dict_of_authors_and_comments.items():
        count += 1
        list_of_all_cosines = []
        
        # pass comments into separate_like_comments_into_dict(comments) = LC_dict
        like_comments_dict = separate_like_comments_into_dict(comment_list)
        
        for like_comments_list in like_comments_dict.values():
            
            # check if there's another things in the list to actually merit comparison
            if(len(like_comments_list) > 1):

                list_of_cosines = compare_comments_in_list(like_comments_list)

                # add current list_of_cosines to main one
                list_of_all_cosines += list_of_cosines
            
            else: 
                list_of_all_cosines += [0]
            
        # condense list_of_cosines into single-mean value and place in our dict
        dict_of_bot_percentage[author] = round(mean(list_of_all_cosines), 4)

    
    print("Bot percentage calculation complete.")
    e1 = time.process_time() - start 
    print("Time elapsed: ", e1)
    print("Number of authors analyzed:", count)

    return dict_of_bot_percentage


'''
DESCRIPTION: simple function that will sort out authors who have a 50% or more possibility of being a bot
'''
def get_the_top_50_percent_of_possible_bots(full_dict_of_bot_percentage):
    
    with open("cosine_output.csv", mode = 'w') as percentage_output_file:

        fieldnames = ['percentage', 'author name']
        writer = csv.DictWriter(percentage_output_file, fieldnames = fieldnames)

        writer.writeheader()
    
        for author, percent in full_dict_of_bot_percentage.items():
            if percent > .49:
                writer.writerow({'percentage': percent, 'author name': author})

        print("cosine_output.csv complete")
        return True
    
    print("failed to write to cosine_output.csv")
    return False


### CALLING OUR FUNCTIONS ###


dict_of_comments_and_authors = extract_data_from_CSV(CSV_FILE)

dict_of_bot_percentage = getting_bot_percentage(dict_of_comments_and_authors)

# for author_name, bot_percent in dict_of_bot_percentage.items():
#     print(bot_percent, ":", author_name)

#get_the_top_50_percent_of_possible_bots(dict_of_bot_percentage)


