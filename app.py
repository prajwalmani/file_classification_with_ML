from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import os
import pickle
import filetype
import filehandle
import textprocess_ML
import magic
app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from datetime import datetime

@app.route('/')
def testindex():
    return render_template('page.html')


@app.route('/predict', methods=['GET', 'POST'])
def file():
    if request.method == 'POST':
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        file = request.files['file']
        file.save("Documents_Uploaded/"+file.filename)
        file_error = "Not a valid document type \n Please select PDF or WORD"
        FileType = []
        try:
            FileType = magic.from_file("Documents_Uploaded/"+file.filename)
        except:
            return render_template('page.html', err=file_error)
        FileTypeArray = []
        FileTypeArray=FileType.split(" ")
        if "Word" in FileTypeArray:
            tags=predict(filehandle.wordtolist(filename=file.filename),now)
            try:
                return render_template('page.html', tag1=tags[0][0],tag2=tags[0][1],filename=file.filename,format="WORD",duration1=tags[1],duration2=tags[2])
            except:
                return render_template('page.html', err=file_error)
        elif "PDF" in FileTypeArray:
            try:
                tags=predict(filehandle.pdftolist(filename=file.filename),now)
                return render_template('page.html', tag1=tags[0][0],tag2=tags[0][1],filename=file.filename,format="PDF",duration1=tags[1],duration2=tags[2])
            except:
                file_error = "This PDF file has no content in it"
                return render_template('page.html', err=file_error)
        elif "Zip" in FileTypeArray:
            ''' Certain Word Files formats are ZIP format '''
            try:
                tags=predict(filehandle.wordtolist(filename=file.filename),now)
                return render_template('page.html', tag1=tags[0][0],tag2=tags[0][1],filename=file.filename,format="WORD",duration1=tags[1],duration2=tags[2])
            except:
                #return render_template('index.html', err="Zip File")
                return render_template('page.html', err=file_error)
        else:
            try:
                tags=predict(filehandle.wordtolist(filename=file.filename),now)
                return render_template('page.html', tag1=tags[0][0],tag2=tags[0][1],filename=file.filename,format="WORD",duration1=tags[1],duration2=tags[2])
            except:
                #return render_template('index.html', err="Unknow File Format")
                return render_template('page.html', err=file_error)

def predict(textlist,now):
    '''
    a function that prefictes the given file to which tag does it belong
    :param textlist:
    :return:
    '''
    with open('vectorizer.pickle', 'rb') as file:
        vectorizer = pickle.load(file)

    textlist_clean=textprocess_ML.clean_textlist(textlist)
    textlist_vec=vectorizer.transform(textlist_clean)

    with open('1NB_model', 'rb') as file:
        NB_model = pickle.load(file)
    with open('2DT_model', 'rb') as file:
        DT_model = pickle.load(file)

    Tag1 = add_freq_element(NB_model.predict(textlist_vec).tolist(),"Naive Bayes")

    later1 = datetime.now()
    duration1 = str(later1-now)
    duration1 = duration1.split(".")[0]

    Tag2 = add_freq_element(DT_model.predict(textlist_vec).tolist(),"Decision Tree")

    later2 = datetime.now()
    duration2 = str(later2-now)
    duration2 = duration2.split(".")[0]

    alltags = [Tag1,Tag2]

    result = [alltags,duration1,duration2]
    return result

def add_freq_element(predict_list,model_name):
    '''
    function to find the highest frequency and map to the tags
    :param predict_list:
    :return:
    '''
    print(model_name,"Tag Count Ready")
    tag_value=max(predict_list,key=predict_list.count)
    l=['Business','Entertainment','Politics','Sport','Technology']
    tags=l[tag_value]

    return tags


if __name__ == "__main__":
    app.run(debug=True)
