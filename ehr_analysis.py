def load_labs(filename):
    """I put the data into a dictionary using the timestamp as the
    key value because it was the only value that was unique for each row."""
    with open(filename) as stream:
        lab_data_string = stream.read()

        lab_data_list = lab_data_string.split("\n")
        lab_data_upated_list = []
        for lab_data_entry in lab_data_list:
            lab_data_entry = lab_data_entry.strip().replace("\t", ",")
            lab_data_upated_list.append(lab_data_entry)

    # key VALUE will be , patientID labname lavbalue
    # Examplle for  = 1992-07-01 01:36:17.91key0
    # value = 1A8791E3-A61C-455A-8DEE-763EB90C9B2C, URINALYSIS: RED BLOOD CELLS, 1.8
    dictionary_lab_values = {}
    for index, lab_data in enumerate(lab_data_upated_list):
        if lab_data is not None and lab_data != "":
            i = lab_data.split(",")
            if len(i) != 6:
                raise ValueError('File should be 6 column tab deliminated')
            dictionary_lab_values[i[5]] = i[0] + ", " + i[2] + ", " + i[3]
    return dictionary_lab_values
    # print(dictionary_lab_values)


def sick_patients(lab_data, lab, gt_lt, value):
    """For this function I assigned ID's to the values in the dictionary,
     then created an if else statement
    to filter through the data for the two conditions ">" or "<",
    finally I created a set object to ensure there were no duplicate ID's,"""
    if not isinstance(lab, str):
        raise ValueError('lab should be a string')
    try:
        value = float(value)
    except ValueError:
        raise ValueError('lab value should be an int or float')

    matchinglabid = []
    # key will be timestamp
    # key VALUE will be , patientID labname lavbalue
    for key in lab_data:
        # print(key, '->', dictionary_lab_values[key])
        keyvalue = lab_data[key].split(",")
        patient_id = keyvalue[0]
        labtype = keyvalue[1].strip()
        labvalue = keyvalue[2].strip()

        if gt_lt == ">":
            if labtype == lab and float(labvalue) > value:
                matchinglabid.append(patient_id)
        else:
            if labtype == lab and float(labvalue) < value:
                matchinglabid.append(patient_id)

    matchinglabid = list(set(matchinglabid))
    return matchinglabid


<<<<<<< HEAD
labdata = load_labs("labcorepopulatedtest.txt")
#print(lab_data_ex['2006-10-13 16:27:58.243'])
#print(sick_patients(labdata, 20, ">", 4.0 ))

# Returns a list of patient ages.


def load_patients(filename):
    """ This Function parses the PatientCorePopulatedTable and converts
    the DOB timestamps into age in years
    There are 4 for loops in this function which equates to o(4n), in big
    O notation, the constant cancels out leaving
    o(n) as the computational complexity."""
=======
# Returns a list of patient ages. 
def load_patients (filename):
>>>>>>> 6766e2ca858e1d207ad56b4afa2054c901436518
    from datetime import datetime
    #from datetime import date

    listofages = []
    with open(filename) as stream:
        patient_data_string = stream.read()

        patient_data_list = patient_data_string.split("\n")
        patient_data_upated_list = []
        for patient_data_entry in patient_data_list:
            patient_data_entry = patient_data_entry.strip().replace("\t", ",")
            patient_data_upated_list.append(patient_data_entry)
        dictionary_patient_values = {}

        for index, patient_data in enumerate(patient_data_upated_list):
            if patient_data is not None and patient_data != "":
                i = patient_data.split(",")

                dictionary_patient_values[i[0]] = i[2]
    # print(dictionary_patient_values)
    listofbirthdates = []
    for key in dictionary_patient_values:
        birthdate = dictionary_patient_values[key]
        # print(keyvalue)

        try:
            birthday_date_object = datetime.strptime(
                birthdate, "%Y-%m-%d %H:%M:%S.%f")
            listofbirthdates.append(birthday_date_object)
        except Exception:
            # print("Thats not a date you silly goose.")
            pass

    today = datetime.now()

    for birthdateobject in listofbirthdates:
        time_difference = today - birthdateobject
        ageinseconds = time_difference.total_seconds()
        age = ageinseconds / 31536000
        listofages.append(age)

    return listofages


def num_older_than(patientages, age):
    """This function loops through the data once to determine
the number of values greater than the age input
 therfore the complexity is O(n) """

    try:
        age = float(age)
    except ValueError:
        raise ValueError('age should be an int or float')

    oldagecounter = 0
    for patient_age in patientages:
        if patient_age > age:
            oldagecounter = oldagecounter + 1
    return oldagecounter
<<<<<<< HEAD


patientages = load_patients("patientcorepopulatedtest.txt")
print(num_older_than(patientages, 70))


def age_admission(patientid, filename):
    labdata = load_labs(filename)
=======
        
patientages = load_patients("PatientCorePopulatedTable.txt")
print(num_older_than(patientages, 70))
>>>>>>> 6766e2ca858e1d207ad56b4afa2054c901436518
