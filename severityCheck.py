import pandas as pd
import os

reportlist = []
masterlist = input('\nEnter Master list : ')
reportname = input('\nEnter Report : ')
# for i in range(noReports):
#     reportlist.append(input('\nEnter Report : '))
    
# for i in range(noReports):
#     report = pd.concat([pd.read_csv(reportlist[j]) for j in range(noReports)])
report = pd.read_csv(reportname)
master = pd.read_excel(masterlist)
masterColumn = master.columns.values.tolist()
a = report['Vulnerability CVSSv3 Score'] 

seriesGroup = []

for i in range(len(masterColumn)):
    result = report[report['Asset IP Address'].isin(master[masterColumn[i]])]
    if result.empty != True:
        seriesGroup.append(masterColumn[i])
                 
lowScore = []
mediumScore = []
highScore = []
criticalScore = []
informationalScore = []

for i in range(len(a)):
    if (a[i] > 0 and a[i] < 4.0):
        lowScore.append(a[i])
    elif (a[i] >= 4.0 and a[i] < 7.0):
        mediumScore.append(a[i])
    elif (a[i] >= 7.0 and a[i] < 9.0):
        highScore.append(a[i])
    elif (a[i] >= 9.0 and a[i] < 10.1):
        criticalScore.append(a[i])
    else:
        informationalScore.append(a[i])
totalcount = pd.concat([pd.DataFrame(lowScore), pd.DataFrame(mediumScore), pd.DataFrame(highScore), pd.DataFrame(criticalScore), pd.DataFrame(informationalScore)]).count()

finalReport = pd.concat([s.reset_index(drop=True)
                         for s in [pd.DataFrame(seriesGroup), pd.DataFrame([len(criticalScore)]), pd.DataFrame([len(highScore)]), pd.DataFrame([len(mediumScore)]), pd.DataFrame([len(lowScore)]), pd.DataFrame([len(informationalScore)]), totalcount]], axis=1)
finalReport.columns = ['Series','Critical', 'High', 'Medium', 'Low','Informational','Total']
reportName = 'Severity Scores.csv' 
hdr = False if os.path.exists(reportName) else True
finalReport.to_csv(reportName, index=False, header=hdr, mode='a')
