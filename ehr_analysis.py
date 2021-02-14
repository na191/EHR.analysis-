# global variables  


"""I put the data into a dictionary using the timestamp as the key value because it was the only value that was unique for each row. 
This function includes 2 for loops which equates to O(2n), the constant is dropped resulting in O(n)  """
def load_labs(filename):
    with open (filename) as stream:
        lab_data_string = stream.read()

        lab_data_list = lab_data_string.split('\n')
        lab_data_upated_list = []
        for lab_data_entry in lab_data_list:
            lab_data_entry = lab_data_entry.strip().replace("\t", ",")
            lab_data_upated_list.append(lab_data_entry)
    
    # key will be timestamp
    # key VALUE will be , patientID labname lavbalue
    # Examplle for  = 1992-07-01 01:36:17.91key0
    # value = 1A8791E3-A61C-455A-8DEE-763EB90C9B2C, URINALYSIS: RED BLOOD CELLS, 1.8
    for index, lab_data in enumerate(lab_data_upated_list):
        if lab_data is not None and lab_data != "":
            i = lab_data.split(',')
            
            dictionary_lab_values[i[5]] = i[0] + ', ' + i[2] + ", " + i[3]








"""For this function I assigned ID's to the values in the dictionary, then created an if else statement to filter through the data
for the two conditions ">" or "<", finally I created a set object to ensure there were no duplicate ID's, This fucntion includes one for 
loop so the big O notation is o(n)    """


def sick_patients(lab, gt_lt, value):
    parseLabCorePopulatedTable()
    matchinglabid = []
    # key will be timestamp
    # key VALUE will be , patientID labname lavbalue
    for key in dictionary_lab_values:
        #print(key, '->', dictionary_lab_values[key])
        keyvalue =  dictionary_lab_values[key].split(',')
        patientID = keyvalue[0]
        labtype = keyvalue[1].strip()
        labvalue= keyvalue[2].strip()

        if gt_lt == '>':
            if labtype == lab and float(labvalue) > value:
                matchinglabid.append(patientID)
        else:
            if labtype == lab and float(labvalue) < value:
                matchinglabid.append(patientID)

    matchinglabid = list(set(matchinglabid))
    return matchinglabid
    
    
""" This Function parses the PatientCorePopulatedTable and converts the DOB timestamps into age in years
There are 4 for loops in this function which equates to o(4n), in big O notation, the constant cancels out leaving
o(n) as the computational complexity."""


# Returns a list of patient ages. 
def load_patients (filename):
    from datetime import datetime
    from datetime import date
    listofages = []
    with open (filename) as stream:
        patient_data_string = stream.read()

        patient_data_list = patient_data_string.split('\n')
        patient_data_upated_list = []
        for patient_data_entry in patient_data_list:
            patient_data_entry = patient_data_entry.strip().replace("\t", ",")
            patient_data_upated_list.append(patient_data_entry)
        dictionary_patient_values= {}
        
        
        for index, patient_data in enumerate(patient_data_upated_list):
            if patient_data is not None and patient_data != "":
                i = patient_data.split(',')
                
                dictionary_patient_values[i[0]] = i[2] 
    #print(dictionary_patient_values)
    listofbirthdates = []
    for key in dictionary_patient_values:
        birthdate =  dictionary_patient_values[key]
        #print(keyvalue)
        
        try:
            birthday_date_object = datetime.strptime(birthdate, "%Y-%m-%d %H:%M:%S.%f")
            listofbirthdates.append(birthday_date_object)
        except Exception:
            #print("Thats not a date you silly goose.")
            pass


    today = datetime.now()
    
    for birthdateobject in listofbirthdates:
        time_difference= today - birthdateobject
        ageinseconds= time_difference.total_seconds()
        age = ageinseconds/31536000
        listofages.append(age)
    
    return listofages
        
"""This function loops through the data once to determine the number of values greater than the age input
 therfore the complexity is O(n) """

def num_older_than(patientages, age):
    oldagecounter = 0
    for patientAge in patientages:
        if patientAge > age:
            oldagecounter = oldagecounter + 1
    return oldagecounter
        
patientages = load_patients("PatientCorePopulatedTable.txt")
print(num_older_than(patientages, 70))