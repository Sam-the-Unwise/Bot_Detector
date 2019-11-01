import csv

dict_of_outputs = {}

with open('top_50.csv', 'rt') as csv_file:
    csv_reader = csv.reader(x.replace('\0', '') for x in csv_file)

    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            author = row[1]
            percent = row[0]
            dict_of_outputs[author] = [percent]
        line_count += 1


    print("top_50.csv complete")

with open('top_50_no_lower.csv', 'rt') as csv_file:

    csv_reader = csv.reader(x.replace('\0', '') for x in csv_file)

    line_count = 0
    for row in csv_reader:

        if line_count > 0:
            author = row[0]
            percent = row[1]

            if author in dict_of_outputs:
                dict_of_outputs[author] += [percent]
                
            else:
                dict_of_outputs[author] = ['--'] + [percent]

        line_count += 1


    print("top_50_no_lower.csv complete")

# go through dictionary, and set second value in all lists to '--' since this means this version of the CSV didn't contain these authors
for author, percent in dict_of_outputs.items():
    if len(percent) == 1:
        percent += ['--']

# write CSV with the different files as the columns and '--' substituted if no percent is found
with open('output_comparison.csv', mode = 'w') as csvfile:

    fieldnames = ['Name', 'Normal CSV', 'No-Lower CSV']
    filewriter = csv.DictWriter(csvfile, fieldnames = fieldnames)

    filewriter.writeheader()

    for name, percents in dict_of_outputs.items():
        normal_csv = percents[0]
        no_lower = percents[1]
        author = name

        filewriter.writerow({'Name': author, 'Normal CSV': normal_csv, 'No-Lower CSV': no_lower})

        