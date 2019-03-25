'''
script: Test run 1, to be edited later
Author: Debjani Bhowmick, Tilburg University
'''

# importing necessary libraries
import process_data as prd
import analyze_data as ald

# Languages and years of data to be used for the study
languages = ["English", "French", "Spanish"]
years = ["1990", "1991", "1992", "1997"]

# Parameters to be used in the studyß
data_path = "/Users/dgupta/Desktop/UN/"

num_passes = 5
num_topics = [5, 10, 15, 20]


# Create object for ProcessData class
#obj_process = prd.ProcessData(data_path, languages, years, process_sign="T001")
# Finding all the matching files
#obj_process.find_matching_files(save_flag=True, save_fname="temp.txt")
# Preparing the corpus data
#obj_process.prepare_corpus()

# Perform anaysis
process_sign = "T001"
obj_analysis = ald.AnalyzeData(languages, years, data_path, process_sign, "lda", num_passes, num_topics)
#obj_analysis.run_analysis()

output_path = data_path + "output/" + process_sign + "/output/5_topics"
compare_table = obj_analysis.generate_comparisons(output_path)
print(compare_table)