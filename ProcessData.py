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
    matching_files = []
    
    def __init__(self, languages, years, min_count = 5, remove_n = 50, n_topics = 10, n_passes = 20):

        self.languages = languages
        self.years = years
        self.min_count = min_count
        self.remove_n = remove_n
        self.n_topics = n_topics
        self.n_passes = n_passes


    def find_matching_files(self):
        '''
        This function creates a dictionary containing the filepaths for all
        the files in all the desired languages and desired years
        '''
        filepaths = {}
        for language in self.languages:
            filepaths[language] = {}
        for language in self.languages:
            for year in self.years:
                filepaths[language][year] = get_filepaths(
                                            "UN/{}/{}".format(language, year))
                filepaths[language][year] = [file[file.index('\\')+1:] 
                                            for file in filepaths[language][year]]
        matching_files = {}
        for year in self.years:
            set1 = set(filepaths["English"][year])
            set2 = set(filepaths["Arabic"][year])
            set3 = set(filepaths["Chinese"][year])
            set4 = set(filepaths["Russian"][year])
            set5 = set(filepaths["Spanish"][year])
            set6 = set(filepaths["French"][year])
            set1.intersection_update(set2, set3, set4, set5, set6)
            matching_files[year] = list(set1)
        return matching_files


