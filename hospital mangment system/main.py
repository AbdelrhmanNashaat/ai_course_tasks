from abc import ABC, abstractmethod


class Patient:
    patient_name = ''
    patient_national_id = ''
    patient_gender = ''
    patient_age = 0
    patient_phone_number = 0
    patient_address = ''
    patient_disease = ''
    patient_id = 0

    def __init__(self, name, national_id, gender, age, phone_number, address, disease, patient_id):
        self.patient_name = name
        self.patient_national_id = national_id
        self.patient_gender = gender
        self.patient_age = age
        self.patient_phone_number = phone_number
        self.patient_address = address
        self.patient_disease = disease
        self.patient_id = patient_id

    def print_patient_data(self):
        print('Patient Name :', self.patient_name)
        print('Patient National ID :', self.patient_national_id)
        print('Patient Gender :', self.patient_gender)
        print('Patient Age :', self.patient_age)
        print('Patient Phone Number :', self.patient_phone_number)
        print('Patient Address :', self.patient_address)
        print('Patient Disease :', self.patient_disease)
        print('Patient Id :', self.patient_id)


class Employee(ABC):
    name = ''
    national_id = ''
    gender = ''
    age = ''
    phone_number = 0
    address = ''
    employee_id = 0

    def __int__(self, name, national_id, gender, age, phone_number, address, employee_id):
        self.name = name
        self.national_id = national_id
        self.gender = gender
        self.age = age
        self.phone_number = phone_number
        self.address = address
        self.employee_id = id

    @abstractmethod
    def print_data(self):
        pass


class Doctors(Employee):
    doctor_filed = ''
    doctor_salary = ''
    number_of_worked_days = ''
    has_staff = False

    def __init__(self, name, national_id, gender, age, phone_number, address, employee_id, doctor_filed, doctor_salary,
                 number_of_worked_days, has_staff):
        super().__init__(name, national_id, gender, age, phone_number, address, employee_id)
        self.doctor_filed = doctor_filed
        self.doctor_salary = doctor_salary
        self.number_of_worked_days = number_of_worked_days
        self.has_staff = has_staff

    def print_data(self):
        print('Doctor Name :', self.name)
        print('Doctor National ID :', self.national_id)
        print('Doctor Gender :', self.gender)
        print('Doctor Age :', self.age)
        print('Doctor Phone Number :', self.phone_number)
        print('Doctor Address :', self.address)
        print('Doctor Id :', self.employee_id)
        print('Doctor Filed :', self.doctor_filed)
        print('Doctor Number of worked days :', self.number_of_worked_days)
        print('Doctor Has staff or not :', self.has_staff)


class Nurses(Employee):
    worked_with_doctor_named = ''
    salary = ''
    has_bonus = False
    under_training_or_not = False

    def __init__(self, name, national_id, gender, age, phone_number, address, employee_id, worked_with_doctor_named,
                 salary,
                 has_bonus, under_training_or_not):
        super().__init__(name, national_id, gender, age, phone_number, address, employee_id)
        self.worked_with_doctor_named = worked_with_doctor_named
        self.salary = salary
        self.has_bonus = has_bonus
        self.under_training_or_not = under_training_or_not

    def print_data(self):
        print('Nurse Name :', self.name)
        print('Nurse National ID :', self.national_id)
        print('Nurse Gender :', self.gender)
        print('Nurse Age :', self.age)
        print('Nurse Phone Number :', self.phone_number)
        print('Nurse Address :', self.address)
        print('Nurse Id :', self.employee_id)
        print('Worked With Doctor :', self.worked_with_doctor_named)
        print('Nurse Salary :', self.salary)
        print('Nurse Has bonus :', self.has_bonus)
        print('Nurse under training :', self.under_training_or_not)


class Pharmacy:
    medicines = []
    patient_names = []
    patient_and_his_medicines = {}

    def add_new_patient(self, patient):
        self.patient_names.append(patient)

    def print_all_patient(self):
        print(self.patient_names)

    def add_new_medicine(self, medicine):
        self.medicines.append(medicine)

    def print_all_medicines(self):
        print(self.medicines)

    def sell_medicine(self, patient_name, medicines):
        self.patient_and_his_medicines['patient_name'] = medicines
        print('Price For ', self.patient_and_his_medicines['patient_name'], 'Is : 10$')

    def print_receipt(self, patient_name):
        print('receipt For :', patient_name)
        print('Medicines : :', self.patient_and_his_medicines['patient_name'])
