import PyPDF2   # PDF Reader Library
import docx     # WORD Reader Library

def pdftolist(filename):

    ''' A function to convert PDF CONTENT to LIST '''

    # Loads the PDF Document
    pdf_file = open("Documents_Uploaded/"+filename, 'rb')

    # Reads the PDF Document
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    c = read_pdf.numPages

    # Make PDF CONTENT into LIST
    txtlist=[]
    texts=""
    for i in range(c):
        page = read_pdf.getPage(i)
        texts = page.extractText()
        texts=str(texts).split("\n\n")
        txtlist.extend(texts)
    textlist=list(filter(None, txtlist))
    textlist[:]=[item for item in textlist if item !=' ']

    # LIST READY of PDF FORMAT
    print("Reading PDF Complete")

    # Return the TEXTLIST
    return textlist

def wordtolist(filename):

    ''' A function to convert WORD CONTENT to LIST '''

    # Loads the WORD Document
    word_file = open("Documents_Uploaded/"+filename, 'rb')

    # Reads the WORD Document
    read_word = docx.Document(word_file)
    doc = read_word

    # Make WORD CONTENT into LIST
    listText = []
    for paragraph in doc.paragraphs:
        listText.append(paragraph.text)
    textlist=list(filter(None, listText))
    textlist[:]=[item for item in textlist if item !=' ']

    # LIST READY of WORD FORMAT
    print("Reading WORD Complete")

    # Return the TEXTLIST
    return textlist



