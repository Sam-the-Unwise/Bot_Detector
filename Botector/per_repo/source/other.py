# '''
# DESCRIPTION: main function that will mainly just call all other functions
# RETURN: dictionay containing {author: bot_percentage} pairs
# NOTE: in here, we will also create a second dictionary that will hold the 
#       final result of our cosine comp.s
# '''
# def getting_bot_percentage_using_repo_dict(dict_of_repos):
#     start = time.process_time()
#     dict_of_repos_with_percents = {}
#     count = 0
#     subtotal = 0
#     total = 0
    
#     while(count < 1):
#         # loop through author, comment in dict_of_authors_and_comments.items()
#         for repo, info_list in dict_of_repos.items():
#             count += 1

#             dict_of_bot_percentage = {}
#             list_of_all_cosines = []

#             owner = info_list[OWNER]
#             dict_of_authors_and_comments = info_list[AUTHORS_AND_COMMENTS]


#             for author, comment_list in dict_of_authors_and_comments.items():
#                 total += len(comment_list)

#             print ("Total " + str(total))


#             for author, comment_list in dict_of_authors_and_comments.items():
#                 print("Percent (by author) Complete: " + str(subtotal/total * 100))
#                 print("Current analysis on author: " + author)
#                 subtotal+=1

#                 # 3 or less comments is not enough to accurate calculate a bot
#                 #  thus, only analyze if the user has posted more than 3 comments
#                 if len(comment_list) > 3:

#                     # comments are sorted into lists of same size 
#                     #   in form {author: {length_1 : [comments], length_2: [comments]}, author_2: {...}, ...}
#                     #   comments in lists are returned in vector form
#                     like_comments_vector_dict = separate_like_comments_into_dict(comment_list)

#                     for length, like_comments_list in like_comments_vector_dict.items():
                        
#                         # elimate no comments, 'K', 'Ok', an emoji, etc.
#                         if(length > 2):
#                             list_of_comments_in_range = get_comments_in_range(like_comments_vector_dict, length)
                            
#                             # IF there are more than one comment in the range, compare
#                             if(len(list_of_comments_in_range) > 1):

#                                 list_of_cosines = compare_comments_in_range(list_of_comments_in_range, like_comments_list)
#                                 list_of_all_cosines += list_of_cosines
                                
#                             # ELSE add 0 to the list of cosines since this comment won't match any others
#                             else:
#                                 list_of_all_cosines += [0]

#                 if(len(list_of_all_cosines) > 0):
#                     # condense list_of_cosines into single-mean value and place in our dict
#                     dict_of_bot_percentage[author] = round(mean(list_of_all_cosines), 4)
#                 else:
#                     dict_of_bot_percentage[author] = 0
            
#             dict_of_repos_with_percents.update({repo: [owner, dict_of_bot_percentage]})

#     print("Bot percentage calculation complete.")
#     e1 = time.process_time() - start 
#     print("Time elapsed: ", e1)

#     return dict_of_repos_with_percents