"""test ehr.analysis.py """
import pytest
import ehr_analysis


def test_load_labs_size():
    """Test Load_ labs expected size"""
    assert len(ehr_analysis.load_labs("labcorepopulatedtest.txt")
               ) == 10, "File was not parsed correctly"


def test_load_labs_label():
    """Test Load_ labs expected label"""
    assert ehr_analysis.load_labs("labcorepopulatedtest.txt")[
        '1992-07-01 01:31:08.677'] == '1A8791E3-A61C-455A-8DEE-763EB90C9B2C, CBC: RED BLOOD CELL COUNT, 4.8', "file was not parsed correctly"


labdata = ehr_analysis.load_labs("labcorepopulatedtest.txt")


def test_sick_pateints():
    """Test sick_patients value not present """
    assert ehr_analysis.sick_patients(
        labdata, "METABOLIC: ALBUMIN", ">", 4.0) == [], 'incorrect ID values'


def test_sick_pateints():
    """Test sick_patients value"""
    assert ehr_analysis.sick_patients(labdata, "METABOLIC: TOTAL PROTEIN", ">", 4.0) == [
        '1A8791E3-A61C-455A-8DEE-763EB90C9B2C'], 'incorrect ID values'


def test_load_patients_size():
    """test load_patients expected size"""
    assert len(ehr_analysis.load_patients(
        "patientcorepopulatedtest.txt")) == 9, "File was not parsed correctly"


def test_load_patients_label():
    assert round(ehr_analysis.load_patients("patientcorepopulatedtest.txt")[
                 0]) == 73, "date was not calculated correctly"


patientages = ehr_analysis.load_patients("patientcorepopulatedtest.txt")


def test_num_older_than_validage():
    """ test older than with valid age"""
    assert ehr_analysis.num_older_than(
        patientages, 70) == 4, "value is incorrect"


def test_num_older_than_invalidage():
    """ test older than with invalid age """
    assert ehr_analysis.num_older_than(
        patientages, 300) == 0, "value is incorrect"


def test_num_older_than_string_for_age():
    with pytest.raises(ValueError) as valueerrorinfo:
        ehr_analysis.num_older_than(patientages, "hello")
        assert 'age should be an int or float' in str(valueerrorinfo.value)


def test_float_older_than():
    try:
        ehr_analysis.num_older_than(patientages, 70)
    except ValueError:
        pytest.fail("Unexpected error for float - test_float_older_than")


def test_float_sick_patient():
    try:
        ehr_analysis.sick_patients(
            labdata, "METABOLIC: TOTAL PROTEIN", ">", 4.0)
    except ValueError:
        pytest.fail("Unexpected error for sick_patient")


def test_sick_patient_for_lab_value():
    with pytest.raises(ValueError) as valueerrorinfo:
        ehr_analysis.sick_patients(
            labdata, "METABOLIC: TOTAL PROTEIN", ">", "hello")
        assert 'lab value should be an int or float' in str(
            valueerrorinfo.value)


def test_sick_patient_for_lab_type():
    with pytest.raises(ValueError) as valueerrorinfo:
        ehr_analysis.sick_patients(labdata, 20, ">", 4)
