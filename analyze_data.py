"""
Script: This class contains all the attributes and functions required for the analysis of data
Author: Debjani Bhowmick, Tilburg University
Year: 2019
"""

import os
import sys
import re

from gensim import models, corpora

import numpy as np
import process_data

class AnalyzeData:

    '''
    Attributes:

    '''

    def __init__(self, obj_prd, algorithm="lda", num_passes = 20, num_topics = 5):
        '''
        :param
        obj_prd: Object of Process data class already initialized with the required parameters
        num_passes:
        num_topics:

        :return: nothing
        '''

        self.obj_prd = obj_prd
        self.algorithm = algorithm.lower()

        self.num_passes = num_passes
        self.num_topics = num_topics
        self.languages = obj_prd.languages
        self.years = obj_prd.years
        self.data_path = obj_prd.data_path
        self.process_sign = obj_prd.process_sign

    def __init__(self, languages, years, data_path, process_sign, algorithm="lda", num_passes = 20, num_topics = 5):
        '''
        :param
        obj_prd: Object of Process data class already initialized with the required parameters
        num_passes:
        num_topics:

        :return: nothing
        '''

        self.algorithm = algorithm.lower()

        self.num_passes = num_passes
        self.num_topics = num_topics
        self.languages = languages
        self.years = years
        self.data_path = data_path
        self.process_sign = process_sign

    ## Private functions of the class

    def __reshape_corpus(self, corpus):
        '''
        This function shapes the corpus the correct way, even if only one file is
        present.
        '''
        new_corpus = []
        corpus = np.squeeze(corpus)
        for j in corpus:
            new_corpus.append(tuple(j))
        new_corpus = [new_corpus, ]
        return new_corpus

    def __write_output(self, name, model, language):
        '''
        This function writes the topics of the trained model to a comma separated
        file.
        '''
        topics = model.print_topics(-1)
        topics = [x[1] for x in topics]
        topics = [x.split(" + ") if "+" in x else x for x in topics]
        if language.lower() in ["english", "french", "spanish"]:
            topics = [[re.sub("[^a-zéáíóúýàèùìòâêîôûäëïöüÿœæñç]", "", x) for x in y] for y in topics]
        elif language.lower() == "arabic":
            topics = [[re.sub("[^\u0621-\u064A]", "", x) for x in y] for y in topics]
        elif language.lower() == "russian":
            topics = [[re.sub("[^\u0400-\u045F]", "", x) for x in y] for y in topics]
        elif language.lower() == "chinese":
            topics = [[re.sub("[^\u4E00-\u9FFF]", "", x) for x in y] for y in topics]
        output = ""
        for topic in topics:
            for word in topic:
                output += word
                output += ","
        f = open(name, "wb")
        f.write(output.encode("utf-8"))
        f.close()

    def __calc_eucl_dist(self, list1, list2):
        '''
        This function returns a simple euclidean distance between two lists.
        '''
        match = 0
        for item in list1:
            if item in list2:
                match += 1
        return (match / len(list1))

    def __load_output(self, file):
        '''
        This function reads the encoded output file and outputs it into a splitted
        list.
        '''
        f = open(file, "r", encoding="utf-8")
        output = f.read()
        output = output.split(",")
        output = [word.lower() for word in output if word != ""]
        f.close()
        return output

    def generate_comparisons(self, output_path):
        self.output_path = output_path

        self.table = {}
        for i in self.languages:
            self.table[i] = {}
            for j in self.languages:
                list1 = self.__load_output("{}/{}.txt".format(self.output_path, i))
                list2 = self.__load_output("{}/{}.txt".format(self.output_path, j))
                self.table[i][j] = self.__calc_eucl_dist(list1, list2)
        return self.table

    def __lda(self):
        '''
        This function performs the Latent Dirichlet Allocation algoritm and saves
        both the output and the model to a file.
        '''
        temp_save_fpath = self.data_path + 'output/' + self.process_sign + "/temp/models/"
        temp_save_fpath_out = self.data_path + 'output/' + self.process_sign + "/"
        if not os.path.exists(temp_save_fpath):
            os.makedirs(temp_save_fpath)

        for language in self.languages:
            for n in self.num_topics:
                dictionary = corpora.Dictionary()
                dictionary = dictionary.load(self.data_path + "output/" + self.process_sign + "/temp/dictionary/{}".format(language))
                model = models.LdaModel(num_topics=n, update_every=1,
                                        id2word=dictionary)
                for i in range(1, self.num_passes + 1):
                    for year in self.years:
                        corpus = np.load(self.data_path + "output/" + self.process_sign + "/temp/step2/{}_{}.npy".format(language, year))
                        if len(corpus) == 1:
                            corpus = self.__reshape_corpus(corpus)
                        model.update(corpus)
                        print("Pass {} completed for {}, {}, {} topics".format(i, language, year, n))
                model.save(temp_save_fpath + "{}_{}".format(language.lower(), n))
                if not os.path.exists(temp_save_fpath_out + "output/{}_topics".format(n)):
                    os.makedirs(temp_save_fpath_out + "/output/{}_topics".format(n))
                self.__write_output(temp_save_fpath_out + "output/{}_topics/{}.txt".format(n, language), model, language.lower())


    ## Public functions of the class
    def run_analysis(self):

        if self.algorithm == "lda":
            self.__lda()



