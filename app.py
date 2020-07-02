from flask import Flask, render_template, request  # Flask Library
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer  # sklearn Library
import pickle  # Read Pickle File
import filetype
import filehandle  # Import filehandle.py -- Read PDF & WORD
import textprocessor_ML  # Import textprocess_ML.py -- Preprocess clean text list
import magic  # Checks for file Format

app = Flask(__name__)
from datetime import datetime


# GET Default Route
@app.route('/')
def index():
    return render_template('index.html')


# GET | POST Predict Route
@app.route('/predict', methods=['GET', 'POST'])
def file():
    if request.method == 'POST':
        # Start Time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        # File Request
        file = request.files['file']
        file.save("Documents_Uploaded/" + file.filename)
        file_error = "Not a valid document type \n Please select PDF or WORD"
        FileType = []

        # Error Check for Documents_Upload Folder
        try:
            FileType = magic.from_file("Documents_Uploaded/" + file.filename)
        except:
            return render_template('index.html', err=file_error, filename=file.filename)

        # File Format Check    
        FileTypeArray = []
        FileTypeArray = FileType.split(" ")

        # Format: WORD
        if "Word" in FileTypeArray:
            try:
                # Predict WORD CONTENT
                tags = predict(filehandle.wordtolist(filename=file.filename), now)
                return render_template('index.html', tag1=tags[0][0], tag2=tags[0][1], filename=file.filename,
                                       format="WORD", duration=tags[1])
            except:
                # Error Reading WORD CONTENT
                return render_template('index.html', err=file_error, filename=file.filename, format="WORD")

        # Format: PDF
        elif "PDF" in FileTypeArray:
            try:
                # Predict PDF CONTENT
                tags = predict(filehandle.pdftolist(filename=file.filename), now)
                return render_template('index.html', tag1=tags[0][0], filename=file.filename,
                                       format="PDF", duration=tags[1])
            except:
                # Error Reading PDF CONTENT
                file_error = "This PDF file has no content in it"
                return render_template('index.html', err=file_error, filename=file.filename, format="PDF")

        # Format: ZIP or WORD
        elif "Zip" in FileTypeArray:

            ''' Certain Word Files formats are ZIP format '''

            try:
                # Predict WORD / ZIP CONTENT
                tags = predict(filehandle.wordtolist(filename=file.filename), now)
                return render_template('index.html', tag1=tags[0][0], tag2=tags[0][1], filename=file.filename,
                                       format="WORD", duration=tags[1])
            except:

                # Not a PDF / WORD CONTENT
                return render_template('index.html', err=file_error, filename=file.filename, format="ZIP")

        # Format: Unknow
        else:
            try:
                # Predict WORD / Unknow CONTENT
                tags = predict(filehandle.wordtolist(filename=file.filename), now)
                return render_template('index.html', tag1=tags[0][0], tag2=tags[0][1], filename=file.filename,
                                       format="WORD", duration=tags[1])
            except:

                # Not a PDF / WORD CONTENT
                return render_template('index.html', err=file_error, filename=file.filename, format="Unknow Format")


# Predicting Content
def predict(textlist, now):
    '''
    A function that predicts the given file to which tag does it belong
    :param textlist:
    :param now:
    :return:
    '''
    # Cleans Text List
    textlist_clean = textprocessor_ML.call_textprocess_func(textlist)

    # load  Naive Bayes Model
    with open('classification_model', 'rb') as file:
        NB_model = pickle.load(file)

    # Predict Naive Bayes Model
    Naive_Bayes_Tag = add_freq_element(NB_model.predict(textlist_clean).tolist(), "Naive Bayes")


    # Calculate Time Taken to Complete Prediction
    later = datetime.now()
    duration = str(later - now)
    duration = duration.split(".")[0]

    # Predicted Tags
    alltags = [Naive_Bayes_Tag]
    result = [alltags, duration]

    # Return Required Data
    return result


def add_freq_element(predict_list, model_name):
    ''' Function to find the highest frequency and map to the Tags '''

    tag_value = max(predict_list, key=predict_list.count)
    tag_list = ['Business', 'Entertainment', 'Politics', 'Sport', 'Technology']
    tags = tag_list[tag_value]

    # Completion of Prediction Model
    print(model_name, "Tag Count Ready")

    return tags


if __name__ == "__main__":
    app.run(debug=True)