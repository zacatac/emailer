import csv,sys

def find_date(row):
    return row[3].split('-')

def find_year(row):
    date = row[3].split('-')
    year = date[0]
    return year
    
def birth_month(row,month):
    try:
        int(find_date(row)[1])
    except:
        return False
    if int(find_date(row)[1]) == month:
        return True
    return False

email_dict = {}
f = open(sys.argv[1], 'rb') # opens the csv file
try:
    reader = csv.reader(f)  # creates the reader object    
    for row in reader:   # iterates the rows of the file in orders
        if birth_month(row,7) and not row[4] == ' ':
            name_tuple = (row[0].title(),row[1].title(),row[-1])
            email_dict[row[4].strip()] = name_tuple
    print(email_dict)
finally:
    f.close()      # closing
