import pandas as pd
import os
import logging as lg
from datetime import datetime

masterlist = input('Enter Master list : ')

lg.basicConfig(filemode='a',filename= 'Log_file.log', level=lg.INFO)
lg.info(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) +
        '\t Inititated')
noReports = int(input('\nEnter Number of reports: '))
lg.info(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + '\t'  + str(noReports) + ' number of report(s)')

reportlist = [] # array that stores the report names

for i in range(noReports):
    reportlist.append(input('\nEnter Report : '))


lg.info(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + '\t' + str(noReports) + ' report(s) inserted')
dirName = input('\nPlease enter a dir name : ')
print('-------------------------------------')
print("\nMerging the reports into one")



master = pd.read_excel(masterlist)
lg.info(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + '\tMaster List read')

for i in range(noReports):
    report = pd.concat([pd.read_csv(reportlist[j]) for j in range(noReports)]) #the loop converts the report(s) into one single file

lg.info(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + '\treports merged')

total_Count = report['Asset IP Address'].count()

masterColumn = master.columns.values.tolist() #Retrieves the headers of the master list

ip = 'Asset IP Address'

path = os.path.join(os.getcwd(), dirName)

if os.path.isdir(path):
    print('\nDirectory Already created')
    lg.info(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + '\tDirectory Exists, using the same directory')
else:
    os.mkdir(path, mode = 0o777) #Makes a directory to store the seperated reports
    lg.info(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + '\tNew Directory Created')

reports_name = ''

for i in reportlist:
    reports_name += i + ', '



lg.info(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + '\t' + str(total_Count) + ' total vulnerabilties in ' + "'%s'" %reports_name)

print("\nSearching for IP addresses for all Columns\n ")
for i in range(len(masterColumn)):
    result = report[report[ip].isin(master[masterColumn[i]])]  #sorts the IPs according to their groups  
    if result.empty != True:
        series_count = result['Asset IP Address'].count()
        reportName = masterColumn[i] + '.csv'
        hdr = False if os.path.exists(os.path.join(path, reportName)) else True #checks if the file exists
        result.to_csv(os.path.join(path, reportName), index=False, header=hdr, mode = 'a') #exports into csv
        print(reportName + ' Created' + "\n")
        lg.info(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\t" + reportName + ' Created at ' + os.path.join(path, reportName) )
        lg.info(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) +
                "\t" + reportName + ' count : ' + str(series_count))

lg.info('\n')
