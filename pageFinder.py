import PyPDF2
import re

class pageFinder:
    
    startString = "2. Discovered System"
    endString = "3. Discovered and Potential Vulnerabilities"
    pdfname = ''
    
    def __init__(self, pdfname):
        self.pdfname = pdfname
        
    def getPDf(self):
        object = PyPDF2.PdfFileReader(self.pdfname)
        return(object)
        
    def getpdfpages(self, object):
        NumPages = object.getNumPages()
        return(NumPages)

    def start_page(self, NumPages, object):
        
        for i in range(0, NumPages):
            PageObj = object.getPage(i)
            Text = PageObj.extractText()
            if re.search(pageFinder.startString, Text):
                start_page = i + 1
        
        return(start_page)
                
    def end_page(self, NumPages, object):
        for i in range(0, NumPages):
            PageObj = object.getPage(i)
            Text = PageObj.extractText()
            if re.search(pageFinder.endString, Text):
                end_page = i + 1
        return(end_page)

