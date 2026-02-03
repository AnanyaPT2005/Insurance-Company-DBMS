import tkinter as tk
from tkinter import messagebox
import mysql.connector
import datetime
from tkinter import messagebox
from tkinter import Tk, Label, Entry, Button, messagebox, Toplevel
from tkinter import ttk

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",                
            password="DBMS2025@",    
            database="insurance_management"
        )
        
        return conn
    except mysql.connector.Error as err:
        print("❌ Connection error:", err)
        return None

users = {}

def login_user():
    username = entry_user.get()
    password = entry_pass.get()
    if username in users and users[username] == password:
        messagebox.showinfo("Success", f"Welcome {username}!")
        root.destroy()  # Close login window
        open_dashboard()
    else:
        messagebox.showerror("Error", "Invalid credentials")


root = tk.Tk()
root.title("Login Page")
root.geometry("600x400")


login_frame = tk.Frame(root)
login_frame.place(relx=0.5, rely=0.5, anchor='center')

tk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10)
entry_user = tk.Entry(login_frame)
entry_user.grid(row=0, column=1, padx=10, pady=10)

tk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10)
entry_pass = tk.Entry(login_frame, show="*")
entry_pass.grid(row=1, column=1, padx=10, pady=10)

login_btn = tk.Button(login_frame, text="Login", command=login_user)
login_btn.grid(row=2, column=0, columnspan=2, pady=20)

register_btn = tk.Button(login_frame, text="Register", command=lambda: open_register_window())
register_btn.grid(row=3, column=0, columnspan=2)

def open_register_window():
    reg_win = tk.Toplevel(root)
    reg_win.title("Register")
    reg_win.geometry("600x400")

    register_frame = tk.Frame(reg_win)
    register_frame.place(relx=0.5, rely=0.5, anchor='center')

    tk.Label(register_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    reg_user = tk.Entry(register_frame)
    reg_user.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(register_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    reg_pass = tk.Entry(register_frame, show="*")
    reg_pass.grid(row=1, column=1, padx=10, pady=10)

    def register_user():
        username = reg_user.get()
        password = reg_pass.get()
        if username in users:
            messagebox.showerror("Error, usernme already exists!")
        else:
            users[username]=password
           
           
            messagebox.showinfo("Success", "User registered successfully!")
            reg_win.destroy()

    register_btn = tk.Button(register_frame, text="Register", command=register_user)
    register_btn.grid(row=2, column=0, columnspan=2, pady=20)

def open_dashboard():
    dash = tk.Tk()
    dash.title("InsureMEDS")
    dash.geometry("600x400")

    tk.Label(dash, text="InsureMED", font=("Arial", 20)).pack(pady=20)

    # Buttons
    tk.Button(dash, text="View Patients", width=20, command=view_patients).pack(pady=10)
    tk.Button(dash, text="Add Patient", width=20, command=open_add_patient_form).pack(pady=10)
    tk.Button(dash, text="Edit Patient", width=20, command=open_edit_patient_window).pack(pady=10)
    tk.Button(dash, text="Delete Patient", width=20, command=open_delete_patient_window).pack(pady=10)
    


    dash.mainloop()



def open_add_patient_form():
    add_window = Toplevel()
    add_window.title("Add Patient")
    add_window.geometry("400x400")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DBMS2025@",
        database="insurance_management"
    )
    cursor = conn.cursor()

    
    def place_label_entry(label_text, row):
        Label(add_window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = Entry(add_window, width=30)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    name_entry = place_label_entry("Name:", 0)
    gender_entry = place_label_entry("Gender (M/F):", 1)
    age_entry = place_label_entry("Age:", 2)
    phone_entry = place_label_entry("Phone No:", 3)
    email_entry = place_label_entry("Email:", 4)

    

    def save_patient():
        name = name_entry.get()
        gender = gender_entry.get()
        age = age_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        last_updated = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not (name and gender and age and phone and email):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO patient (name, Gender, Age, PhoneNo, email)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, gender, age, phone, email))
            conn.commit()
            messagebox.showinfo("Success", "Patient added successfully!")
            add_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add patient: {e}")

    Button(add_window, text="Save Patient", command=save_patient).grid(row=6, column=0, columnspan=2, pady=20)

    conn.commit()




def view_patients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient")
        rows = cursor.fetchall()
        conn.close()

        view_win = tk.Toplevel()
        view_win.title("Patient Records")
        view_win.geometry("1200x1000")

        cols = ['PatientID', 'Name', 'Gender', 'Age', 'PhoneNo', 'Email']
        for idx, col in enumerate(cols):
            tk.Label(view_win, text=col, relief="solid", width=15, bg="lightblue").grid(row=0, column=idx)

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                tk.Label(view_win, text=val, relief="solid", width=15).grid(row=i+1, column=j)

        # Add PID section after rows
        row_offset = len(rows) + 2
        tk.Label(view_win, text="Enter PatientID to view full details:", font=("Arial", 11)).grid(row=row_offset, column=0, columnspan=2, pady=(20, 5), sticky="w")

        pid_entry = tk.Entry(view_win)
        pid_entry.grid(row=row_offset + 1, column=0, pady=5, sticky="w")

        tk.Button(view_win, text="View Details", command=lambda: fetch_patientid_details(pid_entry.get(), view_win)).grid(row=row_offset + 2, column=0, pady=10, sticky="w")

    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to fetch records:\n{e}")
        tk.Button(pid_frame, text="Back", command=clear_patient_details).grid(row=3, column=0, pady=5, sticky="w")


def fetch_patientid_details(pid, parent_window,):
    current_row = 0  
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

       
        details_window = tk.Toplevel(parent_window)
        details_window.title(f"Details for Patient ID {pid}")
        details_window.geometry("1200x600")

        
        canvas = tk.Canvas(details_window)
        scrollbar = tk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Display patient details (info fetched from the database)
        cursor.execute("SELECT * FROM patient WHERE PatientID = %s", (pid,))
        patient = cursor.fetchone()
        if patient:
            tk.Label(scrollable_frame, text=f"Patient ID: {patient[0]}",anchor="w",justify="left",width=50, font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)
            tk.Label(scrollable_frame, text=f"Name: {patient[1]}",anchor="w",justify="left",width=50, font=("Arial", 10)).grid(row=1, column=0, pady=5)
            tk.Label(scrollable_frame, text=f"Gender: {patient[2]}" , anchor="w",justify="left",width=50, font=("Arial", 10)).grid(row=2, column=0, pady=5)
            tk.Label(scrollable_frame, text=f"Age: {patient[3]}",anchor="w",justify="left",width=50, font=("Arial", 10)).grid(row=3, column=0, pady=5)
            tk.Label(scrollable_frame, text=f"Phone: {patient[4]}",anchor="w",justify="left",width=50, font=("Arial", 10)).grid(row=4, column=0, pady=5)
            tk.Label(scrollable_frame, text=f"Email: {patient[5]}", anchor="w",justify="left",width=50,font=("Arial", 10)).grid(row=5, column=0, pady=5)
        current_row=6
        # Fetch and display the medbill details
        cursor.execute("SELECT billID, date, Amount, Item, Hospital_name FROM medbill WHERE PatientID = %s", (pid,))
        bills = cursor.fetchall()
        tk.Label(scrollable_frame, text="Medical Bills:", font=("Arial", 12, "bold")).grid(row=6, column=0, pady=5, sticky="w")
            
    
        tk.Button(scrollable_frame, text="Add Medbill", command=lambda: add_medbill(pid, scrollable_frame)).grid(row=7, column=0, pady=5, sticky="w")
        tk.Button(scrollable_frame, text="Edit Medbill", command=lambda: edit_medbill(scrollable_frame)).grid(row=7, column=1, pady=5, sticky="w")
        tk.Button(scrollable_frame, text="Delete Medbill", command=lambda: delete_medbill_window(pid, scrollable_frame)).grid(row=7, column=2, pady=5, sticky="w")
        current_row=8
        if bills:
            
    
            bill_tree = ttk.Treeview(scrollable_frame, columns=("ID", "Date", "Amount", "Item", "Hospital"), show='headings')
            for col in bill_tree["columns"]:
                bill_tree.heading(col, text=col)
                bill_tree.column(col, anchor="w")  # Ensure left alignment

            for row in bills:
                bill_tree.insert("", "end", values=row)

            bill_tree.grid(row=8, column=0, columnspan=6, pady=5, sticky="w")
           
        current_row += 2
        next_row = current_row

        # --- Doctor Section ---
        cursor.execute("SELECT doctorID, DrName, Department, Hosptal_Name FROM doctor WHERE PatientID = %s", (pid,))
        doctors = cursor.fetchall()
        tk.Label(scrollable_frame, text="Doctor Details:", font=("Arial", 12, "bold")).grid(row=next_row, column=0, pady=5, sticky="w")

        next_row += 1
            
        tk.Button(scrollable_frame, text="Add Doctor", command=lambda: add_doctor(pid, scrollable_frame)).grid(row=next_row, column=0, pady=5, sticky="w")
        tk.Button(scrollable_frame, text="Edit Doctor", command=lambda: edit_doctor(scrollable_frame)).grid(row=next_row, column=1, pady=5, sticky="w")
        tk.Button(scrollable_frame, text="Delete Doctor", command=lambda: delete_doctor_window(pid, scrollable_frame)).grid(row=next_row, column=2, pady=5, sticky="w")

        next_row += 1
        if doctors:
           
            doctor_tree = ttk.Treeview(scrollable_frame, columns=("Doctor ID","DrName", "Department", "Hospital"), show='headings')
            for col in doctor_tree["columns"]:
                doctor_tree.heading(col, text=col)
                doctor_tree.column(col, anchor="w")

            for row in doctors:
                doctor_tree.insert("", "end", values=row)

            doctor_tree.grid(row=next_row, column=0, columnspan=6, pady=5, sticky="w")
            next_row += 2

                # Fetch and display the policy details
        cursor.execute("SELECT policyNo, policy_name, Monthly_payment, Dues, Start_date, End_date FROM policy WHERE PatientID = %s", (pid,))
        policies = cursor.fetchall()
        
        tk.Label(scrollable_frame, text="Policy Details:", font=("Arial", 12, "bold")).grid(row=next_row, column=0, pady=5, sticky="w")
        
       
        tk.Button(scrollable_frame, text="Add Policy", command=lambda: add_policy(pid, scrollable_frame)).grid(row=next_row+1, column=0, pady=5, sticky="w")
        tk.Button(scrollable_frame, text="Edit Policy", command=lambda: edit_policy(pid, scrollable_frame)).grid(row=next_row+1, column=1, pady=5, sticky="w")
        tk.Button(scrollable_frame, text="Delete Policy", command=lambda: delete_policy(pid, scrollable_frame)).grid(row=next_row+1, column=2, pady=5, sticky="w")
        
        policy_table_row = next_row + 2
        if policies:
         
            policy_tree = ttk.Treeview(scrollable_frame, columns=("Policy No", "Policy Name", "Monthly Payment", "Dues", "Start Date", "End Date"), show='headings')
            for col in policy_tree["columns"]:
                policy_tree.heading(col, text=col)
                policy_tree.column(col, anchor="w")  # Left align

            for row in policies:
                policy_tree.insert("", "end", values=row)

            policy_tree.grid(row=policy_table_row, column=0, columnspan=6, pady=5, sticky="w")
        
        next_row = policy_table_row + 2


        # Insurance & Claim Section
        cursor.execute("""
            SELECT i.InsureID, i.policyNo, c.claimID, i.claim_amount,  c.Claim_approval, c.Status 
            FROM insurance i 
            JOIN claim c ON i.claimID = c.claimID 
            WHERE i.PatientID = %s
        """, (pid,))
        insurance_data = cursor.fetchall()
        tk.Label(scrollable_frame, text="Insurance & Claim Details:", font=("Arial", 12, "bold")).grid(row=next_row, column=0, pady=5, sticky="w")

        next_row += 1
            
        tk.Button(scrollable_frame, text="Add Insurance", command=lambda: add_insurance(pid, scrollable_frame)).grid(row=next_row, column=0, pady=5, sticky="w")
        tk.Button(scrollable_frame, text="Edit Insurance", command=lambda: edit_insurance(scrollable_frame)).grid(row=next_row, column=1, pady=5, sticky="w")
        tk.Button(scrollable_frame, text="Delete Insurance", command=lambda: delete_insurance_window(pid, scrollable_frame)).grid(row=next_row, column=2, pady=5, sticky="w")

        next_row += 1
        if insurance_data:
            
            ins_tree = ttk.Treeview(scrollable_frame, columns=("Insurance ID","Policy No","Claim ID", "Claim Amount", "Approval", "Status"), show='headings')
            for col in ins_tree["columns"]:
                ins_tree.heading(col, text=col)
                ins_tree.column(col, anchor="w")

            for row in insurance_data:
                ins_tree.insert("", "end", values=row)

            ins_tree.grid(row=next_row, column=0, columnspan=6, pady=5, sticky="w")
            next_row += 2

    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to fetch patient details:\n{e}") 



def clear_patient_details(scrollable_frame):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    details_window.destroy()


def add_medbill(patient_id, scrollable_frame):
    add_bill_window = Toplevel()
    add_bill_window.title("Add Medical Bill")
    add_bill_window.geometry("400x400")

    
    Label(add_bill_window, text="Bill ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    billid_entry = Entry(add_bill_window)
    billid_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(add_bill_window, text="Date:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    date_entry = Entry(add_bill_window)
    date_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(add_bill_window, text="Amount:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    amount_entry = Entry(add_bill_window)
    amount_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(add_bill_window, text="Item:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    item_entry = Entry(add_bill_window)
    item_entry.grid(row=3, column=1, padx=10, pady=5)

    Label(add_bill_window, text="Hospital:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    hospital_entry = Entry(add_bill_window)
    hospital_entry.grid(row=4, column=1, padx=10, pady=5)

    def save_medbill():
        bill_id = billid_entry.get()
        date = date_entry.get()
        amount = amount_entry.get()
        item = item_entry.get()
        hospital = hospital_entry.get()

     
        if not (bill_id and date and amount and item and hospital):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
           
            bill_id = int(bill_id)

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="DBMS2025@",
                database="insurance_management"
            )
            cursor = conn.cursor()

            
            query = """
                INSERT INTO medbill (billID, PatientID, date, Amount, Item, Hospital_name)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (bill_id, patient_id, date, amount, item, hospital))
            conn.commit()

            messagebox.showinfo("Success", "Medical bill added successfully!")

            add_bill_window.destroy()
            fetch_patientid_details(patient_id, scrollable_frame)  

        except ValueError:
            messagebox.showerror("Error", "Bill ID must be an integer")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add medical bill: {e}")

    Button(add_bill_window, text="Save Bill", command=save_medbill).grid(row=5, column=0, columnspan=2, pady=20)

def edit_medbill(scrollable_frame):
    edit_window = tk.Toplevel()
    edit_window.title("Edit Medical Bill")
    edit_window.geometry("400x400")

   
    tk.Label(edit_window, text="Enter BillID to edit:").pack(pady=5)
    bill_id_entry = tk.Entry(edit_window)
    bill_id_entry.pack(pady=5)

    def fetch_and_edit():
        bill_id = bill_id_entry.get()
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM medbill WHERE billID = %s", (bill_id,))
        bill = cursor.fetchone()

        if not bill:
            messagebox.showerror("Error", "Medical bill not found.")
            return

       
        labels = ["PatientID", "Date (YYYY-MM-DD)", "Amount", "Item", "Hospital Name"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(edit_window, text=label).pack()
            entry = tk.Entry(edit_window)
            entry.insert(0, bill[i + 1])  
            entry.pack()
            entries.append(entry)

        def save_changes():
            try:
                patient_id = entries[0].get()
                date = entries[1].get()
                amount = entries[2].get()
                item = entries[3].get()
                hospital = entries[4].get()

                cursor.execute("""
                    UPDATE medbill
                    SET PatientID=%s, date=%s, Amount=%s, Item=%s, Hospital_name=%s
                    WHERE billID=%s
                """, (patient_id, date, amount, item, hospital, bill_id))
                conn.commit()
                messagebox.showinfo("Success", "Medical bill updated successfully.")
                edit_window.destroy()
                refresh_scrollable_window(patient_id, scrollable_frame)  

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update bill: {e}")

        tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)

    tk.Button(edit_window, text="Fetch Bill", command=fetch_and_edit).pack(pady=10)

def delete_medbill_window(patient_id, scrollable_frame):
    delete_window = tk.Toplevel()
    delete_window.title("Delete Medical Bill")
    delete_window.geometry("300x150")

    Label(delete_window, text="Enter Bill ID to delete:").pack(pady=10)
    billid_entry = Entry(delete_window)
    billid_entry.pack()

    def delete_medbill():
        bill_id = billid_entry.get()
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="DBMS2025@",
                database="insurance_management"
            )
            cursor = conn.cursor()

            
            cursor.execute("SELECT * FROM medbill WHERE billID = %s AND PatientID = %s", (bill_id, patient_id))
            if cursor.fetchone() is None:
                messagebox.showerror("Error", "Medical Bill ID not found for the given patient.")
            else:
                cursor.execute("DELETE FROM medbill WHERE billID = %s", (bill_id,))
                conn.commit()
                messagebox.showinfo("Success", f"Medical Bill {bill_id} deleted.")
                refresh_scrollable_window(patient_id, scrollable_frame) 
                delete_window.destroy()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(delete_window, text="Delete", command=delete_medbill).pack(pady=10)




def refresh_scrollable_window(patient_id, scrollable_frame):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    fetch_patientid_details(patient_id, scrollable_frame)


def add_doctor(patient_id, scrollable_frame):
    add_window = Toplevel()
    add_window.title("Add Doctor")
    add_window.geometry("400x400")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DBMS2025@",
        database="insurance_management"
    )
    cursor = conn.cursor()

    def place_label_entry(label_text, row):
        Label(add_window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = Entry(add_window, width=30)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

   
    doctorid_entry = place_label_entry("Doctor ID:", 0)  
    drname_entry = place_label_entry("Doctor's Name:", 1)
    department_entry = place_label_entry("Department:", 2)
    hospital_entry = place_label_entry("Hospital Name:", 3)

    
    def save_doctor():
        doctor_id = doctorid_entry.get()  
        drname = drname_entry.get()
        department = department_entry.get()
        hospital = hospital_entry.get()

        if not (doctor_id and drname and department and hospital):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO doctor (doctorID, PatientID, DrName, Department, Hosptal_Name)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (doctor_id, patient_id, drname, department, hospital))
            conn.commit()
            messagebox.showinfo("Success", "Doctor details added successfully!")
            refresh_scrollable_window(patient_id, scrollable_frame)

            add_window.destroy()


        except Exception as e:
            messagebox.showerror("Error", f"Failed to add doctor: {e}")

   
    Button(add_window, text="Save Doctor", command=save_doctor).grid(row=4, column=0, columnspan=2, pady=20)

    conn.commit()

def edit_doctor(scrollable_frame):
    edit_window = tk.Toplevel()
    edit_window.title("Edit Doctor Details")
    edit_window.geometry("400x350")


    tk.Label(edit_window, text="Enter DoctorID to edit:").pack(pady=5)
    doc_id_entry = tk.Entry(edit_window)
    doc_id_entry.pack(pady=5)

    def fetch_and_edit():
        doctor_id = doc_id_entry.get()
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM doctor WHERE doctorID = %s", (doctor_id,))
        doctor = cursor.fetchone()

        if not doctor:
            messagebox.showerror("Error", "Doctor not found.")
            return

        labels = ["PatientID", "DrName", "Department", "Hospital Name"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(edit_window, text=label).pack()
            entry = tk.Entry(edit_window)
            entry.insert(0, doctor[i + 1])  
            entry.pack()
            entries.append(entry)

        def save_changes():
            try:
                patient_id = entries[0].get()
                dr_name = entries[1].get()
                department = entries[2].get()
                hospital = entries[3].get()

                cursor.execute("""
                    UPDATE doctor
                    SET PatientID=%s, DrName=%s, Department=%s, Hosptal_Name=%s
                    WHERE doctorID=%s
                """, (patient_id, dr_name, department, hospital, doctor_id))
                conn.commit()
                messagebox.showinfo("Success", "Doctor details updated successfully.")
                edit_window.destroy()
                refresh_scrollable_window(patient_id, scrollable_frame)  

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update doctor: {e}")

        tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)

    tk.Button(edit_window, text="Fetch Doctor", command=fetch_and_edit).pack(pady=10)

def delete_doctor_window(patient_id, scrollable_frame):
    delete_window = tk.Toplevel()
    delete_window.title("Delete Doctor")
    delete_window.geometry("300x150")

    Label(delete_window, text="Enter Doctor ID to delete:").pack(pady=10)
    doctorid_entry = Entry(delete_window)
    doctorid_entry.pack()

    def delete_doctor():
        doctor_id = doctorid_entry.get()
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="DBMS2025@",
                database="insurance_management"
            )
            cursor = conn.cursor()

           
            cursor.execute("SELECT * FROM doctor WHERE doctorID = %s AND PatientID = %s", (doctor_id, patient_id))
            if cursor.fetchone() is None:
                messagebox.showerror("Error", "Doctor ID not found for the given patient.")
            else:
                cursor.execute("DELETE FROM doctor WHERE doctorID = %s", (doctor_id,))
                conn.commit()
                messagebox.showinfo("Success", f"Doctor {doctor_id} deleted.")
                refresh_scrollable_window(patient_id, scrollable_frame)  # Refresh the frame after deletion
                delete_window.destroy()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(delete_window, text="Delete", command=delete_doctor).pack(pady=10)


def add_policy(patient_id, scrollable_frame):
    add_policy_window = Toplevel()
    add_policy_window.title("Add Insurance Policy")
    add_policy_window.geometry("400x400")

    Label(add_policy_window, text="Policy No:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    policy_no_entry = Entry(add_policy_window)
    policy_no_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(add_policy_window, text="Policy Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    policy_name_entry = Entry(add_policy_window)
    policy_name_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(add_policy_window, text="Monthly Payment:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    monthly_payment_entry = Entry(add_policy_window)
    monthly_payment_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(add_policy_window, text="Dues:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    dues_entry = Entry(add_policy_window)
    dues_entry.grid(row=3, column=1, padx=10, pady=5)

    Label(add_policy_window, text="Start Date (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    start_date_entry = Entry(add_policy_window)
    start_date_entry.grid(row=4, column=1, padx=10, pady=5)

    Label(add_policy_window, text="End Date (YYYY-MM-DD):").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    end_date_entry = Entry(add_policy_window)
    end_date_entry.grid(row=5, column=1, padx=10, pady=5)

    def save_policy():
        policy_no = policy_no_entry.get()
        policy_name = policy_name_entry.get()
        monthly_payment = monthly_payment_entry.get()
        dues = dues_entry.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        
        if not (policy_no and policy_name and monthly_payment and dues and start_date and end_date):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
           
            policy_no = int(policy_no)

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="DBMS2025@",
                database="insurance_management"
            )
            cursor = conn.cursor()

            
            query = """
                INSERT INTO policy (policyNo, PatientID, policy_name, Monthly_payment, Dues, Start_date, End_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (policy_no, patient_id, policy_name, monthly_payment, dues, start_date, end_date))
            conn.commit()

            messagebox.showinfo("Success", "Policy added successfully!")

            add_policy_window.destroy()

            
            fetch_patientid_details(patient_id, scrollable_frame)

        except ValueError:
            messagebox.showerror("Error", "Policy No must be an integer")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add policy: {e}")

    Button(add_policy_window, text="Save Policy", command=save_policy).grid(row=6, column=0, columnspan=2, pady=20)

def edit_policy(pid, scrollable_frame):
    edit_window = tk.Toplevel()
    edit_window.title("Edit Policy Details")
    edit_window.geometry("400x350")

    
    tk.Label(edit_window, text="Enter PolicyNo to edit:").pack(pady=5)
    policy_no_entry = tk.Entry(edit_window)
    policy_no_entry.pack(pady=5)

    def fetch_and_edit():
        policy_no = policy_no_entry.get()
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM policy WHERE policyNo = %s", (policy_no,))
        policy = cursor.fetchone()

        if not policy:
            messagebox.showerror("Error", "Policy not found.")
            return

        labels = ["Policy Name", "Monthly Payment", "Dues", "End Date"]
        entries = []


        for i, label in enumerate(labels):
            tk.Label(edit_window, text=label).pack()
            entry = tk.Entry(edit_window)
            entry.insert(0, policy[i + 2])  
            entry.pack()
            entries.append(entry)

        def save_changes():
            try:
                policy_name = entries[0].get()
                monthly_payment = entries[1].get()
                dues = entries[2].get()
                end_date = entries[3].get()

                
                cursor.execute("""
                    UPDATE policy
                    SET policy_name=%s, Monthly_payment=%s, Dues=%s, End_date=%s
                    WHERE policyNo=%s
                """, (policy_name, monthly_payment, dues, end_date, policy_no))
                conn.commit()
                messagebox.showinfo("Success", "Policy details updated successfully.")
                edit_window.destroy()
                refresh_scrollable_window(pid, scrollable_frame)  

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update policy: {e}")

        tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)

    tk.Button(edit_window, text="Fetch Policy", command=fetch_and_edit).pack(pady=10)

def delete_policy(pid, scrollable_frame):
    delete_window = tk.Toplevel()
    delete_window.title("Delete Policy Details")
    delete_window.geometry("400x200")

   
    tk.Label(delete_window, text="Enter PolicyNo to delete:").pack(pady=5)
    policy_no_entry = tk.Entry(delete_window)
    policy_no_entry.pack(pady=5)

    def delete_policy_from_db():
        policy_no = policy_no_entry.get()
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="DBMS2025@",
                database="insurance_management"
            )
            cursor = conn.cursor()

            
            cursor.execute("DELETE FROM policy WHERE policyNo = %s", (policy_no,))
            conn.commit()
            messagebox.showinfo("Success", f"Policy with PolicyNo {policy_no} deleted.")
            refresh_scrollable_window(pid, scrollable_frame)  
            delete_window.destroy()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(delete_window, text="Delete", command=delete_policy_from_db).pack(pady=10)


def add_insurance(patient_id, scrollable_frame):
    add_window = Toplevel()
    add_window.title("Add Insurance and Claim Details")
    add_window.geometry("400x400")

    def place_entry(label, row):
        tk.Label(add_window, text=label).grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(add_window, width=30)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    policy_entry = place_entry("Policy No:", 0)
    claim_id_entry = place_entry("Claim ID:", 1)
    approval_entry = place_entry("Claim Approval amount:", 2)
    status_entry = place_entry("Status:", 3)

    def save():
        policy_no = policy_entry.get()
        claim_id = claim_id_entry.get()
        approval = approval_entry.get()
        status = status_entry.get()

        if not (policy_no and claim_id and approval and status):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="DBMS2025@",
                database="insurance_management"
            )
            cursor = conn.cursor()

            
            cursor.execute("""
                INSERT INTO insurance (InsureID, PatientID, claimID, policyNo)
                VALUES (%s, %s, %s, %s)
                """, (int(patient_id), int(patient_id), claim_id, policy_no))

            
            cursor.execute("""
                INSERT INTO claim (claimID, InsureID, Claim_approval, Status)
                VALUES (%s, %s, %s, %s)
            """, (claim_id, int(patient_id), approval, status))

            conn.commit()
            messagebox.showinfo("Success", "Insurance and claim details added successfully!")
            add_window.destroy()
            refresh_scrollable_window(patient_id, scrollable_frame)

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    tk.Button(add_window, text="Save", command=save).grid(row=5, column=0, columnspan=2, pady=20)

def edit_insurance(scrollable_frame):
    edit_window = tk.Toplevel()
    edit_window.title("Edit Insurance Details")
    edit_window.geometry("400x350")

    
    tk.Label(edit_window, text="Enter InsureID to edit:").pack(pady=5)
    insure_id_entry = tk.Entry(edit_window)
    insure_id_entry.pack(pady=5)

    def fetch_and_edit():
        insure_id = insure_id_entry.get()
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.InsureID, i.PatientID, i.policyNo, c.claim_approval, c.Status
            FROM insurance i
            JOIN claim c ON i.InsureID = c.InsureID
            WHERE i.InsureID = %s
        """, (insure_id,))
        insurance = cursor.fetchone()

        if not insurance:
            messagebox.showerror("Error", "Insurance record not found.")
            return

        labels = ["PatientID", "Policy Number", "Claim Approval", "Status"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(edit_window, text=label).pack()
            entry = tk.Entry(edit_window)
            entry.insert(0, insurance[i + 1])  
            entry.pack()
            entries.append(entry)

        def save_changes():
            try:
                patient_id = entries[0].get()
                policy_no = entries[1].get()
                claim_approval = entries[2].get()
                status = entries[3].get()


                cursor.execute("""
                    UPDATE insurance
                    SET PatientID=%s, policyNo=%s
                    WHERE InsureID=%s
                """, (patient_id, policy_no, insure_id))


                cursor.execute("""
                UPDATE claim
                SET claim_approval=%s, Status=%s
                WHERE InsureID=%s
                """, (claim_approval, status, insure_id))

                conn.commit()
                messagebox.showinfo("Success", "Insurance updated successfully.")
                edit_window.destroy()
                refresh_scrollable_window(patient_id, scrollable_frame)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update insurance: {e}")

        tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)

    tk.Button(edit_window, text="Fetch Insurance", command=fetch_and_edit).pack(pady=10)

def delete_insurance_window(patient_id, scrollable_frame):
    delete_window = tk.Toplevel()
    delete_window.title("Delete Insurance Details")
    delete_window.geometry("300x150")

    Label(delete_window, text="Enter Insurance ID to delete:").pack(pady=10)
    insureid_entry = Entry(delete_window)
    insureid_entry.pack()

    def delete_insurance():
        insure_id = insureid_entry.get()
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="DBMS2025@",
                database="insurance_management"
            )
            cursor = conn.cursor()

            
            cursor.execute("""
                SELECT i.InsureID, c.claimID 
                FROM insurance i
                LEFT JOIN claim c ON i.InsureID = c.InsureID
                WHERE i.PatientID = %s AND i.InsureID = %s
            """, (patient_id, insure_id))
            
            insurance = cursor.fetchone()

            if not insurance:
                messagebox.showerror("Error", "Insurance ID not found for the given patient.")
            else:
               
                cursor.execute("DELETE FROM claim WHERE InsureID = %s", (insure_id,))
                
                
                cursor.execute("DELETE FROM insurance WHERE InsureID = %s", (insure_id,))
                conn.commit()
                messagebox.showinfo("Success", f"Insurance details {insure_id} deleted.")
                refresh_scrollable_window(patient_id, scrollable_frame) 
                delete_window.destroy()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(delete_window, text="Delete", command=delete_insurance).pack(pady=10)



def open_edit_patient_window():
    edit_window = tk.Toplevel()
    edit_window.title("Edit Patient")
    edit_window.geometry("400x400")

   
    tk.Label(edit_window, text="Enter PatientID to edit:").pack(pady=5)
    pid_entry = tk.Entry(edit_window)
    pid_entry.pack(pady=5)

    def fetch_and_edit():
        pid = pid_entry.get()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient")
        rows = cursor.fetchall()
        cursor.execute("SELECT * FROM patient WHERE PatientID = %s", (pid,))
        patient = cursor.fetchone()

        if not patient:
            messagebox.showerror("Error", "Patient not found.")
            return

        
        labels = ["Name", "Gender", "Age", "PhoneNo", "Email"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(edit_window, text=label).pack()
            entry = tk.Entry(edit_window)
            entry.insert(0, patient[i + 1])  
            entry.pack()
            entries.append(entry)

        def save_changes():
            name = entries[0].get()
            gender = entries[1].get()
            age = entries[2].get()
            phone = entries[3].get()
            email = entries[4].get()

            try:
                cursor.execute("""
                    UPDATE patient 
                    SET name=%s, Gender=%s, Age=%s, PhoneNo=%s, email=%s
                    WHERE PatientID=%s
                """, (name, gender, age, phone, email, pid))
                conn.commit()
                messagebox.showinfo("Success", "Patient updated successfully.")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update patient: {e}")

        tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)

    tk.Button(edit_window, text="Fetch Patient", command=fetch_and_edit).pack(pady=10)


def open_delete_patient_window():
    delete_window = tk.Toplevel()
    delete_window.title("Delete Patient")
    delete_window.geometry("300x150")

    Label(delete_window, text="Enter Patient ID to delete:").pack(pady=10)
    pid_entry = Entry(delete_window)
    pid_entry.pack()

    def delete_patient():
        pid = pid_entry.get()
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="DBMS2025@",
                database="insurance_management"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM patient WHERE PatientID = %s", (pid,))
            if cursor.fetchone() is None:
                messagebox.showerror("Error", "Patient ID not found.")
            else:
                cursor.execute("DELETE FROM patient WHERE PatientID = %s", (pid,))
                conn.commit()
                messagebox.showinfo("Success", f"Patient {pid} deleted.")
                delete_window.destroy()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    

    Button(delete_window, text="Delete", command=delete_patient).pack(pady=10)

root.mainloop()
