import PyPDF2


def pdftolist(filename):
    '''
     a function to convert pdf to list
    :param filename of the pdf:
    :return:contains list of contents of pdf file
    '''
    pdf_file = open(filename, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    c = read_pdf.numPages
    txtlist=[]
    texts=""
    for i in range(c):
        page = read_pdf.getPage(i)
        texts = page.extractText()
        texts=str(texts).split("\n")
        txtlist.extend(texts)
    textlist=list(filter(None, txtlist))
    textlist[:]=[item for item in textlist if item !=' ']
    print(textlist)
    return textlist

