import csv


with open("users.csv", mode='r') as csvfile:
    readfile = (csv.reader(csvfile))
    outputFile = open("Output-Users.csv", mode='w+')
    writer = csv.writer(outputFile, delimiter=',',
                            quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    linescounted = 0
    with outputFile as output:
            for row in readfile:
                if linescounted == 0:
                    print([f'{row[0]} {row[1]} {row[2]} '+"Email"])
                    writer.writerow([f'ID, {row[1]}, {row[2]},'+ "Email" ])
                else:
                    print([f'{row[0]} {row[1]} {row[2]} {row[1][0]} {row[2]}' + "@email.com"])
                    writer.writerow([f'{row[0]}, {row[1]}, {row[2]}, {row[1][0]}{row[2]}' + "@email.com"])
                linescounted +=1
                

