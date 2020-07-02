import re # Regular Expression Library
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Cleaning Text List
def clean_textlist(textlist):
    new_textlist = []
    for text in textlist:
        new_textlist.append(preprocess(text))
    print("Cleaned Text List Ready")
    return new_textlist

# Filtering Words
def filtering_words(text):
    words = text.split()
    new_words_list = []
    for word in words:
        if word not in stop_words:
            word = stemmer.stem(word)
            word = lemmatizer.lemmatize(word, pos ='v')
            new_words_list.append(word)
    return " ".join(new_words_list)

# Method to Cleaning the text content
def preprocess(text):
    text = text.lower()
    # Using Regular Expression to replace non-alphabets with null
    text = clean_text(text)
    text = re.sub('[^a-zA-Z ]','',text)
    text = filtering_words(text)
    return text

# Rephrasing certain text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip(' ')
    return text

def call_textprocess_func(text):
    '''
    function to call other main functions
    :param text:
    :return text:
    '''
    text=clean_textlist(text)
    text=filtering_words(text)
    text=preprocess(text)
    text=clean_text(text)
    return text
