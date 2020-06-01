import pandas as pd
from PyPDF2 import PdfFileMerger
import matplotlib.pyplot as plt
import numpy as np
import os

ScanList = input('\nEnter final status scan file: ')

hml = pd.read_csv(input('Enter severity score file: '))

hml = hml.drop(['Total'], axis = 1)
hmlname = [hml['Series'].iloc[i] for i in range(len(hml))]
ScanList = pd.read_excel(ScanList)

scannedList = []
unscannedList = []
seriesList = []
for i in range(len(ScanList['Final Status'])):
     
    if ScanList['Final Status'].iloc[i] == 'Scanned':
        scannedList.append(ScanList['IP'].iloc[i])
    else:
        unscannedList.append(ScanList['IP'].iloc[i])

uniqueList = ScanList['Grp'].unique()

for i in range(len(ScanList['Grp'].unique())):
    seriesList.append(uniqueList[i])
    
    
ratio = len(scannedList)/len(unscannedList)
        
scannedList = pd.DataFrame(scannedList).count()
unscannedList = pd.DataFrame(unscannedList).count()

totalCount = pd.concat([s.reset_index(drop=True)for s in [scannedList, unscannedList]], axis=1)
totalCount.columns = ['Scanned', 'Unscanned']
seriesList = pd.DataFrame(seriesList)
print(seriesList)
Barsize = pd.DataFrame()
scannedList1 = []
unscannedList1 = []

Barsize = pd.crosstab(ScanList.Grp, ScanList['Final Status'].str.capitalize())
print(Barsize)

print(Barsize.columns)

plt.rcParams.update({'font.size': 30})
totalCount.columns = ['Scanned', 'Unscanned']
piePlot = totalCount.plot.bar(title='Overall Scan Status', figsize=(45, 45))
piePlot.set_xlabel('Total Scanned and Unscanned')
piePlot.set_ylabel('Asset')
piePlot.set_xticklabels([''])

for p in piePlot.patches:
    piePlot.annotate(np.round(p.get_height(), decimals=2), (p.get_x()+p.get_width()/2.,
                                                            p.get_height()), ha='center', va='center', xytext=(0,10), textcoords='offset points')

piePlot.get_figure().savefig('pie.pdf')
index = [seriesList[0].iloc[i] for i in range(len(seriesList))]
BarFrame = pd.DataFrame(data=Barsize )

barPlot = BarFrame.plot.bar(
    title='Series Scan', figsize=(45, 45))
barPlot.set_xlabel('Groups')
barPlot.set_ylabel('Assets')
barPlot.set_xticklabels(seriesList[0], rotation=360)

barPlot.get_figure().savefig('bar.pdf')

hmlplot = hml.plot.bar(
    title='HML Graph', figsize=(45, 45), width = 0.5,align='center')
hmlplot.set_xlabel('Groups')
hmlplot.set_ylabel('Assets')

hmlplot.set_xticklabels(hml.Series, rotation = 360)
for p in hmlplot.patches:
    hmlplot.annotate(np.round(p.get_height(), decimals=2), (p.get_x()+p.get_width()/2.,
                                                            p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

for p in barPlot.patches:
    barPlot.annotate(np.round(p.get_height(), decimals=2), (p.get_x()+p.get_width()/2.,
                                                       p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')

hmlplot.get_figure().savefig('hml.pdf')

pdfs = ['hml.pdf','bar.pdf','pie.pdf']

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")
merger.close()
os.remove('pie.pdf')
os.remove('hml.pdf')
