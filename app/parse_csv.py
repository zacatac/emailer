import csv,sys
import mandrill



"""
Storing players with X birth month into a dictionary
"""
def find_date(row):
    return row[3].split('-')
    
def birth_month(row,month):
    try:
        if int(find_date(row)[1]) == month:
            return True
    except:
        return False
    return False


def CSV_to_dict(addr):
    email_dict = {}
    f = open(addr, 'rb') # opens the csv file
    try:
        reader = csv.reader(f)  # creates the reader object    
        for row in reader:   # iterates the rows of the file in order
            if birth_month(row,7) and not row[4] == ' ':
                name_tuple = (row[0].title(),row[1].title(),row[-1])
                email_dict[row[4].strip()] = name_tuple
        print(email_dict)

    finally:
        f.close()      # closing    
    return email_dict

