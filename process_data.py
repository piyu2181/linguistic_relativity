"""
Script: This class contains all the attributes and functions required for preprocessing of the data before
performing linguistic relativity
Author: Debjani Bhowmick, Tilburg University
Year: 2019
"""
import os
import sys

from gensim import models, corpora
import jieba
import re
import numpy as np
from xml.etree import ElementTree

class ProcessData:

    '''
    Attributes:
    min_count: Defines the min. number of documents that contain a certain word; a count below this number would
    ignore the word from the study
    remove_n:
    n_topics:
    n_passes:
    matching_files: stores the paths for all the files of desired languages and years
    data_path: Path for the data; should refer to the path containing folders for languages and years
    '''
    min_count = 5
    remove_n = 50
    n_topics = 10
    n_passes = 20
    matching_files = {}
    data_path = './UN/'
    matching_files = {}

    
    def __init__(self,
                 data_path, languages, years, target_language = "English", process_sign = "temp",
                 min_count = 5, remove_n = 50, n_topics = 10, n_passes = 20):

        self.languages = languages
        self.target_language = target_language
        self.years = years
        self.min_count = min_count
        self.remove_n = remove_n
        self.n_topics = n_topics
        self.n_passes = n_passes
        self.data_path = data_path
        self.process_sign = process_sign

    ## Functions private to the class

    def __get_filepaths(self, directory):
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

    def __clean_text(self, doc, language):
        '''
        This function takes the unprocessed text of a document and strips it of its
        punctuation. It returns the document cleaned and splitted on each word.
        '''
        if language.lower() in ["english", "french", "spanish"]:
            doc = doc.lower()
            # Basic Latin + Latin-1 Supplement without punctuation and numerals
            doc = re.sub(r"[^\u0041-\u005A\u0061-\u007A\u00C0-\u00FF]", " ", doc)
            doc = re.sub(r"(\\n)", " ", doc)
            doc = re.sub(r"\s+", " ", doc)
            doc = doc.split()
            doc = [word for word in doc if len(word) > 1]
        elif language.lower() == "arabic":
            # Arabic subset without numerals and punctuation marks
            doc = re.sub(r"[^\u0621-\u065F]", " ", doc)
            doc = re.sub(r"(\\n)", " ", doc)
            doc = re.sub(r"\s+", " ", doc)
            doc = doc.split()
            doc = [word for word in doc if len(word) > 1]
        elif language.lower() == "chinese":
            # CJK Unified Ideographs subset
            doc = re.sub(r"[^\u4E00-\u9FFF]", " ", doc)
            doc = re.sub(r"\s+", " ", doc)
            doc = jieba.lcut(doc)
        elif language.lower() == "russian":
            # Cyrillic subset without punctuation
            doc = re.sub(r"[^\u0400-\u047F]", " ", doc)
            doc = doc.lower()
            doc = re.sub(r"(\\n)", " ", doc)
            doc = re.sub(r"\s+", " ", doc)
            doc = doc.split()
            doc = [word for word in doc if len(word) > 1]
        return doc

    def __parse_xml(self, file):
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

    def __load_files(self, year, language, matching_files):
        '''
        This function takes a list of .xml files and returns a corpus that is both
        parsed and cleaned.
        '''
        files_list = matching_files[year]
        files_list = [self.data_path + "{}/{}/{}".format(language, year, file)
                      for file in files_list]
        files = []
        for file in files_list:
            f = open(file, "r", encoding="utf8")
            xml = f.read()
            files.append((self.__clean_text(self.__parse_xml(xml), language)))
            f.close()
        files = np.array(files)
        return files


    ## Public functions of the class, accesible only through a class object.

    def find_matching_files(self, save_flag = False, save_fname = ""):
        '''
        This function creates a dictionary containing the filepaths for all
        the files in all the desired languages and desired years
        save_Flag: if True, the matching_files vector is stored in ./temp/matching_files.rxt in human-readable format
        '''

        if save_flag and save_fname == "":
            print("Error! No file name for saving matched files")
            sys.exit(0)

        filepaths = {}
        for language in self.languages:
            filepaths[language] = {}
        for language in self.languages:
            for year in self.years:
                full_path = self.data_path + "{}/{}".format(language, year)
                filepaths[language][year] = self.__get_filepaths(full_path)
                filepaths[language][year] = [file.replace(full_path, "")
                                            for file in filepaths[language][year]]

        matching_files = {}
        # Getting the unique set of names for all the files located
        for year in self.years:
            language_set = dict()
            # Finding the set of unique filenames for each language
            for language in self.languages:
                language_set[language] = set(filepaths[language][year])

            # Update the set for the target language to only contain filenames that are present in all languages
            for language in self.languages:
                language_set[self.target_language].intersection_update(language_set[language])

            # Putting the found filenames into matching_files
            matching_files[year] = list(language_set[self.target_language])

        # Saving the matching_files information
        if save_flag == True:

            if not os.path.exists(self.data_path + 'output/' + self.process_sign + "/"):
                os.makedirs(self.data_path + 'output/' + self.process_sign + "/")

            fid = open(self.data_path + 'output/' + self.process_sign + "/" + save_fname, "w+")

            for i in range(0, len(matching_files)):

                keylist = list(matching_files.keys())
                if not len(matching_files[keylist[i]]) == 0:
                    fid.write(keylist[i] + "\n")
                else:
                    fid.write(keylist[i] + "\n\n")
                for j in range(0, len(matching_files[keylist[i]])):
                    fid.write(matching_files[keylist[i]][j] + "\n")

            fid.close()
        self.matching_files = matching_files

    def prepare_corpus(self):
        '''
        This function converts the data into desired corpus format.
        '''
        # Check and create the temp folder, if does not exist
        temp_save_fpath = self.data_path + 'output/' + self.process_sign + "/temp/"
        if not os.path.exists(temp_save_fpath):
            os.makedirs(temp_save_fpath)

        if not os.path.exists(temp_save_fpath + "dictionary/"):
            os.makedirs(temp_save_fpath + "dictionary/")
        if not os.path.exists(temp_save_fpath + "step1/"):
            os.makedirs(temp_save_fpath + "step1/")
        if not os.path.exists(temp_save_fpath + "step2/"):
            os.makedirs(temp_save_fpath + "step2/")
        for language in self.languages:
            dictionary = corpora.Dictionary()
            for year in self.years:
                corpus = self.__load_files(year, language, self.matching_files)
                dictionary.add_documents(corpus)
                corpus = np.array(corpus)
                np.save(temp_save_fpath + "step1/{}_{}.npy".format(language, year), corpus)
                print("Step 1 completed for {}, {}".format(language, year))

            dictionary.filter_extremes(no_below=self.min_count)
            dictionary.filter_n_most_frequent(remove_n=self.remove_n)
            for year in self.years:
                corpus = np.load(temp_save_fpath + "step1/{}_{}.npy".format(language, year))
                corpus = [dictionary.doc2bow(doc) for doc in corpus]
                np.save(temp_save_fpath + "step2/{}_{}.npy".format(language, year), corpus)
                print("Step 2 completed for {}, {}".format(language, year))
            dictionary.save(temp_save_fpath + "dictionary/{}".format(language))
