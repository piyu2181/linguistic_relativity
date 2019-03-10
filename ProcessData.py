"""
Script: This class contains all the attributes and functions required for preprocessing of the data before
performing linguistic relativity
Author: Debjani Bhowmick, Tilburg University
Year: 2019
"""


class ProcessData:

    '''
    Attributes:
    min_count: Defines the min. number of documents that contain a certain word; a count below this number would
    ignore the word from the study
    remove_n:
    n_topics:
    n_passes:
    '''
    min_count = 5
    remove_n = 50
    n_topics = 10
    n_passes = 20

    def __init__(self, languages, years, min_count = 5, remove_n = 50, n_topics = 10, n_passes = 20):

        self.languages = languages
        self.years = years
        self.min_count = min_count
        self.remove_n = remove_n
        self.n_topics = n_topics
        self.n_passes = n_passes


    def find_matching_files(self):



