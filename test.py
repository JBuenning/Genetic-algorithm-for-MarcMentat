import csv
new = []
with open('penis.csv','r',newline='\n') as file:
    r = csv.reader(file)
    i=0
    for line in r:
        if i == 10:
            new.append(line)
            i = 0
        else:
            i+=1
with open('small_penis.csv','w',newline='\n') as file:
    w = csv.writer(file)
    w.writerows(new)