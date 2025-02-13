import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt  # Matplotlib is still included for future use

class HospitalManagementSystem:
    def __init__(self):
        # In-memory data structures
        self.patients = []
        self.doctors = []
        self.appointments = []
        self.feedbacks = []
        self.complaints = []
        self.billing_records = []
        self.token_queue = []  # List to manage tokens
        self.wards = {}  # Dictionary to hold ward information

    def add_patient(self, name, age, gender, ailment):
        patient_id = len(self.patients) + 1  # Simple ID generation
        token_number = len(self.token_queue) + 1  # Generate token number
        self.patients.append({"id": patient_id, "name": name, "age": age, "gender": gender, "ailment": ailment, "token": token_number})
        self.token_queue.append(token_number)  # Add token to the queue

    def add_doctor(self, name, specialization, contact):
        doctor_id = len(self.doctors) + 1  # Simple ID generation
        self.doctors.append({"id": doctor_id, "name": name, "specialization": specialization, "contact": contact})

    def schedule_appointment(self, patient_id, doctor_id, appointment_time):
        self.appointments.append({"patient_id": patient_id, "doctor_id": doctor_id, "appointment_time": appointment_time})

    def add_feedback(self, feedback):
        self.feedbacks.append(feedback)

    def add_complaint(self, complaint):
        self.complaints.append(complaint)

    def add_billing(self, patient_id, registration_charge, medicine_cost):
        total_cost = registration_charge + medicine_cost
        self.billing_records.append({"patient_id": patient_id, "registration_charge": registration_charge, "medicine_cost": medicine_cost, "total_cost": total_cost})

    def get_patients(self):
        return self.patients

    def get_doctors(self):
        return self.doctors

    def get_appointments(self):
        return self.appointments

    def add_ward(self, ward_name, total_beds):
        if ward_name not in self.wards:
            self.wards[ward_name] = {"total_beds": total_beds, "occupied_beds": 0}
            return True
        return False

    def assign_bed(self, ward_name):
        if ward_name in self.wards and self.wards[ward_name]["occupied_beds"] < self.wards[ward_name]["total_beds"]:
            self.wards[ward_name]["occupied_beds"] += 1
            return True
        return False

    def get_wards(self):
        return self.wards

    def get_next_token(self):
        if self.token_queue:
            return self.token_queue.pop(0)  # Return and remove the next token
        return None

    def send_reminder(self):
        for appointment in self.appointments:
            appointment_time = appointment["appointment_time"]
            if appointment_time <= datetime.now() + timedelta(days=1):  # Reminder for appointments within the next day
                patient = next((p for p in self.patients if p["id"] == appointment["patient_id"]), None)
                if patient:
                    messagebox.showinfo("Appointment Reminder", f"Reminder: {patient['name']}, you have an appointment scheduled on {appointment_time.strftime('%Y-%m-%d %H:%M')}.")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login")
        self.root.geometry("300x300")
        self.root.configure(bg="#e0f7fa")

        tk.Label(self.root, text="Admin ID:", font=("Arial", 12)).pack(pady=10)
        self.admin_id_entry = tk.Entry(self.root)
        self.admin_id_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=("Arial", 12)).pack(pady=10)
        self.admin_password_entry = tk.Entry(self.root, show='*')
        self.admin_password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.admin_login, bg="#4db6ac", fg="white").pack(pady=20)

    def admin_login(self):
        admin_id = self.admin_id_entry.get()
        admin_password = self.admin_password_entry.get()
        
        # Replace with actual admin credentials
        if admin_id == "admin" and admin_password == "password":
         self.root.destroy()  # Close the login window
         self.open_main_application()
        else:
            messagebox.showerror("Login Error", "Invalid Admin ID or Password")

    def open_main_application(self):
        main_app = tk.Tk()
        main_app.title("Hospital Management System")
        main_app.geometry("800x600")
        main_app.configure(bg="#e0f7fa")
        
        # Create tabs
        self.tab_control = ttk.Notebook(main_app)
        self.patient_tab = ttk.Frame(self.tab_control)
        self.doctor_tab = ttk.Frame(self.tab_control)
        self.appointment_tab = ttk.Frame(self.tab_control)
        self.feedback_tab = ttk.Frame(self.tab_control)
        self.complaint_tab = ttk.Frame(self.tab_control)
        self.billing_tab = ttk.Frame(self.tab_control)
        self.ward_tab = ttk.Frame(self.tab_control)  # New tab for ward management
        self.token_tab = ttk.Frame(self.tab_control)  # New tab for token management

        self.tab_control.add(self.patient_tab, text='Patients')
        self.tab_control.add(self.doctor_tab, text='Doctors')
        self.tab_control.add(self.appointment_tab, text='Appointments')
        self.tab_control.add(self.feedback_tab, text='Feedback')
        self.tab_control.add(self.complaint_tab, text='Complaints')
        self.tab_control.add(self.billing_tab, text='Billing')
        self.tab_control.add(self.token_tab, text='Tokens')  # Add token tab
        self.tab_control.add(self.ward_tab, text='Wards')  # Add ward tab
        self.tab_control.pack(expand=1, fill='both')

        self.hms = HospitalManagementSystem()
        self.create_patient_tab()
        self.create_doctor_tab()
        self.create_appointment_tab()
        self.create_feedback_tab()
        self.create_complaint_tab()
        self.create_billing_tab()
        self.create_token_tab()  # Create token management tab
        self.create_ward_tab()  # Create ward management tab

        # Call the reminder function periodically
        self.reminder_button = tk.Button(main_app, text="Send Reminders", command=self.hms.send_reminder, bg="#ffcc00", fg="black", font=("Arial", 12))
        self.reminder_button.pack(pady=10)

        # Button to show ward statistics
        self.show_ward_stats_button = tk.Button(main_app, text="Show Ward Statistics", command=self.show_ward_statistics, bg="#4db6ac", fg="white", font=("Arial", 12))
        self.show_ward_stats_button.pack(pady=10)

        # Contact option
        self.contact_button = tk.Button(main_app, text="Contact Support", command=self.contact_support, bg="#d32f2f", fg="white", font=("Arial", 12))
        self.contact_button.pack(pady=10)

        main_app.mainloop()

    def create_patient_tab(self):
        tk.Label(self.patient_tab, text="Patient Name:", bg="#e0f7fa").grid(row=0, column=0, padx=10, pady=10)
        self.patient_name_entry = tk.Entry(self.patient_tab)
        self.patient_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.patient_tab, text="Age:", bg="#e0f7fa").grid(row=1, column=0, padx=10, pady=10)
        self.patient_age_entry = tk.Entry(self.patient_tab)
        self.patient_age_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.patient_tab, text="Gender:", bg="#e0f7fa").grid(row=2, column=0, padx=10, pady=10)
        self.patient_gender_entry = ttk.Combobox(self.patient_tab, values=["Male", "Female"])
        self.patient_gender_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.patient_tab, text="Ailment:", bg="#e0f7fa").grid(row=3, column=0, padx=10, pady=10)
        self.patient_ailment_entry = tk.Entry(self.patient_tab)
        self.patient_ailment_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.patient_tab, text="Add Patient", command=self.add_patient, bg="#00796b", fg="white").grid(row=4, columnspan=2, pady=10)

        self.patient_listbox = tk.Listbox(self.patient_tab, width=50)
        self.patient_listbox.grid(row=5, columnspan=2, padx=10, pady=10)

        tk.Button(self.patient_tab, text="Sort Patients", command=self.sort_patients, bg="#ff9800", fg="white").grid(row=6, columnspan=2, pady=10)

        self.refresh_patient_list()

    def add_patient(self):
        name = self.patient_name_entry.get()
        age = self.patient_age_entry.get()
        gender = self.patient_gender_entry.get()
        ailment = self.patient_ailment_entry.get()
        if name and age.isdigit() and ailment and gender:
            self.hms.add_patient(name, int(age), gender, ailment)
            self.refresh_patient_list()
            self.patient_name_entry.delete(0, tk.END)
            self.patient_age_entry.delete(0, tk.END)
            self.patient_gender_entry.set('')  # Reset the gender dropdown
            self.patient_ailment_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Input Error", "Please enter valid patient details.")

    def refresh_patient_list(self):
        self.patient_listbox.delete(0, tk.END)
        patients = self.hms.get_patients()
        for patient in patients:
            self.patient_listbox.insert(tk.END, f"ID: {patient['id']}, Name: {patient['name']}, Age: {patient['age']}, Gender: {patient['gender']}, Ailment: {patient['ailment']}")

    def sort_patients(self):
        self.hms.patients.sort(key=lambda x: x['name'])  # Sort by patient name
        self.refresh_patient_list()

    def create_doctor_tab(self):
        tk.Label(self.doctor_tab, text="Doctor Name:", bg="#ffe0b2", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        self.doctor_name_entry = ttk.Combobox(self.doctor_tab, values=["Dr. A. Sharma", "Dr. R. Gupta", "Dr. S. Verma", "Dr. P. Singh", "Dr. N. Mehta", "Dr. K. Rao"], font=("Arial", 12))
        self.doctor_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.doctor_tab, text="Specialization:", bg="#ffe0b2", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.doctor_specialization_entry = ttk.Combobox(self.doctor_tab, values=["Cardiology", "Neurology", "Pediatrics", "Orthopedics", "General Medicine"], font=("Arial", 12))
        self.doctor_specialization_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.doctor_tab, text="Contact:", bg="#ffe0b2", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
        self.doctor_contact_entry = tk.Entry(self.doctor_tab, font=("Arial", 12))
        self.doctor_contact_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.doctor_tab, text="Add Doctor", command=self.add_doctor, bg="#4db6ac", fg="white", font=("Arial", 12)).grid(row=3, columnspan=2, pady=10)

        self.doctor_listbox = tk.Listbox(self.doctor_tab, width=50, font=("Arial", 12))
        self.doctor_listbox.grid(row=4, columnspan=2, padx=10, pady=10)

        self.refresh_doctor_list()

    def add_doctor(self):
        name = self.doctor_name_entry.get()
        specialization = self.doctor_specialization_entry.get()
        contact = self.doctor_contact_entry.get()
        if name and specialization and contact:
            self.hms.add_doctor(name, specialization, contact)
            self.refresh_doctor_list()
            self.doctor_name_entry.set('')  # Reset the doctor name dropdown
            self.doctor_specialization_entry.set('')  # Reset the specialization dropdown
            self.doctor_contact_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Input Error", "Please enter valid doctor details.")

    def refresh_doctor_list(self):
        self.doctor_listbox.delete(0, tk.END)
        doctors = self.hms.get_doctors()
        for doctor in doctors:
            self.doctor_listbox.insert(tk.END, f"ID: {doctor['id']}, Name: {doctor['name']}, Specialization: {doctor['specialization']}, Contact: {doctor['contact']}")

    def create_appointment_tab(self):
        tk.Label(self.appointment_tab, text="Patient ID:", bg="#c5e1a5", font=("Arial", 12)).grid(row=0, column=0)
        self.appointment_patient_id_entry = tk.Entry(self.appointment_tab, font=("Arial", 12))
        self.appointment_patient_id_entry.grid(row=0, column=1)

        tk.Label(self.appointment_tab, text="Doctor ID:", bg="#c5e1a5", font=("Arial", 12)).grid(row=1, column=0)
        self.appointment_doctor_id_entry = tk.Entry(self.appointment_tab, font=("Arial", 12))
        self.appointment_doctor_id_entry.grid(row=1, column=1)

        tk.Label(self.appointment_tab, text="Appointment Time:", bg="#c5e1a5", font=("Arial", 12)).grid(row=2, column=0)
        self.appointment_time_entry = tk.Entry(self.appointment_tab, font=("Arial", 12))
        self.appointment_time_entry.grid(row=2, column=1)

        tk.Button(self.appointment_tab, text="Schedule Appointment", command=self.schedule_appointment, bg="#4db6ac", fg="white", font=("Arial", 12)).grid(row=3, columnspan=2)

    def schedule_appointment(self):
        patient_id = self.appointment_patient_id_entry.get()
        doctor_id = self.appointment_doctor_id_entry.get()
        appointment_time = self.appointment_time_entry.get()
        if patient_id.isdigit() and doctor_id.isdigit() and appointment_time:
            try:
                appointment_time = datetime.strptime(appointment_time, '%Y-%m-%d %H:%M')
                self.hms.schedule_appointment(int(patient_id), int(doctor_id), appointment_time)
                messagebox.showinfo("Success", "Appointment scheduled successfully.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid appointment time (YYYY-MM-DD HH:MM).")
        else:
            messagebox.showerror("Input Error", "Please enter valid appointment details.")

    def create_feedback_tab(self):
        tk.Label(self.feedback_tab, text="Feedback:", bg="#ffe0b2", font=("Arial", 12)).grid(row=0, column=0)
        self.feedback_entry = tk.Text(self.feedback_tab, height=5, width=40, font=("Arial", 12))
        self.feedback_entry.grid(row=0, column=1)

        tk.Button(self.feedback_tab, text="Submit Feedback", command=self.submit_feedback, bg="#4db6ac", fg="white", font=("Arial", 12)).grid(row=1, columnspan=2)

        tk.Label(self.feedback_tab, text="Submitted Feedback:", bg="#ffe0b2", font=("Arial", 12)).grid(row=2, column=0)
        self.feedback_listbox = tk.Listbox(self.feedback_tab, width=50, height=5)
        self.feedback_listbox.grid(row=2, column=1)

        self.refresh_feedback_list()

    def submit_feedback(self):
        feedback = self.feedback_entry.get("1.0", tk.END).strip()
        if feedback:
            self.hms.add_feedback(feedback)
            messagebox.showinfo("Success", "Feedback submitted successfully.")
            self.feedback_entry.delete("1.0", tk.END)
            self.refresh_feedback_list()
        else:
            messagebox.showerror("Input Error", "Please enter your feedback.")

    def refresh_feedback_list(self):
        self.feedback_listbox.delete(0, tk.END)
        for feedback in self.hms.feedbacks:
            self.feedback_listbox.insert(tk.END, feedback)

    def create_complaint_tab(self):
        tk.Label(self.complaint_tab, text="Complaint:", bg="#ffccbc", font=("Arial", 12)).grid(row=0, column=0)
        self.complaint_entry = tk.Text(self.complaint_tab, height=5, width=40, font=("Arial", 12))
        self.complaint_entry.grid(row=0, column=1)

        tk.Button(self.complaint_tab, text="Submit Complaint", command=self.submit_complaint, bg="#d32f2f", fg="white", font=("Arial", 12)).grid(row=1, columnspan=2)

        tk.Label(self.complaint_tab, text="Submitted Complaints:", bg="#ffccbc", font=("Arial", 12)).grid(row=2, column=0)
        self.complaint_listbox = tk.Listbox(self.complaint_tab, width=50, height=5)
        self.complaint_listbox.grid(row=2, column=1)

        self.refresh_complaint_list()

    def submit_complaint(self):
        complaint = self.complaint_entry.get("1.0", tk.END).strip()
        if complaint:
            self.hms.add_complaint(complaint)
            messagebox.showinfo("Success", "Complaint submitted successfully.")
            self.complaint_entry.delete("1.0", tk.END)
            self.refresh_complaint_list()
        else:
            messagebox.showerror("Input Error", "Please enter your complaint.")

    def refresh_complaint_list(self):
        self.complaint_listbox.delete(0, tk.END)
        for complaint in self.hms.complaints:
            self.complaint_listbox.insert(tk.END, complaint)

    def create_billing_tab(self):
        tk.Label(self.billing_tab, text="Patient ID:", bg="#c5e1a5", font=("Arial", 12)).grid(row=0, column=0)
        self.billing_patient_id_entry = tk.Entry(self.billing_tab, font=("Arial", 12))
        self.billing_patient_id_entry.grid(row=0, column=1)

        tk.Label(self.billing_tab, text="Registration Charge:", bg="#c5e1a5", font=("Arial", 12)).grid(row=1, column=0)
        self.registration_charge_entry = tk.Entry(self.billing_tab, font=("Arial", 12))
        self.registration_charge_entry.grid(row=1, column=1)

        tk.Label(self.billing_tab, text="Medicine Cost:", bg="#c5e1a5", font=("Arial", 12)).grid(row=2, column=0)
        self.medicine_cost_entry = tk.Entry(self.billing_tab, font=("Arial", 12))
        self.medicine_cost_entry.grid(row=2, column=1)

        tk.Button(self.billing_tab, text="Add Billing", command=self.add_billing, bg="#4db6ac", fg="white", font=("Arial", 12)).grid(row=3, columnspan=2)

        tk.Button(self.billing_tab, text="Print Receipt", command=self.print_receipt, bg="#4caf50", fg="white", font=("Arial", 12)).grid(row=4, columnspan=2)

    def add_billing(self):
        patient_id = self.billing_patient_id_entry.get()
        registration_charge = self.registration_charge_entry.get()
        medicine_cost = self.medicine_cost_entry.get()
        if patient_id.isdigit() and registration_charge.isdigit() and medicine_cost.isdigit():
            self.hms.add_billing(int(patient_id), int(registration_charge), int(medicine_cost))
            messagebox.showinfo("Success", "Billing added successfully.")
            self.billing_patient_id_entry.delete(0, tk.END)
            self.registration_charge_entry.delete(0, tk.END)
            self.medicine_cost_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Input Error", "Please enter valid billing details.")

    def print_receipt(self):
        patient_id = self.billing_patient_id_entry.get()
        if patient_id.isdigit():
            patient_id = int(patient_id)
            for record in self.hms.billing_records:
                if record["patient_id"] == patient_id:
                    total_cost = record["total_cost"]
                    receipt = f"Receipt\n{'-'*20}\nPatient ID: {patient_id}\n"
                    receipt += f"Registration Charge: {record['registration_charge']} Rupees\n"
                    receipt += f"Medicine Cost: {record['medicine_cost']} Rupees\n"
                    receipt += f"Total Amount: {total_cost} Rupees\n"
                    messagebox.showinfo("Receipt", receipt)
                    return
            messagebox.showerror("Error", "No billing record found for this patient ID.")
        else:
            messagebox.showerror("Input Error", "Please enter a valid patient ID.")

    def create_token_tab(self):
        tk.Label(self.token_tab, text="Current Tokens:", bg="#e0f7fa").grid(row=0, column=0, padx=10, pady=10)
        self.token_listbox = tk.Listbox(self.token_tab, width=50)
        self.token_listbox.grid(row=1, columnspan=2, padx=10, pady=10)

        tk.Button(self.token_tab, text="Call Next Token", command=self.call_next_token, bg="#00796b", fg="white").grid(row=2, columnspan=2, pady=10)

        self.refresh_token_list()

    def call_next_token(self):
        next_token = self.hms.get_next_token()
        if next_token is not None:
            messagebox.showinfo("Next Token", f"Next token to be called: {next_token}")
            self.refresh_token_list()
        else:
            messagebox.showwarning("No Tokens", "No tokens available to call.")

    def refresh_token_list(self):
        self.token_listbox.delete(0, tk.END)
        for patient in self.hms.get_patients():
            self.token_listbox.insert(tk.END, f"Token: {patient['token']}, Patient: {patient['name']}")

    def create_ward_tab(self):
        tk.Label(self.ward_tab, text="Ward Name:", bg="#c5e1a5", font=("Arial", 12)).grid(row=0, column=0)
        self.ward_name_entry = tk.Entry(self.ward_tab, font=("Arial", 12))
        self.ward_name_entry.grid(row=0, column=1)

        tk.Label(self.ward_tab, text="Total Beds:", bg="#c5e1a5", font=("Arial", 12)).grid(row=1, column=0)
        self.total_beds_entry = tk.Entry(self.ward_tab, font=("Arial", 12))
        self.total_beds_entry.grid(row=1, column=1)

        tk.Button(self.ward_tab, text="Add Ward", command=self.add_ward, bg="#4db6ac", fg="white", font=("Arial", 12)).grid(row=2, columnspan=2)

        tk.Label(self.ward_tab, text="Available Wards:", bg="#c5e1a5", font=("Arial", 12)).grid(row=3, column=0)
        self.ward_listbox = tk.Listbox(self.ward_tab, width=50, height=5)
        self.ward_listbox.grid(row=3, column=1)

        self.refresh_ward_list()

    def add_ward(self):
        ward_name = self.ward_name_entry.get()
        total_beds = self.total_beds_entry.get()
        if ward_name and total_beds.isdigit():
            if self.hms.add_ward(ward_name, int(total_beds)):
                messagebox.showinfo("Success", "Ward added successfully.")
                self.refresh_ward_list()
                self.ward_name_entry.delete(0, tk.END)
                self.total_beds_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Ward already exists.")
        else:
            messagebox.showerror("Input Error", "Please enter valid ward details.")

    def refresh_ward_list(self):
        self.ward_listbox.delete(0, tk.END)
        for ward_name, details in self.hms.get_wards().items():
            self.ward_listbox.insert(tk.END, f"Ward: {ward_name}, Total Beds: {details['total_beds']}, Occupied Beds: {details['occupied_beds']}")

    def show_ward_statistics(self):
        ward_stats = "\n".join([f"Ward: {name}, Total Beds: {info['total_beds']}, Occupied Beds: {info['occupied_beds']}" for name, info in self.hms.get_wards().items()])
        messagebox.showinfo("Ward Statistics", ward_stats if ward_stats else "No wards available.")

    def contact_support(self):
        messagebox.showinfo("Contact Support", "For support, please contact us at: support@hospital.com or call +1234567890.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()