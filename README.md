# Bot_Detector
Currently:
A project that will grab information from a MongoDB database (which has been mined from Github repositories), sort the data based by author, and analyze the comments against each other to determine a percentage of certainty on whether or not the author of those comments is a bot. 

Future:
This project will expand to include an analysis of an author's profile on Github to create a more accurate reading of whether or not a user is a bot.

<i> Please note, this code is designed to run on a Linux machine and includes packages that will not work on Windows </i>

### writing_csv.py

This script contains all the methods necessary for extracting the data from MongoDB and saving it accordingly in a csv file for easier access.

### extracting_from_csv.py

This script contains all the methods necessary for extracting the data from the csv file (made by writing_csv.py) and storing the information in a python dictionary for easier use. The dictionary stores the information in the following manner: {author_1: [list_of_author_1_comments], author_2: [list_of_author_2_comments], ....}

### cosine_comparison.py

This script contains all the methods that are used to compare our comments against each other. Comments are compared against others only with the same length as the current comment. Comments are compared against each other using a cosine comparison method. The predicted bot percentage is outputted to a csv file in the format {authors name, percentage}.

### cosine_comparison_II.py

This script contains all the methods that are used to compare our comments against each other. Comments are compared against others within the range of the length of the current comments length (n) to n*log{n//2}{n*2}. Comments are compared against each other using a cosine comparison method. The predicted bot percentage is outputted to a csv file in the format {authors name, percentage}. CSV files are saved based on the name of the repository and repo owner the comments were taken from.

### analyze_output.py

This script contains all the methods used to extract the author and bot_percentage from the different files created by cosine_comparison_II.py and stores them in a single csv file based on different variables.

## Authors

* **Samantha Muellner** - [GitHub](https://github.com/Sam-the-Unwise)

## Acknowledgments

* **Igor Steinmacher, PHD.** - *Advisor* [Profile](https://www.igor.pro.br/)
