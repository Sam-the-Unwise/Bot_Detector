import csv

dict_of_outputs = {}

with open('top_50_II.csv', 'rt') as csv_file:
    csv_reader = csv.reader(x.replace('\0', '') for x in csv_file)

    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            author = row[0]
            percent = row[1]
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

with open('top_75.csv', 'rt') as csv_file:

    csv_reader = csv.reader(x.replace('\0', '') for x in csv_file)

    line_count = 0
    for row in csv_reader:

        if line_count > 0:
            author = row[0]
            percent = row[1]

            if author in dict_of_outputs:
                dict_of_outputs[author] += [percent]
                
            else:
                dict_of_outputs[author] = ['--'] + ['--'] + [percent]

        line_count += 1


    print("top_75.csv complete")

# go through dictionary, and set second value in all lists to '--' since this means this version of the CSV didn't contain these authors
for author, percent in dict_of_outputs.items():
    if len(percent) == 2:
        percent += ['--']


with open('50-74_comments.csv', 'rt') as csv_file:

    csv_reader = csv.reader(x.replace('\0', '') for x in csv_file)

    line_count = 0
    for row in csv_reader:

        if line_count > 0:
            author = row[0]
            percent = row[1]

            if author in dict_of_outputs:
                dict_of_outputs[author] += [percent]
                
            else:
                dict_of_outputs[author] = ['--'] + ['--'] + ['--'] + [percent]

        line_count += 1


    print("50-74_comments.csv complete")

# go through dictionary, and set second value in all lists to '--' since this means this version of the CSV didn't contain these authors
for author, percent in dict_of_outputs.items():
    if len(percent) == 3:
        percent += ['--']

# write CSV with the different files as the columns and '--' substituted if no percent is found
with open('output_comparison.csv', mode = 'w') as csvfile:

    fieldnames = ['Name', 'Reg', 'No-Lower', 'Different COS 75', 'Different COS 50']
    filewriter = csv.DictWriter(csvfile, fieldnames = fieldnames)

    filewriter.writeheader()

    for name, percents in dict_of_outputs.items():
        author = name
        normal_csv = percents[0]
        no_lower = percents[1]
        cos_75 = percents[2]
        cos_50 = percents[3]

        print(percents[0])
        
        filewriter.writerow({'Name': author, 'Reg': normal_csv, 'No-Lower': no_lower, 'Different COS 75': cos_75, 'Different COS 50': cos_50})

        