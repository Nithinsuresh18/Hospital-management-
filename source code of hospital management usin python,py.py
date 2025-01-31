import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="Hospital"
)
cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT,
        gender VARCHAR(10),
        phone_number VARCHAR(15),
        bill_due DECIMAL(10, 2)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        specialization VARCHAR(255),
        salary DECIMAL(10, 2)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        doctor_id INT,
        time VARCHAR(20),
        date DATE,
        FOREIGN KEY (patient_id) REFERENCES patients(id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pharmacy (
        id INT AUTO_INCREMENT PRIMARY KEY,
        medicine_name VARCHAR(255),
        quantity INT,
        price DECIMAL(10, 2),
        expiry_date DATE
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        doctor_id INT,
        diagnosis TEXT,
        medicine_prescribed TEXT,
        bill_amount DECIMAL(10, 2),
        FOREIGN KEY (patient_id) REFERENCES patients(id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        password VARCHAR(255)
    )
""")
db.commit()

# GUI
class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Healthcare Management System")

        # Hospital Name
        self.hospital_name_label = tk.Label(self.root, text="SRM Hospitals", font=('Helvetica', 26, 'bold'))
        self.hospital_name_label.pack(pady=10)

        # Live Date and Time
        self.date_time_label = tk.Label(self.root, font=('Helvetica', 12))
        self.date_time_label.pack(pady=5)

        # Tabs
        self.notebook = ttk.Notebook(root)
        self.login_tab = ttk.Frame(self.notebook)
        self.patient_tab = ttk.Frame(self.notebook)
        self.doctor_tab = ttk.Frame(self.notebook)
        self.appointment_tab = ttk.Frame(self.notebook)
        self.pharmacy_tab = ttk.Frame(self.notebook)
        self.report_tab = ttk.Frame(self.notebook)
        

        self.notebook.add(self.login_tab, text='Login')
        self.notebook.add(self.patient_tab, text='Patients', state='disabled')
        self.notebook.add(self.doctor_tab, text='Doctors', state='disabled')
        self.notebook.add(self.appointment_tab, text='Appointments', state='disabled')
        self.notebook.add(self.pharmacy_tab, text='Pharmacy', state='disabled')
        self.notebook.add(self.report_tab, text='Report', state='disabled')
        # Login Tab
        self.create_login_tab()

        # Patient Tab
        self.create_patient_tab()

        # Doctor Tab
        self.create_doctor_tab()

        # Appointment Tab
        self.create_appointment_tab()

        # Pharmacy Tab
        self.create_pharmacy_tab()

        #Report tab
        self.create_report_tab()

        self.notebook.pack()

        # Update date and time every second
        self.update_date_time()

    def update_date_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_time_label.config(text=f"Current Date and Time: {current_time}")
        self.root.after(1000, self.update_date_time)

    def create_login_tab(self):
        # User ID Entry
        self.user_id_label = tk.Label(self.login_tab, text="User ID:")
        self.user_id_entry = tk.Entry(self.login_tab)

        # Password Entry
        self.password_label = tk.Label(self.login_tab, text="Password:")
        self.password_entry = tk.Entry(self.login_tab, show="*")

        # Login Button
        self.login_button = tk.Button(self.login_tab, text="Login", command=self.login)

        # Grid
        self.user_id_label.grid(row=0, column=0, pady=10)
        self.user_id_entry.grid(row=0, column=1, pady=10)

        self.password_label.grid(row=1, column=0, pady=10)
        self.password_entry.grid(row=1, column=1, pady=10)

        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.user_id_entry.get()
        password = self.password_entry.get()

        # Check the credentials in the 'users' table
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()

        if result:
            # If the login is successful, enable all tabs and switch to the Patients tab
            for tab in (self.patient_tab, self.doctor_tab, self.appointment_tab, self.pharmacy_tab, self.report_tab):
                self.notebook.tab(tab, state='normal')
            self.notebook.select(self.patient_tab)
        else:
            # Display an error message for unsuccessful login
            tk.messagebox.showerror("Login Failed", "Invalid username or password")

    def create_patient_tab(self):
        # Patient Entry
        self.patient_name_label = tk.Label(self.patient_tab, text="Name:")
        self.patient_name_entry = tk.Entry(self.patient_tab)

        self.patient_age_label = tk.Label(self.patient_tab, text="Age:")
        self.patient_age_entry = tk.Entry(self.patient_tab)

        self.patient_gender_label = tk.Label(self.patient_tab, text="Gender:")
        self.patient_gender_var = tk.StringVar(self.patient_tab)
        self.patient_gender_combobox = ttk.Combobox(self.patient_tab, textvariable=self.patient_gender_var,
                                                    values=["Male", "Female", "Other"])

        self.phone_number_label = tk.Label(self.patient_tab, text="Phone Number:")
        self.phone_number_entry = tk.Entry(self.patient_tab)

        self.bill_due_label = tk.Label(self.patient_tab, text="Bill Due:")
        self.bill_due_entry = tk.Entry(self.patient_tab)

        self.add_patient_button = tk.Button(self.patient_tab, text="Add Patient", command=self.add_patient)
        self.edit_patient_button = tk.Button(self.patient_tab, text="Edit Patient", command=self.edit_patient)
        self.update_patient_button = tk.Button(self.patient_tab, text="Update Patient", command=self.update_patient)
        self.delete_patient_button = tk.Button(self.patient_tab, text="Delete Patient", command=self.delete_patient)

        # Patient Treeview
        self.patients_tree = ttk.Treeview(self.patient_tab, columns=('ID', 'Name', 'Age', 'Gender', 'Phone Number', 'Bill Due'))
        self.patients_tree.heading('ID', text='ID')
        self.patients_tree.heading('Name', text='Name')
        self.patients_tree.heading('Age', text='Age')
        self.patients_tree.heading('Gender', text='Gender')
        self.patients_tree.heading('Phone Number', text='Phone Number')
        self.patients_tree.heading('Bill Due', text='Bill Due')

        # Grid
        self.patient_name_label.grid(row=0, column=0)
        self.patient_name_entry.grid(row=0, column=1)

        self.patient_age_label.grid(row=1, column=0)
        self.patient_age_entry.grid(row=1, column=1)

        self.patient_gender_label.grid(row=2, column=0)
        self.patient_gender_combobox.grid(row=2, column=1)

        self.phone_number_label.grid(row=3, column=0)
        self.phone_number_entry.grid(row=3, column=1)

        self.bill_due_label.grid(row=4, column=0)
        self.bill_due_entry.grid(row=4, column=1)

        self.add_patient_button.grid(row=5, column=0, columnspan=2)
        self.edit_patient_button.grid(row=5, column=2, columnspan=2)
        self.update_patient_button.grid(row=5, column=4, columnspan=2)
        self.delete_patient_button.grid(row=5, column=6, columnspan=2)

        self.patients_tree.grid(row=6, column=0, columnspan=8)

        # Load Patients on startup
        self.load_patients()

    def add_patient(self):
        name = self.patient_name_entry.get()
        age = self.patient_age_entry.get()
        gender = self.patient_gender_var.get()
        phone_number = self.phone_number_entry.get()
        bill_due = self.bill_due_entry.get()

        # Inserting data into the 'patients' table
        cursor.execute("INSERT INTO patients (name, age, gender, phone_number, bill_due) VALUES (%s, %s, %s, %s, %s)",
                       (name, age, gender, phone_number, bill_due))
        db.commit()

        # Update the patient list
        self.load_patients()

    def edit_patient(self):
        selected_item = self.patients_tree.selection()
        if selected_item:
            patient_id, name, age, gender, phone_number, bill_due = self.patients_tree.item(selected_item, 'values')
            self.patient_name_entry.delete(0, tk.END)
            self.patient_age_entry.delete(0, tk.END)
            self.patient_name_entry.insert(0, name)
            self.patient_age_entry.insert(0, age)
            self.patient_gender_var.set(gender)
            self.phone_number_entry.delete(0, tk.END)
            self.phone_number_entry.insert(0, phone_number)
            self.bill_due_entry.delete(0, tk.END)
            self.bill_due_entry.insert(0, bill_due)

    def update_patient(self):
        selected_item = self.patients_tree.selection()
        if selected_item:
            patient_id = self.patients_tree.item(selected_item, 'values')[0]
            name = self.patient_name_entry.get()
            age = self.patient_age_entry.get()
            gender = self.patient_gender_var.get()
            phone_number = self.phone_number_entry.get()
            bill_due = self.bill_due_entry.get()

            # Updating data in the 'patients' table
            cursor.execute("UPDATE patients SET name=%s, age=%s, gender=%s, phone_number=%s, bill_due=%s WHERE id=%s",
                           (name, age, gender, phone_number, bill_due, patient_id))
            db.commit()

            # Update the patient list
            self.load_patients()

    def delete_patient(self):
        selected_item = self.patients_tree.selection()
        if selected_item:
            patient_id = self.patients_tree.item(selected_item, 'values')[0]

            # Deleting data from the 'patients' table
            cursor.execute("DELETE FROM patients WHERE id=%s", (patient_id,))
            db.commit()

            # Update the patient list
            self.load_patients()

    def load_patients(self):
        # Clearing the existing data in the treeview
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)

        # Fetching patients from the database
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()

        # Inserting the updated data
        for patient in patients:
            self.patients_tree.insert('', 'end', values=patient)

    def create_doctor_tab(self):
        # Doctor Entry
        self.doctor_name_label = tk.Label(self.doctor_tab, text="Name:")
        self.doctor_name_entry = tk.Entry(self.doctor_tab)

        self.specialization_label = tk.Label(self.doctor_tab, text="Specialization:")
        self.specialization_entry = tk.Entry(self.doctor_tab)

        self.salary_label = tk.Label(self.doctor_tab, text="Salary:")
        self.salary_entry = tk.Entry(self.doctor_tab)

        self.add_doctor_button = tk.Button(self.doctor_tab, text="Add Doctor", command=self.add_doctor)
        self.edit_doctor_button = tk.Button(self.doctor_tab, text="Edit Doctor", command=self.edit_doctor)
        self.update_doctor_button = tk.Button(self.doctor_tab, text="Update Doctor", command=self.update_doctor)
        self.delete_doctor_button = tk.Button(self.doctor_tab, text="Delete Doctor", command=self.delete_doctor)

        # Doctor Treeview
        self.doctors_tree = ttk.Treeview(self.doctor_tab, columns=('ID', 'Name', 'Specialization', 'Salary'))
        self.doctors_tree.heading('ID', text='ID')
        self.doctors_tree.heading('Name', text='Name')
        self.doctors_tree.heading('Specialization', text='Specialization')
        self.doctors_tree.heading('Salary', text='Salary')

        # Grid
        self.doctor_name_label.grid(row=0, column=0)
        self.doctor_name_entry.grid(row=0, column=1)

        self.specialization_label.grid(row=1, column=0)
        self.specialization_entry.grid(row=1, column=1)

        self.salary_label.grid(row=2, column=0)
        self.salary_entry.grid(row=2, column=1)

        self.add_doctor_button.grid(row=5, column=0, columnspan=2)
        self.edit_doctor_button.grid(row=5, column=2, columnspan=2)
        self.update_doctor_button.grid(row=5, column=4, columnspan=2)
        self.delete_doctor_button.grid(row=5, column=6, columnspan=2)

        self.doctors_tree.grid(row=6, column=0, columnspan=8)

        # Load Doctors on startup
        self.load_doctors()

    def add_doctor(self):
        name = self.doctor_name_entry.get()
        specialization = self.specialization_entry.get()
        salary = self.salary_entry.get()

        # Inserting data into the 'doctors' table
        cursor.execute("INSERT INTO doctors (name, specialization, salary) VALUES (%s, %s, %s)", (name, specialization, salary))
        db.commit()

        # Update the doctor list
        self.load_doctors()

    def edit_doctor(self):
        selected_item = self.doctors_tree.selection()
        if selected_item:
            doctor_id, name, specialization, salary = self.doctors_tree.item(selected_item, 'values')
            self.doctor_name_entry.delete(0, tk.END)
            self.specialization_entry.delete(0, tk.END)
            self.salary_entry.delete(0, tk.END)
            self.doctor_name_entry.insert(0, name)
            self.specialization_entry.insert(0, specialization)
            self.salary_entry.insert(0, salary)

    def update_doctor(self):
        selected_item = self.doctors_tree.selection()
        if selected_item:
            doctor_id = self.doctors_tree.item(selected_item, 'values')[0]
            name = self.doctor_name_entry.get()
            specialization = self.specialization_entry.get()
            salary = self.salary_entry.get()

            # Updating data in the 'doctors' table
            cursor.execute("UPDATE doctors SET name=%s, specialization=%s, salary=%s WHERE id=%s", (name, specialization, salary, doctor_id))
            db.commit()

            # Update the doctor list
            self.load_doctors()

    def delete_doctor(self):
        selected_item = self.doctors_tree.selection()
        if selected_item:
            doctor_id = self.doctors_tree.item(selected_item, 'values')[0]

            # Deleting data from the 'doctors' table
            cursor.execute("DELETE FROM doctors WHERE id=%s", (doctor_id,))
            db.commit()

            # Update the doctor list
            self.load_doctors()

    def load_doctors(self):
        # Clearing the existing data in the treeview
        for item in self.doctors_tree.get_children():
            self.doctors_tree.delete(item)

        # Fetching doctors from the database
        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()

        # Inserting the updated data
        for doctor in doctors:
            self.doctors_tree.insert('', 'end', values=doctor)


    def create_appointment_tab(self):
        # Appointment Entry
        self.appointment_patient_label = tk.Label(self.appointment_tab, text="Patient:")
        self.appointment_patient_var = tk.StringVar(self.appointment_tab)
        self.appointment_patient_combobox = ttk.Combobox(self.appointment_tab, textvariable=self.appointment_patient_var,
                                                         values=self.get_patient_names())

        self.appointment_doctor_label = tk.Label(self.appointment_tab, text="Doctor:")
        self.appointment_doctor_var = tk.StringVar(self.appointment_tab)
        self.appointment_doctor_combobox = ttk.Combobox(self.appointment_tab, textvariable=self.appointment_doctor_var,
                                                         values=self.get_doctor_names())

        self.appointment_time_label = tk.Label(self.appointment_tab, text="Time:")
        self.appointment_time_entry = tk.Entry(self.appointment_tab)

        self.appointment_date_label = tk.Label(self.appointment_tab, text="Date:")
        self.appointment_date_entry = tk.Entry(self.appointment_tab)

        self.add_appointment_button = tk.Button(self.appointment_tab, text="Add Appointment", command=self.add_appointment)
        self.edit_appointment_button = tk.Button(self.appointment_tab, text="Edit Appointment", command=self.edit_appointment)
        self.update_appointment_button = tk.Button(self.appointment_tab, text="Update Appointment", command=self.update_appointment)
        self.delete_appointment_button = tk.Button(self.appointment_tab, text="Delete Appointment", command=self.delete_appointment)

        # Appointment Treeview
        self.appointments_tree = ttk.Treeview(self.appointment_tab, columns=('ID', 'Patient', 'Doctor', 'Time', 'Date'))
        self.appointments_tree.heading('ID', text='ID')
        self.appointments_tree.heading('Patient', text='Patient')
        self.appointments_tree.heading('Doctor', text='Doctor')
        self.appointments_tree.heading('Time', text='Time')
        self.appointments_tree.heading('Date', text='Date')

        # Grid
        self.appointment_patient_label.grid(row=0, column=0)
        self.appointment_patient_combobox.grid(row=0, column=1)

        self.appointment_doctor_label.grid(row=1, column=0)
        self.appointment_doctor_combobox.grid(row=1, column=1)

        self.appointment_time_label.grid(row=2, column=0)
        self.appointment_time_entry.grid(row=2, column=1)

        self.appointment_date_label.grid(row=3, column=0)
        self.appointment_date_entry.grid(row=3, column=1)

        self.add_appointment_button.grid(row=4, column=0, columnspan=2)
        self.edit_appointment_button.grid(row=4, column=2, columnspan=2)
        self.update_appointment_button.grid(row=4, column=4, columnspan=2)
        self.delete_appointment_button.grid(row=4, column=6, columnspan=2)

        self.appointments_tree.grid(row=12, column=0, columnspan=8)

        # Load Appointments on startup
        self.load_appointments()

    def add_appointment(self):
        patient_name = self.appointment_patient_var.get()
        doctor_name = self.appointment_doctor_var.get()
        time = self.appointment_time_entry.get()
        date = self.appointment_date_entry.get()

        # Get patient and doctor IDs
        patient_id = self.get_patient_id_by_name(patient_name)
        doctor_id = self.get_doctor_id_by_name(doctor_name)

        if patient_id and doctor_id:
            # Inserting data into the 'appointments' table
            cursor.execute("INSERT INTO appointments (patient_id, doctor_id, time, date) VALUES (%s, %s, %s, %s)",
                           (patient_id, doctor_id, time, date))
            db.commit()

            # Update the appointment list
            self.load_appointments()

    def edit_appointment(self):
        selected_item = self.appointments_tree.selection()
        if selected_item:
            appointment_id, patient_name, doctor_name, time = self.appointments_tree.item(selected_item, 'values')
            self.appointment_patient_var.set(patient_name)
            self.appointment_doctor_var.set(doctor_name)
            self.appointment_time_entry.delete(0, tk.END)
            self.appointment_time_entry.insert(0, time)

    def update_appointment(self):
        selected_item = self.appointments_tree.selection()
        if selected_item:
            appointment_id = self.appointments_tree.item(selected_item, 'values')[0]
            patient_name = self.appointment_patient_var.get()
            doctor_name = self.appointment_doctor_var.get()
            time = self.appointment_time_entry.get()

            # Get patient and doctor IDs
            patient_id = self.get_patient_id_by_name(patient_name)
            doctor_id = self.get_doctor_id_by_name(doctor_name)

            if patient_id and doctor_id:
                # Updating data in the 'appointments' table
                cursor.execute("UPDATE appointments SET patient_id=%s, doctor_id=%s, time=%s WHERE id=%s",
                               (patient_id, doctor_id, time, appointment_id))
                db.commit()

                # Update the appointment list
                self.load_appointments()

    def delete_appointment(self):
        selected_item = self.appointments_tree.selection()
        if selected_item:
            appointment_id = self.appointments_tree.item(selected_item, 'values')[0]

            # Deleting data from the 'appointments' table
            cursor.execute("DELETE FROM appointments WHERE id=%s", (appointment_id,))
            db.commit()

            # Update the appointment list
            self.load_appointments()

    def load_appointments(self):
        # Clearing the existing data in the treeview
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)

        # Fetching appointments from the database
        cursor.execute("SELECT * FROM appointments")
        appointments = cursor.fetchall()

        # Inserting the updated data into the treeview
        for appointment in appointments:
            # Format the date before inserting into the Treeview
            formatted_date = datetime.strftime(appointment[4], "%Y-%m-%d")
            self.appointments_tree.insert('', 'end', values=(appointment[0], self.get_patient_name_by_id(appointment[1]),
                                                            self.get_doctor_name_by_id(appointment[2]), appointment[3],
                                                            formatted_date))

    

    def create_pharmacy_tab(self):
        # Medicine Entry
        self.medicine_id_label = tk.Label(self.pharmacy_tab, text="Medicine ID:")
        self.medicine_id_entry = tk.Entry(self.pharmacy_tab, state='disabled')

        self.medicine_name_label = tk.Label(self.pharmacy_tab, text="Medicine Name:")
        self.medicine_name_entry = tk.Entry(self.pharmacy_tab)

        self.medicine_quantity_label = tk.Label(self.pharmacy_tab, text="Quantity:")
        self.medicine_quantity_entry = tk.Entry(self.pharmacy_tab)

        self.medicine_cost_label = tk.Label(self.pharmacy_tab, text="Medicine Cost:")
        self.medicine_cost_entry = tk.Entry(self.pharmacy_tab)

        self.medicine_expiry_label = tk.Label(self.pharmacy_tab, text="Expiry Date (YYYY-MM-DD):")
        self.medicine_expiry_entry = tk.Entry(self.pharmacy_tab)

        self.add_medicine_button = tk.Button(self.pharmacy_tab, text="Add Medicine", command=self.add_medicine)
        self.edit_medicine_button = tk.Button(self.pharmacy_tab, text="Edit Medicine", command=self.edit_medicine)
        self.update_medicine_button = tk.Button(self.pharmacy_tab, text="Update Medicine", command=self.update_medicine)
        self.delete_medicine_button = tk.Button(self.pharmacy_tab, text="Delete Medicine", command=self.delete_medicine)

        # Medicine Treeview
        self.medicines_tree = ttk.Treeview(self.pharmacy_tab, columns=('ID', 'Medicine Name', 'Quantity', 'Cost', 'Expiry Date'))
        self.medicines_tree.heading('ID', text='ID')
        self.medicines_tree.heading('Medicine Name', text='Medicine Name')
        self.medicines_tree.heading('Quantity', text='Quantity')
        self.medicines_tree.heading('Cost', text='Cost')
        self.medicines_tree.heading('Expiry Date', text='Expiry Date')

        # Grid
        self.medicine_id_label.grid(row=0, column=0)
        self.medicine_id_entry.grid(row=0, column=1)

        self.medicine_name_label.grid(row=1, column=0)
        self.medicine_name_entry.grid(row=1, column=1)

        self.medicine_quantity_label.grid(row=2, column=0)
        self.medicine_quantity_entry.grid(row=2, column=1)

        self.medicine_cost_label.grid(row=3, column=0)
        self.medicine_cost_entry.grid(row=3, column=1)

        self.medicine_expiry_label.grid(row=4, column=0)
        self.medicine_expiry_entry.grid(row=4, column=1)

        self.add_medicine_button.grid(row=5, column=0, columnspan=2)
        self.edit_medicine_button.grid(row=5, column=2, columnspan=2)
        self.update_medicine_button.grid(row=5, column=4, columnspan=2)
        self.delete_medicine_button.grid(row=5, column=6, columnspan=2)

        self.medicines_tree.grid(row=10, column=0, columnspan=8)

        # Load Medicines on startup
        self.load_medicines()

    def add_medicine(self):
        name = self.medicine_name_entry.get()
        quantity = self.medicine_quantity_entry.get()
        cost = self.medicine_cost_entry.get()
        expiry_date = self.medicine_expiry_entry.get()

        # Inserting data into the 'pharmacy' table
        cursor.execute("INSERT INTO pharmacy (medicine_name, quantity, price, expiry_date) VALUES (%s, %s, %s, %s)",
                       (name, quantity, cost, expiry_date))
        db.commit()

        # Update the medicine list
        self.load_medicines()

    def edit_medicine(self):
        selected_item = self.medicines_tree.selection()
        if selected_item:
            medicine_id, name, quantity, cost, expiry_date = self.medicines_tree.item(selected_item, 'values')
            self.medicine_name_entry.delete(0, tk.END)
            self.medicine_quantity_entry.delete(0, tk.END)
            self.medicine_cost_entry.delete(0, tk.END)
            self.medicine_expiry_entry.delete(0, tk.END)
            self.medicine_name_entry.insert(0, name)
            self.medicine_quantity_entry.insert(0, quantity)
            self.medicine_cost_entry.insert(0, cost)
            self.medicine_expiry_entry.insert(0, expiry_date)

    def update_medicine(self):
        selected_item = self.medicines_tree.selection()
        if selected_item:
            medicine_id = self.medicines_tree.item(selected_item, 'values')[0]
            name = self.medicine_name_entry.get()
            quantity = self.medicine_quantity_entry.get()
            cost = self.medicine_cost_entry.get()
            expiry_date = self.medicine_expiry_entry.get()

            # Updating data in the 'pharmacy' table
            cursor.execute("UPDATE pharmacy SET medicine_name=%s, quantity=%s, price=%s, expiry_date=%s WHERE id=%s",
                           (name, quantity, cost, expiry_date, medicine_id))
            db.commit()

            # Update the medicine list
            self.load_medicines()

    def delete_medicine(self):
        selected_item = self.medicines_tree.selection()
        if selected_item:
            medicine_id = self.medicines_tree.item(selected_item, 'values')[0]

            # Deleting data from the 'pharmacy' table
            cursor.execute("DELETE FROM pharmacy WHERE id=%s", (medicine_id,))
            db.commit()

            # Update the medicine list
            self.load_medicines()

    def load_medicines(self):
        # Clearing the existing data in the treeview
        for item in self.medicines_tree.get_children():
            self.medicines_tree.delete(item)

        # Fetching data from the 'pharmacy' table
        cursor.execute("SELECT * FROM pharmacy")
        medicines = cursor.fetchall()

        # Populating the treeview with the data
        for medicine in medicines:
            self.medicines_tree.insert("", "end", values=medicine)

    def get_patient_names(self):
        cursor.execute("SELECT name FROM patients")
        return [row[0] for row in cursor.fetchall()]

    def get_doctor_names(self):
        cursor.execute("SELECT name FROM doctors")
        return [row[0] for row in cursor.fetchall()]

    def get_patient_id_by_name(self, name):
        cursor.execute("SELECT id FROM patients WHERE name = %s", (name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_doctor_id_by_name(self, name):
        cursor.execute("SELECT id FROM doctors WHERE name = %s", (name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_patient_name_by_id(self, patient_id):
        cursor.execute("SELECT name FROM patients WHERE id = %s", (patient_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_doctor_name_by_id(self, doctor_id):
        cursor.execute("SELECT name FROM doctors WHERE id = %s", (doctor_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def create_report_tab(self):
        # Report Entry
        self.report_patient_label = tk.Label(self.report_tab, text="Patient:")
        self.report_patient_var = tk.StringVar(self.report_tab)
        self.report_patient_combobox = ttk.Combobox(self.report_tab, textvariable=self.report_patient_var,
                                                    values=self.get_patient_names())

        self.report_doctor_label = tk.Label(self.report_tab, text="Doctor:")
        self.report_doctor_var = tk.StringVar(self.report_tab)
        self.report_doctor_combobox = ttk.Combobox(self.report_tab, textvariable=self.report_doctor_var,
                                                    values=self.get_doctor_names())

        self.diagnosis_label = tk.Label(self.report_tab, text="Diagnosis:")
        self.diagnosis_entry = tk.Entry(self.report_tab)

        self.medicine_prescribed_label = tk.Label(self.report_tab, text="Medicine Prescribed:")
        self.medicine_prescribed_entry = tk.Entry(self.report_tab)

        self.bill_amount_label = tk.Label(self.report_tab, text="Bill Amount:")
        self.bill_amount_entry = tk.Entry(self.report_tab)

        self.add_report_button = tk.Button(self.report_tab, text="Add Report", command=self.add_report)
        self.edit_report_button = tk.Button(self.report_tab, text="Edit Report", command=self.edit_report)
        self.update_report_button = tk.Button(self.report_tab, text="Update Report", command=self.update_report)
        self.delete_report_button = tk.Button(self.report_tab, text="Delete Report", command=self.delete_report)

        # Report Treeview
        self.reports_tree = ttk.Treeview(self.report_tab, columns=('ID', 'Patient', 'Doctor', 'Diagnosis', 'Medicine Prescribed', 'Bill Amount'))
        self.reports_tree.heading('ID', text='ID')
        self.reports_tree.heading('Patient', text='Patient')
        self.reports_tree.heading('Doctor', text='Doctor')
        self.reports_tree.heading('Diagnosis', text='Diagnosis')
        self.reports_tree.heading('Medicine Prescribed', text='Medicine Prescribed')
        self.reports_tree.heading('Bill Amount', text='Bill Amount')

        # Grid
        self.report_patient_label.grid(row=0, column=0)
        self.report_patient_combobox.grid(row=0, column=1)

        self.report_doctor_label.grid(row=1, column=0)
        self.report_doctor_combobox.grid(row=1, column=1)

        self.diagnosis_label.grid(row=2, column=0)
        self.diagnosis_entry.grid(row=2, column=1)

        self.medicine_prescribed_label.grid(row=3, column=0)
        self.medicine_prescribed_entry.grid(row=3, column=1)

        self.bill_amount_label.grid(row=4, column=0)
        self.bill_amount_entry.grid(row=4, column=1)

        self.add_report_button.grid(row=5, column=0, columnspan=2)
        self.edit_report_button.grid(row=5, column=2, columnspan=2)
        self.update_report_button.grid(row=5, column=4, columnspan=2)
        self.delete_report_button.grid(row=5, column=6, columnspan=2)

        self.reports_tree.grid(row=10, column=0, columnspan=8)

        # Load Reports on startup
        self.load_reports()

    def add_report(self):
        patient_name = self.report_patient_var.get()
        doctor_name = self.report_doctor_var.get()
        diagnosis = self.diagnosis_entry.get()
        medicine_prescribed = self.medicine_prescribed_entry.get()
        bill_amount = self.bill_amount_entry.get()

        # Get patient and doctor IDs
        patient_id = self.get_patient_id_by_name(patient_name)
        doctor_id = self.get_doctor_id_by_name(doctor_name)

        if patient_id and doctor_id:
            # Inserting data into the 'reports' table
            cursor.execute("INSERT INTO reports (patient_id, doctor_id, diagnosis, medicine_prescribed, bill_amount) VALUES (%s, %s, %s, %s, %s)",
                           (patient_id, doctor_id, diagnosis, medicine_prescribed, bill_amount))
            db.commit()

            # Update the report list
            self.load_reports()

    def edit_report(self):
        selected_item = self.reports_tree.selection()
        if selected_item:
            report_id, patient_name, doctor_name, diagnosis, medicine_prescribed, bill_amount = self.reports_tree.item(selected_item, 'values')
            self.report_patient_var.set(patient_name)
            self.report_doctor_var.set(doctor_name)
            self.diagnosis_entry.delete(0, tk.END)
            self.diagnosis_entry.insert(0, diagnosis)
            self.medicine_prescribed_entry.delete(0, tk.END)
            self.medicine_prescribed_entry.insert(0, medicine_prescribed)
            self.bill_amount_entry.delete(0, tk.END)
            self.bill_amount_entry.insert(0, bill_amount)

    def update_report(self):
        selected_item = self.reports_tree.selection()
        if selected_item:
            report_id = self.reports_tree.item(selected_item, 'values')[0]
            patient_name = self.report_patient_var.get()
            doctor_name = self.report_doctor_var.get()
            diagnosis = self.diagnosis_entry.get()
            medicine_prescribed = self.medicine_prescribed_entry.get()
            bill_amount = self.bill_amount_entry.get()

            # Get patient and doctor IDs
            patient_id = self.get_patient_id_by_name(patient_name)
            doctor_id = self.get_doctor_id_by_name(doctor_name)

            if patient_id and doctor_id:
                # Updating data in the 'reports' table
                cursor.execute("UPDATE reports SET patient_id=%s, doctor_id=%s, diagnosis=%s, medicine_prescribed=%s, bill_amount=%s WHERE id=%s",
                               (patient_id, doctor_id, diagnosis, medicine_prescribed, bill_amount, report_id))
                db.commit()

                # Update the report list
                self.load_reports()

    def delete_report(self):
        selected_item = self.reports_tree.selection()
        if selected_item:
            report_id = self.reports_tree.item(selected_item, 'values')[0]

            # Deleting data from the 'reports' table
            cursor.execute("DELETE FROM reports WHERE id=%s", (report_id,))
            db.commit()

            # Update the report list
            self.load_reports()

    def load_reports(self):
        # Clear existing items in the Treeview
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)

        # Fetch data from the 'reports' table
        cursor.execute("""
            SELECT reports.id, patients.name AS patient_name, doctors.name AS doctor_name, diagnosis, medicine_prescribed, bill_amount
            FROM reports
            INNER JOIN patients ON reports.patient_id = patients.id
            INNER JOIN doctors ON reports.doctor_id = doctors.id
        """)
        reports = cursor.fetchall()

        # Populate the Treeview with report data
        for report in reports:
            self.reports_tree.insert('', 'end', values=report)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementSystem(root)
    root.mainloop()
    