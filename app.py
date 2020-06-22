from flask import Flask, render_template, request
import os
import pickle
import filetype
import filehandle
import magic
app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def file():
    if request.method == 'POST':
        file = request.files['file']
        file.save("Documents_Uploaded/"+file.filename)
        file_error = "Not a valid document type \n Please select PDF or WORD"
        FileType = []
        try:
            FileType = magic.from_file("Documents_Uploaded/"+file.filename)
        except:
            return render_template('index.html', err=file_error)
        FileTypeArray = []
        FileTypeArray=FileType.split(" ")
        if "Word" in FileTypeArray:
            tags=predict(filehandle.wordtolist(filename=file.filename),"Word")
            return render_template('index.html', tag=tags)
        elif "MP4" in FileTypeArray:
            #return render_template('index.html', err="MP4 File")
            return render_template('index.html', err=file_error)
        elif "PDF" in FileTypeArray:
            tags=predict(filehandle.pdftolist(filename=file.filename),"PDF")
            return render_template('index.html', tag=tags)
        elif "JPEG" in FileTypeArray:
            #return render_template('index.html', err="JPEG File")
            return render_template('index.html', err=file_error)
        elif "PowerPoint" in FileTypeArray:
            #return render_template('index.html', err="PowerPoint File")
            return render_template('index.html', err=file_error)
        elif "Zip" in FileTypeArray:
            ''' Certain Word Files formats are ZIP format '''
            try:
                tags=predict(filehandle.wordtolist(filename=file.filename),"Word")
                return render_template('index.html', tag=tags)
            except:
                #return render_template('index.html', err="Zip File")
                return render_template('index.html', err=file_error)
        else:
            #return render_template('index.html', err="Unknow File Format")
            return render_template('index.html', err=file_error)

def predict(textlist,format_name):
    '''
    a function that prefictes the given file to which tag does it belong
    :param textlist:
    :return:
    '''
    with open('classification_model', 'rb') as file:
        classi_model = pickle.load(file)
    return add_freq_element(classi_model.predict(textlist).tolist(),format_name)

def add_freq_element(predict_list,format_name):
    '''
    function to find the highest frequency and map to the tags
    :param predict_list:
    :return:
    '''
    tag_value=max(predict_list,key=predict_list.count)
    l=['Business','Entertainment','Politics','Sport','Tech']
    tags="Your "+format_name+" file belongs to "+l[tag_value]+" Tag"
    return tags


if __name__ == "__main__":
    app.run(debug=True)
