from fastapi import FastAPI
import sqlite3
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
from fastapi import FastAPI, HTTPException


class Observation:
    id = ""
    lab = ""
    value = ""
    labdate = ""

    # key VALUE will be , patientID labname lavbalue
    # Examplle for  = 1992-07-01 01:36:17.91key0
    # value = 1A8791E3-A61C-455A-8DEE-763EB90C9B2C, URINALYSIS: RED BLOOD CELLS, 1.8

    def __init__(self, id, lab, value, labdate):
        # print("Obersvation initialized id, lab, value:"+ id + ", " + lab+ ", "+value)
        self.id = id
        self.lab = lab
        self.value = value
        self.labdate = labdate


class Patient:
    DOB = ""
    gender = ""
    race = ""
    observation_list = []
    _id = ""
    _age = 0

    def __init__(self, id, DOB, gender, race):
        # print("Patient initialized DOB, gender, race:"+ DOB + ", " + gender+ ", "+race)
        self.observation_list = []
        self._id = id
        self.DOB = DOB
        self.gender = gender
        self.race = race

    def plot(self, testname, plotimagename, patientID, con):
        con = sqlite3.connect('labscorepopulatedtable.db')
        cur = con.cursor()
        cur1.execute(
            "SELECT labdate,labvalue FROM labsdata WHERE labname = ? AND patientid = ? ORDER BY date(labdate) DESC ", (testname, patientID,))
        labvalues = cur1.fetchall()

        plt.scatter(*zip(*labvalues))

    def num_older_than(self, age):
        con = sqlite3.connect('patientcorepopulatedtable.db')
        cur = con.cursor()
        try:
            age = float(age)
        except ValueError:
            raise ValueError('age should be an int or float')
        cur.execute("SELECT * FROM patientdata WHERE age > ?", (age,))
        rows = cur.fetchall()
        return 'ResultCount = %d' % len(rows)

    def age_admission(self, patientid):
        con = sqlite3.connect('labscorepopulatedtable.db')
        cur = con.cursor()
        if not isinstance(patientid, str):
            raise ValueError('patient ID should be a string')
        from datetime import datetime
        cur.execute1(
            "SELECT labdate FROM labsdata WHERE patientid = ?", (patientid))
        labdates = cur.fetchall()
        oldestlabappointmentdate = min(labdates)

    # patientage/ oldestlabappointmentdate
        today = datetime.now()
        oldestlabappointmentdateObject = datetime.strptime(
            oldestlabappointmentdate, "%Y-%m-%d %H:%M:%S.%f")
        oldestlabappointmentage = today - oldestlabappointmentdateObject
        oldestlabappointmentageinyears = oldestlabappointmentage.days/365.25
        ageatfirstappointment = patientage - oldestlabappointmentageinyears

        return(ageatfirstappointment)


def calculateAge(DOBs):

    try:
        for row in DOBs:
            birthday_date_object = datetime.strptime(
                DOBs, "%Y-%m-%d %H:%M:%S.%f")
            today = datetime.now()
            time_difference = today - birthday_date_object
            ageinseconds = time_difference.total_seconds()
            calculatedAge = ageinseconds / 31536000
            return calculatedAge
    except Exception as e:
        # print("Thats not a date you silly goose.")
        print('exception caused by calculating age ' + str(e))
        pass


def load_labs(filename):
    print("Loading file: "+filename)
    dictionary_lab_values = {}
    """I put the data into a dictionary using the timestamp as the
    key value because it was the only value that was unique for each row."""
    with open(filename) as stream:
        lab_data_string = stream.read()

        lab_data_list = lab_data_string.split("\n")
        lab_data_upated_list = []
        for lab_data_entry in lab_data_list:
            lab_data_entry = lab_data_entry.strip().replace("\t", ",")
            lab_data_upated_list.append(lab_data_entry)

    for index, lab_data in enumerate(lab_data_upated_list):
        if lab_data is not None and lab_data != "":
            i = lab_data.split(",")
            if len(i) != 6:
                raise ValueError('File should be 6 column tab deliminated')
            dictionary_lab_values[i[5]] = i[0] + ", " + i[2] + ", " + i[3]

    return dictionary_lab_values
    # print(dictionary_lab_values)


def load_patients(filename):
    """ This Function parses the PatientCorePopulatedTable and converts
    the DOB timestamps into age in years
    There are 4 for loops in this function which equates to o(4n), in big
    O notation, the constant cancels out leaving
    o(n) as the computational complexity."""
    from datetime import datetime
    # from datetime import date

    listofages = []
    with open(filename, encoding='utf-8-sig') as stream:
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

                dictionary_patient_values[i[0]
                                          ] = i[2] + "," + i[1] + "," + i[3]
    return dictionary_patient_values

    # print(age_admission('1A40AF35-C6D4-4D46-B475-A15D84E8A9D5', 'LabsCorePopulatedTable.txt', 'PatientCorePopulatedTable.txt'))
# if __name__ == '__main__':


def load_data():
    print("Does this run?")

    dictionary_lab_values = load_labs("LabsCorePopulatedTable.txt")
    con1 = sqlite3.connect('labscorepopulatedtable.db')
    cur1 = con1.cursor()
    cur1.execute("DROP table IF EXISTS labsdata")
    cur1.execute(
        "CREATE TABLE labsdata (labdate text PRIMARY KEY ,patientid text NOT NULL, labname text, labvalue text) ")
    for key in dictionary_lab_values:
        dictionaryvalue = dictionary_lab_values.get(key)
        dictionaryvaluearray = dictionaryvalue.split(',')
        tupple = [key.strip(), dictionaryvaluearray[0].strip(),
                  dictionaryvaluearray[1].strip(), dictionaryvaluearray[2].strip()]
        cur1.execute(
            "INSERT INTO labsdata(labdate, patientid, labname, labvalue) VALUES (?, ?, ?, ?);", tupple)
    con1.commit()

    listofobservations = []
    for key in dictionary_lab_values:
        # print(key, '->', dictionary_lab_values[key])
        keyvalue = dictionary_lab_values[key].split(",")
        labdate = key
        patient_id = keyvalue[0]
        labtype = keyvalue[1].strip()
        labvalue = keyvalue[2].strip()
        observation = Observation(
            patient_id, labtype, labvalue, labdate)
        listofobservations.append(observation)

    dictionary_patient_values = load_patients("PatientCorePopulatedTable.txt")
    # print(dictionary_patient_values.get("FB2ABB23-C9D0-4D09-8464-49BF0B982F0F"))
    con = sqlite3.connect('patientcorepopulatedtable.db')
    cur = con.cursor()
    cur.execute("DROP table IF EXISTS patientdata")
    cur.execute(
        "CREATE TABLE patientdata (patient_id text PRIMARY KEY ,DOB text NOT NULL, gender text, race text, age text) ")
    for key in dictionary_patient_values:
        dictionaryvalue = dictionary_patient_values.get(key)
        dictionaryvaluearray = dictionaryvalue.split(',')
        dob = dictionaryvaluearray[0]
        age = calculateAge(dob)
        tupple = [key, dictionaryvaluearray[0],
                  dictionaryvaluearray[1], dictionaryvaluearray[2], age]
        # print(tupple)
        cur.execute(
            "INSERT INTO patientdata(patient_id,DOB , gender,race, age) VALUES (?, ?, ?, ?, ?);", tupple)
    con.commit()

    listofpatients = []
    for key in dictionary_patient_values:
        # print(key, '->', dictionary_lab_values[key])
        patient_id = key
        keyvalue = dictionary_patient_values[key].split(",")
        DOB = keyvalue[0]
        gender = keyvalue[1].strip()
        race = keyvalue[2].strip()
        patient = Patient(patient_id, DOB, gender, race)
        listofpatients.append(patient)

    # very slow. should be sped up
    # for patient in listofpatients:

    listofpatients.pop(0)
    listofobservations.pop(0)
    for patient in listofpatients:
        patient_id = patient._id
        for observation in listofobservations:
            if observation.id == patient_id:
                patient.observation_list.append(observation)

    print(patient.num_older_than(10))
    # print(observation.sick_patients("URINALYSIS: RED BLOOD CELLS", ">", 2))
    patient1 = listofpatients[0]
    # patient1.plot("CBC: ABSOLUTE NEUTROPHILS", "fakeplot",
    #               "220C8D43-1322-4A9D-B890-D426942A3649")


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    load_data()


@app.get("/patients/{patient_id}")
async def root(patient_id):
    con = sqlite3.connect('patientcorepopulatedtable.db')
    cur1 = con.cursor()
    cur1.execute(
        "SELECT * from patientdata WHERE patient_id=?", (patient_id,))
    patientvalues = cur1.fetchall()
    patient = Patient(patientvalues[0][0], patientvalues[0]
                      [1], patientvalues[0][2], patientvalues[0][3])
    return patient


@app.get("/patients/{patient_id}/lab")
async def root(patient_id):
    con = sqlite3.connect('labscorepopulatedtable.db')
    cur1 = con.cursor()
    cur1.execute(
        "SELECT * from labsdata WHERE patientid =?", (patient_id,))
    labvalues = cur1.fetchall()
    lab = Observation(labvalues[0][0], labvalues[0]
                      [1], labvalues[0][2], labvalues[0][3])
    return lab


@app.get("/patients/{age}/num_older_than")
async def root(age):
    int_age = int(age)
    numolder = num_older_than(int_age)
    return numolder


@app.get("/patients/sick_patients/{lab}/{gt_lt}/{value}/")
async def root(lab, gt_lt, value):
    values = float(value)
    sickpatients = sick_patients(lab, gt_lt, values)
    return sickpatients


def num_older_than(age):
    con = sqlite3.connect('patientcorepopulatedtable.db')
    cur = con.cursor()
    try:
        age = float(age)
    except ValueError:
        raise ValueError('age should be an int or float')
    cur.execute("SELECT * FROM patientdata WHERE age > ?", (age,))
    rows = cur.fetchall()
    return 'ResultCount = %d' % len(rows)


def sick_patients(lab, gt_lt, value):
    con = sqlite3.connect('labscorepopulatedtable.db')
    cur1 = con.cursor()
    if not isinstance(lab, str):
        raise ValueError('lab should be a string')
    try:
        value = float(value)
    except ValueError:
        raise ValueError('lab value should be an int or float')
    if gt_lt == ">":
        cur1.execute(
            "SELECT patientid FROM labsdata WHERE labvalue > ? AND labname = ?", (value, lab))
        rows = cur1.fetchall()
        return set(rows)
    else:
        cur1.execute(
            "SELECT patientid FROM labsdata WHERE labvalue < ? AND labname = ?", (value, lab))
        rows = cur1.fetchall()
        return set(rows)
