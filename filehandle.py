import PyPDF2
import docx

def pdftolist(filename):
    '''
     a function to convert pdf to list
    :param filename of the pdf:
    :return:contains list of contents of pdf file
    '''
    pdf_file = open("Documents_Uploaded/"+filename, 'rb')
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
    return textlist

def wordtolist(filename):
    '''
     a function to convert word to list
    :param filename of the word:
    :return:contains list of contents of word file
    '''
    word_file = open("Documents_Uploaded/"+filename, 'rb')
    read_word = docx.Document(word_file)
    doc = read_word

    listText = []
    for paragraph in doc.paragraphs:
        listText.append(paragraph.text)
    textlist=list(filter(None, listText))
    textlist[:]=[item for item in textlist if item !=' ']
    return textlist

#print(wordtolist("testdata/Imran-Resume-2020.docx"))

