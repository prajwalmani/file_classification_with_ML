from flask import Flask, render_template, request
import os
import pickle
import filetype
import filehandle
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
        file.save(file.filename)
        # with open(file.filename ,encoding='iso8859-1') as f:
        #     linelist=f.readlines()
        #     print(linelist)
        file_error = "Not a valid document type \n Please select pdf or word"
        try:
            kind = filetype.guess(file.filename).extension
        except:
            return render_template('index.html', err=file_error)
        if kind == 'pdf':
          tags=predict(filehandle.pdftolist(filename=file.filename))
        else:
            try:
                print(filetype.guess_extension(file.filename))
            except:
                return render_template('index.html', err=file_error)
        return render_template('index.html', tag=tags)

def predict(textlist):
    '''
    a function that prefictes the given file to which tag does it belong
    :param textlist:
    :return:
    '''
    with open('classification_model', 'rb') as file:
        classi_model = pickle.load(file)
    #print(classi_model.predict(textlist).tolist())
    return add_freq_element(classi_model.predict(textlist).tolist())

def add_freq_element(predict_list):
    '''
    function to find the highest frequency and map to the tags
    :param predict_list:
    :return:
    '''
    tag_value=max(predict_list,key=predict_list.count)
    l=['business','entertainment','politics','sport','tech']
    tags="Your file belongs to "+l[tag_value]+"tag"
    return tags


if __name__ == "__main__":
    app.run(debug=True)
