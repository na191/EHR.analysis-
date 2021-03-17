
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime


class Observation: 
    id = ""
    lab = ""
    value = ""
    labdate = ""

    # key VALUE will be , patientID labname lavbalue
    # Examplle for  = 1992-07-01 01:36:17.91key0
    # value = 1A8791E3-A61C-455A-8DEE-763EB90C9B2C, URINALYSIS: RED BLOOD CELLS, 1.8

    def __init__(self,id,lab,value,labdate):
        #print("Obersvation initialized id, lab, value:"+ id + ", " + lab+ ", "+value)
        self.id= id
        self.lab = lab
        self.value = value
        self.labdate = labdate


    def sick_patients(lab_data,lab, gt_lt, value):
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
    



    #searchval = search(labcore_dict, '1A8791E3-A61C-455A-8DEE-763EB90C9B2C')
    #print( searchval)

    #print(sick_patients(labdata, 20, ">", 4.0 ))

    # Returns a list of patient ages.
class Patient:
    DOB = ""
    gender = ""
    race = ""
    observation_list = []
    _id = ""
    _age = 0
    def __init__(self,id, DOB, gender, race):
        #print("Patient initialized DOB, gender, race:"+ DOB + ", " + gender+ ", "+race)
        self.observation_list = []
        self._id = id
        self.DOB= DOB
        self.gender = gender
        self.race = race
        self._age = self.calculateAge()

    def calculateAge(self):
        try:
            birthday_date_object = datetime.strptime(self.DOB, "%Y-%m-%d %H:%M:%S.%f")
            today = datetime.now()
            time_difference = today - birthday_date_object
            ageinseconds = time_difference.total_seconds()
            calculatedAge = ageinseconds / 31536000
            return calculatedAge
        except Exception as e:
            # print("Thats not a date you silly goose.")
            print('exception caused by calculating age '+ str(e))
            pass

    @property
    def age(self):
        return self._age

    @property
    def id(self):
        return self._id

    def plot(self,testname, plotimagename):

        listofteststoplot = []
        for observation in self.observation_list:
            if testname == observation.lab:
                listofteststoplot.append(observation)
                #print("Id :" + str(observation.id) + ", "+ "lab :"+ str(observation.lab) + ", "+ "value :"+ str(observation.value) + ", " + "labdate :"+ str(observation.labdate))
                plt.scatter(observation.labdate, observation.value)
        
        plt.xlabel(testname)
        plt.ylabel(plotimagename)             
        plt.savefig("Date")
        plt.title("Test Values Over Time ")



    def num_older_than(patientagesdictionary, age):
        """This function loops through the data once to determine
    the number of values greater than the age input
    therfore the complexity is O(n) """

        try:
            age = float(age)
        except ValueError:
            raise ValueError('age should be an int or float')

        oldagecounter = 0
        for key in patientagesdictionary:
            patient_age = patientagesdictionary[key]
            if patient_age > age:
                oldagecounter = oldagecounter + 1
        return oldagecounter


    #patientagesdictionarytest = load_patients("patientcorepopulatedtest.txt")
    #print(num_older_than(patientagesdictionarytest, 70))
    def __eq__(self, other):
            if self._age==other.ft and self.inch==other.inch:
                return "both objects are equal"
            else:
                return "both objects are not equal"

    def __lt__(self, other):
        return self._age < other._age

    def __gt__(self, other):
        return self._age > other._age

    def age_admission(patientid, labfile, patientfile):
        if not isinstance(patientid, str):
            raise ValueError('patient ID should be a string')
        from datetime import datetime
        labdata = load_labs(labfile)
        #TODO FIGURE THIS OUT
        #patientdata = load_patients(patientfile)
        #id and ages
    # print(patientdata)
        listoftestdates= []
        patientage = 0
        #specific_id = [val for key,val in patientdata.items() if search in mystring]
        if patientid in patientdata:
            patientage = patientdata.get(patientid)
            
        patientlabdates = []
        for key, value in labdata.items():
            if patientid in value:
                
                patientlabdates.append(key)


        list_admin_date_objects= []
        for i in patientlabdates[1:]:
            date_admin = datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S.%f")
            list_admin_date_objects.append(date_admin)
        today = datetime.now()
        
        oldestlabappointmentdate =  min(list_admin_date_objects)
        
    # patientage/ oldestlabappointmentdate
        today = datetime.now()
        oldestlabappointmentdateObject = datetime.strptime(oldestlabappointmentdate, "%Y-%m-%d %H:%M:%S.%f")
        oldestlabappointmentage = today - oldestlabappointmentdateObject
        oldestlabappointmentageinyears = oldestlabappointmentage.days/365.25
        ageatfirstappointment = patientage - oldestlabappointmentageinyears
        
    
        return(ageatfirstappointment)
        
        
        

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
            if len(i)!= 6:
                raise ValueError('File should be 6 column tab deliminated') 
            dictionary_lab_values[i[5]] = i[0] + ", " + i[2] + ", " + i[3]

    return dictionary_lab_values
    #print(dictionary_lab_values)
def load_patients(filename):

        """ This Function parses the PatientCorePopulatedTable and converts
        the DOB timestamps into age in years
        There are 4 for loops in this function which equates to o(4n), in big
        O notation, the constant cancels out leaving
        o(n) as the computational complexity."""
        from datetime import datetime
        #from datetime import date

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

                    dictionary_patient_values[i[0]] = i[2] + "," + i[1] + "," + i[3]
        return dictionary_patient_values
   
    

    #print(age_admission('1A40AF35-C6D4-4D46-B475-A15D84E8A9D5', 'LabsCorePopulatedTable.txt', 'PatientCorePopulatedTable.txt'))
if __name__ == '__main__':
    dictionary_lab_values = load_labs("LabsCorePopulatedTable.txt")
    listofobservations = []
    for key in dictionary_lab_values:
        # print(key, '->', dictionary_lab_values[key])
        keyvalue = dictionary_lab_values[key].split(",")
        labdate = key
        patient_id = keyvalue[0]
        labtype = keyvalue[1].strip()
        labvalue = keyvalue[2].strip()
        observation = Observation(patient_id, labtype, labvalue, labdate)
        listofobservations.append(observation)

    dictionary_patient_values = load_patients("PatientCorePopulatedTable.txt")
    listofpatients = []
    for key in dictionary_patient_values:
        # print(key, '->', dictionary_lab_values[key])
        patient_id = key
        keyvalue = dictionary_patient_values[key].split(",")
        DOB = keyvalue[0]
        gender = keyvalue[1].strip()
        race = keyvalue[2].strip()
        patient = Patient(patient_id, DOB,gender, race)
        listofpatients.append(patient)

    #very slow. should be sped up
    #for patient in listofpatients:

    listofpatients.pop(0)
    listofobservations.pop(0)
    for patient in listofpatients:
        patient_id = patient._id
        for observation in listofobservations:
            if observation.id == patient_id:
                patient.observation_list.append(observation)
    

    patient1 = listofpatients[0]
    patient1.plot("METABOLIC: ALK PHOS","testplot")
    
