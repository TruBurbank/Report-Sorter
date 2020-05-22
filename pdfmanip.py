import pandas as pd
import tabula as tb
import os
from pageFinder import pageFinder as pf

pdflist = input('Enter PDF : ')
masterlist = input('\nEnter Master list : ')
pdfname = pf(pdflist)
initPDF = pdfname.getPDf()
tPages = pdfname.getpdfpages(object= initPDF)
pages = []

for i in range(pdfname.start_page(NumPages=tPages,object= initPDF), pdfname.end_page(NumPages=tPages,object = initPDF)):
    pages.append(i)    # retrives the pages from the pdf report


print('\nFetching Discovered Devices from PDF...')

tb.convert_into(pdflist, 'test.csv', output_format='csv', pages=pages)

print('\nTemporarily saving the data in test.csv')

pdfReport = pd.read_csv('test.csv',  encoding='unicode_escape')

pdfReport = pdfReport.dropna(subset = ['Node'])

master = pd.read_excel(masterlist)

master.applymap(lambda x: x.strip() if isinstance(x, str) else x) #strips the IPs of their spaces(only right spaces for now)

masterColumn = master.columns.values.tolist() #Retrives the headers of the master list

finalColumns = []
convDF = []
# revisedMasterList = pd.read_csv('revisedMasterList.csv')

# the loop fonds the columns corresponding with the IPs

for i in range(len(masterColumn)):
    result = pdfReport[pdfReport['Node'].isin(master[masterColumn[i]])]
    print(result.empty)
    if result.empty != True:
        print(masterColumn[i])
        finalColumns.append(masterColumn[i]) 
        
        
for j in range(len(finalColumns)):
    convDF.append(master[finalColumns[j]])
convDF = pd.DataFrame(convDF)
convDF1 = pd.DataFrame(convDF).stack()

print('\nSearching for Unscanned IP Addresses...')
IPdf = convDF1[~convDF1.isin(pdfReport['Node'])] #retrives the unscanned IPs
columnGroup= []
initialScanStatus = []

for i in range(len(convDF1)):
    for j in range(len(finalColumns)):
        if convDF1.isin(master[finalColumns[j]]).values[i]:
            columnGroup.append(finalColumns[j]) #Sorts the group names according to the location of the unscanned IPs 

for i in range(len(convDF1)):
    #checks if the IPs are unscanned or not 
    if convDF1.isin(IPdf).values[i]:
        initialScanStatus.append('Unscanned')
    else:
        initialScanStatus.append('Scanned')

#concats the created dataframes into one singel dataframe
finalReport = pd.concat([s.reset_index(drop=True)for s in [convDF1, pd.DataFrame(columnGroup),pd.DataFrame(initialScanStatus)]], axis=1)

finalReport.columns = ['IP', 'Group','Initial Scan Status']

print('\nCreating file')

resultFile = 'Scan_Status_Report ' + os.path.splitext(pdflist)[0].replace('PDF', '') + '.csv'

hdr = False if os.path.exists(resultFile) else True

finalReport.to_csv(resultFile, index=False, header=hdr, mode='a')
os.remove('test.csv')
