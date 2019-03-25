# Libraries -------------------------------------------------------------------

from gensim import models, corpora
import jieba
import numpy as np
import os
import re
from xml.etree import ElementTree

# To Do List ------------------------------------------------------------------

'''
Te veel files matchen
'''

# Parameters ------------------------------------------------------------------

# Amount of languages and years to process
languages = ["french", "spanish", "chinese", "arabic", "russian"]
years = ["1990", "1991", "1992", "1993", "1994", "1995", "1996", 
         "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", 
         "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012",
         "2013", "2014"]

# Set minimum amount of documents a word has to be in, and the amount of top
# n frequent words to remove
no_below = 5
remove_n = 50

# Set the amount of topics and passes
num_topics = [10]  
passes = 20

# Main ------------------------------------------------------------------------

def process():
    preprocess(languages, years, no_below, remove_n)
def analysis():
    lda(languages, years, num_topics, passes)
def compare():
    compare_output("output_translated")    
    
# Functions -------------------------------------------------------------------

def calc_eucl_dist(list1, list2):
    '''
    This function returns a simple euclidean distance between two lists.
    '''
    match = 0
    for item in list1:
        if item in list2:
            match += 1
    return (match/len(list1))

def clean_text(doc, language):
    '''
    This function takes the unprocessed text of a document and strips it of its
    punctuation. It returns the document cleaned and splitted on each word.
    '''
    if language in ["english", "french", "spanish"]:
        doc = doc.lower()
        # Basic Latin + Latin-1 Supplement without punctuation and numerals
        doc = re.sub(r"[^\u0041-\u005A\u0061-\u007A\u00C0-\u00FF]", " ", doc)
        doc = re.sub(r"(\\n)", " ", doc)
        doc = re.sub(r"\s+", " ", doc)
        doc = doc.split()
        doc = [word for word in doc if len(word) > 1]
    elif language == "arabic":
        # Arabic subset without numerals and punctuation marks
        doc = re.sub(r"[^\u0621-\u065F]", " ", doc) 
        doc = re.sub(r"(\\n)", " ", doc)
        doc = re.sub(r"\s+", " ", doc)
        doc = doc.split()
        doc = [word for word in doc if len(word) > 1]
    elif language == "chinese":
        # CJK Unified Ideographs subset
        doc = re.sub(r"[^\u4E00-\u9FFF]", " ", doc) 
        doc = re.sub(r"\s+", " ", doc)
        doc = jieba.lcut(doc)                
    elif language == "russian":
        # Cyrillic subset without punctuation
        doc = re.sub(r"[^\u0400-\u047F]", " ", doc) 
        doc = doc.lower()
        doc = re.sub(r"(\\n)", " ", doc)
        doc = re.sub(r"\s+", " ", doc)
        doc = doc.split()
        doc = [word for word in doc if len(word) > 1]
    return doc

def compare_output(folder):
    '''
    This function generated a table of euclidean distances between every
    file that the provided folder contains.
    '''
    languages = ["english", "french", "spanish", 
                 "chinese", "arabic", "russian"]
    table = {}
    for i in languages:
        table[i] = {}
        for j in languages:
            list1 = load_output("{}/{}.txt".format(folder, i))
            list2 = load_output("{}/{}.txt".format(folder, j))
            table[i][j] = calc_eucl_dist(list1, list2)
    return table

'''###### Can save this table: debjani####'''
def find_matching_files():
    '''
    This function returns a dictionary containing the filepaths for
    all files that are available in all six languages.
    '''
    print("Finding matching files...")
    languages = ["English", "Arabic", "Chinese", 
                 "Russian", "Spanish", "French"]
    years = ["1990", "1991", "1992", "1993", "1994", "1995", "1996", 
             "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", 
             "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012",
             "2013", "2014"]
    filepaths = {}
    for language in languages:
        filepaths[language] = {}
    for language in languages:
        for year in years:
            filepaths[language][year] = get_filepaths(
                                        "UN/{}/{}".format(language, year))
            filepaths[language][year] = [file[file.index('\\')+1:] 
                                        for file in filepaths[language][year]]
    matching_files = {}
    for year in years:
        set1 = set(filepaths["English"][year])
        set2 = set(filepaths["Arabic"][year])
        set3 = set(filepaths["Chinese"][year])
        set4 = set(filepaths["Russian"][year])
        set5 = set(filepaths["Spanish"][year])
        set6 = set(filepaths["French"][year])
        set1.intersection_update(set2, set3, set4, set5, set6)
        matching_files[year] = list(set1)
    return matching_files

def get_filepaths(directory):
    '''
    This function searches a directory for all .xml files it and its subfolders
    contain.
    '''
    filepaths = []
    for root, directory, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith(".xml"):
                filepaths.append(path)
    return filepaths

def load_files(year, language, matching_files):
    '''
    This function takes a list of .xml files and returns a corpus that is both 
    parsed and cleaned.    
    '''
    files_list = matching_files[year]
    files_list = ["UN/{}/{}/{}".format(language, year, file) 
                  for file in files_list]
    files = []
    for file in files_list:
        f = open(file, "r", encoding = "utf8")
        xml = f.read()
        files.append((clean_text(parse_xml(xml), language)))
        f.close()
    files = np.array(files)
    return files

def load_output(file):
    '''
    This function reads the encoded output file and outputs it into a splitted
    list.
    '''
    f = open(file, "r", encoding = "utf-8")
    output = f.read()
    output = output.split(",")
    output = [word.lower() for word in output if word != ""]
    f.close()
    return output

def lda(languages, years, num_topics, passes):
    '''
    This function performs the Latent Dirichlet Allocation algoritm and saves
    both the output and the model to a file.
    '''
    for language in languages:
        for n in num_topics:
            dictionary = corpora.Dictionary()
            dictionary = dictionary.load("temp/dictionary/{}".format(language))
            model = models.LdaModel(num_topics = n, update_every = 1,
                                    id2word = dictionary)
            for i in range(1, passes+1):
                for year in years:
                    corpus = np.load("temp/step2/{}_{}.npy".format(language, year))
                    if len(corpus) == 1:
                        corpus = reshape_corpus(corpus)
                    model.update(corpus)
                    print("Pass {} completed for {}, {}, {} topics".format(i, language, year, n))
            model.save("temp/models/{}_{}".format(language, n))

            write_output("output/{}_topics/{}.txt".format(n, language), model, language) 
            
            
'''save the output in a different folde:Debjani'''
            
def parse_xml(file):
    '''
    This function searches a .xml file for its body context and returns it as
    plain text.
    '''
    body = ""
    try:
        cue = ElementTree.fromstring(file).find("text/body")
        if cue:
            for line in cue.itertext():
                body += repr(line)
    except ElementTree.ParseError:
        print("ParseError")
    return body

def preprocess(languages, years, no_below, remove_n):
    '''
    This function: parses each XML file, cleans the text, constructs a 
    dictionary, converts the text in a term frequency array and saves in 
    a numpy array.
    '''
    matching_files = find_matching_files()
    
    for language in languages:
        dictionary = corpora.Dictionary()
        for year in years:
            corpus = load_files(year, language, matching_files)
            dictionary.add_documents(corpus)
            corpus = np.array(corpus)
            np.save("temp/step1/{}_{}.npy".format(language, year), corpus)
            print("Step 1 completed for {}, {}".format(language, year))
        dictionary.filter_extremes(no_below = no_below)
        dictionary.filter_n_most_frequent(remove_n = remove_n)
        for year in years:
            corpus = np.load("temp/step1/{}_{}.npy".format(language, year))
            corpus = [dictionary.doc2bow(doc) for doc in corpus]
            np.save("temp/step2/{}_{}.npy".format(language, year), corpus)
            print("Step 2 completed for {}, {}".format(language, year))
        dictionary.save("temp/dictionary/{}".format(language))
        
def reshape_corpus(corpus):
    '''
    This function shapes the corpus the correct way, even if only one file is
    present.
    '''
    new_corpus = []
    corpus = np.squeeze(corpus)
    for j in corpus:
        new_corpus.append(tuple(j))
    new_corpus = [new_corpus,]
    return new_corpus
            
def write_output(name, model, language):
    '''
    This function writes the topics of the trained model to a comma separated
    file.
    '''
    topics = model.print_topics(-1)
    topics = [x[1] for x in topics]
    topics = [x.split(" + ") if "+" in x else x for x in topics]
    if language in ["english", "french", "spanish"]:
        topics = [[re.sub("[^a-zéáíóúýàèùìòâêîôûäëïöüÿœæñç]", "", x) for x in y] for y in topics]
    elif language == "arabic":
        topics = [[re.sub("[^\u0621-\u064A]", "", x) for x in y] for y in topics]
    elif language == "russian":
        topics = [[re.sub("[^\u0400-\u045F]", "", x) for x in y] for y in topics]
    elif language == "chinese":
        topics = [[re.sub("[^\u4E00-\u9FFF]", "", x) for x in y] for y in topics]
    output = ""
    for topic in topics:
        for word in topic:
            output += word
            output += ","
    f = open(name, "wb")     
    f.write(output.encode("utf-8"))
    f.close()