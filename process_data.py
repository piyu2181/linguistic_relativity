"""
Script: This class contains all the attributes and functions required for preprocessing of the data before
performing linguistic relativity
Author: Debjani Bhowmick, Tilburg University
Year: 2019
"""
import os
import sys

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

    def __load_files(self, year, language, matching_files):
        '''
        This function takes a list of .xml files and returns a corpus that is both
        parsed and cleaned.
        '''
        files_list = matching_files[year]
        files_list = ["UN/{}/{}/{}".format(language, year, file)
                      for file in files_list]
        files = []
        for file in files_list:
            f = open(file, "r", encoding="utf8")
            xml = f.read()
            files.append((clean_text(parse_xml(xml), language)))
            f.close()
        files = np.array(files)
        return files


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
        return matching_files


