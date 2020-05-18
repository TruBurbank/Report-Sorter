import pandas as pd
import os

masterlist = input('Enter Master list : ')

noReports = int(input('\nEnter Number of reports: '))

reportlist = [] # array that stores the report names

for i in range(noReports):
    reportlist.append(input('\nEnter Report : '))

dirName = input('\nPlease enter a dir name : ')
print('-------------------------------------')
print("\nMerging the reports into one")
    
master = pd.read_excel(masterlist)


for i in range(noReports):
    report = pd.concat([pd.read_csv(reportlist[j]) for j in range(noReports)]) #the loop converts the report(s) into one single file


masterColumn = master.columns.values.tolist() #Retrives the headers of the master list

ip = 'Asset IP Address'

path = os.path.join(os.getcwd(), dirName)

if os.path.isdir(path):
    print('\nDirectory Already created')
else:
    os.mkdir(path, mode = 0o777) #Makes a directory to store the seperated reports


print("\nSearching for IP addresses for all Columns\n ")
for i in range(len(masterColumn)):
    result = report[report[ip].isin(master[masterColumn[i]])]  #sorts the IPs according to their groups  
    if result.empty != True:
        print("Creating a file for " + masterColumn[i] + "\n")
        reportName = masterColumn[i] + '.csv'
        hdr = False if os.path.exists(os.path.join(path, reportName)) else True #checks if the file exists
        result.to_csv(os.path.join(path, reportName), index=False, header=hdr, mode = 'a') #exports into csv
        print(reportName + ' Created' + "\n")
