'''
script: Test run 1, to be edited later
Author: Debjani Bhowmick, Tilburg University
'''

# importing necessary libraries
import process_data as prd

# Languages and years of data to be used for the study
languages = ["English", "French", "Spanish"]
years = ["1990", "1991", "1992", "1997"]

# Parameters to be used in the studyß
data_path = "/Users/dgupta/Desktop/UN/"



# Create object for ProcessData class
obj_process = prd.ProcessData(data_path, languages, years, process_sign="T001")

# Finding all the matching files
obj_process.find_matching_files(save_flag=True, save_fname="temp.txt")