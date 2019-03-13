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
    matching_files: stores the paths for all the files of desired languages and years
    data_path: Path for the data; should refer to the path containing folders for languages and years
    '''
    min_count = 5
    remove_n = 50
    n_topics = 10
    n_passes = 20
    matching_files = {}
    data_path = './UN/'

    
    def __init__(self,
                 languages, years, target_language = "English",
                 min_count = 5, remove_n = 50, n_topics = 10, n_passes = 20):

        self.languages = languages
        self.target_language = target_language
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
                full_path = self.data_path + "{}/{}".format(language, year)
                filepaths[language][year] = get_filepaths(full_path)
                filepaths[language][year] = [file[file.index('\\')+1:] 
                                            for file in filepaths[language][year]]
        matching_files = {}
        # Getting the unique set of names for all the files located
        for year in self.years:
            language_set = {}
            # Finding the set of unique filenames for each language
            for language in self.languages:
                language_set[language] = set(filepaths[language][year])

            # Update the set for the target language to only contain filenames that are present in all languages
            for language in self.languages:
                language_set[self.target_language].intersection_update(language_set[self.language])

            # Putting the found filenames into matching_files
            matching_files[year] = list(language_set[self.target_language])

            # This part needs to be deleted, if the above code works fine
            # set1 = set(filepaths["English"][year])
            # set2 = set(filepaths["Arabic"][year])
            # set3 = set(filepaths["Chinese"][year])
            # set4 = set(filepaths["Russian"][year])
            # set5 = set(filepaths["Spanish"][year])
            # set6 = set(filepaths["French"][year])
            # set1.intersection_update(set2, set3, set4, set5, set6)
            # matching_files[year] = list(set1)
        return matching_files


