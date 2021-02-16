# EHR.analysis
# About 

ehr_analysis is a python document meant to parse and extract certain information from electronic health records. The expected input files are table .txt files. For sick_patients, the file should be in a format similar to the file included in the test materials, and the same is expected for the fucntion num_older_than(). 
The function sick_patients() takes the inputs: data, "string of lab name", "> or <", and an int/float. The function returns a unique list of patient ID's whose test values are above or below the given value.
example: 
```
ehr_analysis.sick_patients("METABOLIC: ALBUMIN", ">", 4.0)
["FB2ABB23-C9D0-4D09-8464-49BF0B982F0F", "64182B95-EB72-4E2B-BE77-8050B71498CE"]
```
The function num_older_than() returns the number of patients older than a given age (given in years). 
example:
```
ehr_analysis.num_older_than(51.2)
52
```

# Setup/Installation 
```
import ehr_analysis
```
# Test instructions 
The test file ehr_analysis_test.py can be evaluated using pytest. Test data is included (labcorepopulatedtest.txt, patientcorepopulatedtest.txt). pytest can be run from the terminal:
```
pip install pytest 

pytest ehr_analysis_test.py
```
