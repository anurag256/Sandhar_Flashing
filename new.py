import customtkinter as ctk
import ttkbootstrap as tb
import tkinter as tk
import datetime
from tkinter import simpledialog, messagebox, filedialog, ttk
from hashlib import sha256
import os
import logging as my_log
from PLC_connect import PLC_reg
from Methods.method import log, read_serial_data
import subprocess
import re
import threading
import sqlite3
from PIL import Image, ImageTk


Setting_Password = '1234'
# selected_files = []  # This list will hold the selected file paths
file_list_1 = ['app.py', 'Path.txt']
file_list_2 = ['test.py', 'file_list_1.txt']

my_log.basicConfig(filename='Log.txt', level=my_log.INFO, format='%(asctime)s - %(message)s')

def check_password():
    while True:
        # Ask for password using a dialog
        password = simpledialog.askstring("Password", "Enter Password:", show='*')
        try:
            # Check if the entered password is correct
            hashed_password = sha256(password.encode()).hexdigest()
            CORRECT_PASSWORD = sha256(Setting_Password.encode()).hexdigest()
            print(f"hashed_password: {hashed_password}\nCurrent_password: {CORRECT_PASSWORD}")
            if hashed_password == CORRECT_PASSWORD:
                return True
            else:
                try_gaian = messagebox.askquestion('Window', 'Wrong Password, Retry!')
                if try_gaian == 'yes':
                    pass
                else:
                    return False
        except Exception as e:
            print(f"Error: {e}")
    

class FlashingApp:
    def __init__(self, root) -> None:
        style = ttk.Style()
        style.layout('TNotebook.tab', [])
        self.root = root
        # self.root.geometry('500x500')
        self.root.title('Flashing Dashboard')
        # self.root.set_default_color_theme('blue')

        self.root.attributes('-fullscreen', True)

        self.Current_Sift = ' '
        self.ok_count_1 = 0
        self.ng_count_1 = 0

        self.ok_count_2 = 0
        self.ng_count_2 = 0

        self.ok_count_3 = 0
        self.ng_count_3 = 0

        self.head_frame = ctk.CTkFrame(self.root, fg_color='#158aff', corner_radius=0)
        self.head_frame.pack(side=ctk.TOP, fill=ctk.X)
        self.head_frame.pack_propagate(False)
        self.head_frame.configure(height=60)

        note = ttk.Notebook(root)
        f1 = ttk.Frame(note)
        note.add(f1)

        self.menu_button = ctk.CTkButton(self.head_frame, text='Menu', fg_color='transparent', text_color='black', font=('bold', 20), corner_radius=0,
                                  hover_color='#42e5eb', border_width=0, height=60, width=75, command=self.my_menu)
        self.menu_button.pack(side=ctk.LEFT)

        self.head_title = ctk.CTkLabel(self.head_frame,text='Flashing Dashboard', fg_color='#158aff',
                                       text_color='#8f4136', font=('calibri', 55, 'bold'))
        self.head_title.pack(side=ctk.LEFT, expand=True)

        # Load image
        image_path = "Icons\sandhar_logo.png"  # Replace "path_to_image.jpg" with the path to your image file
        image = Image.open(image_path)
        # Resize image
        # new_width = 100  # Set the new width here
        # new_height = 100  # Set the new height here
        # resized_image = image.resize((new_width, new_height), 5)

        # Convert resized image to PhotoImage
        photo = ctk.CTkImage(image, size=[100,150])

        # Create a label to display the image
        self.image_label = ctk.CTkLabel(self.head_frame, text='', image=photo, height=60, width=60)
        self.image_label.pack(side=ctk.RIGHT)

        # photo = ctk.CTkImage("Icons\sandhar_logo.png")

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill=ctk.BOTH, expand=True)
        self.home_page()

        self.clock_header = ctk.CTkFrame(self.root, fg_color='skyblue')
        self.clock_header.pack(side=ctk.BOTTOM, fill=ctk.X)
        self.clock_header.pack_propagate(False)
        self.clock_header.configure(height=40)
        # Create clock label
        self.Current_Shift = ctk.CTkLabel(self.clock_header, font=('calibri', 25, 'bold'),
                                          text_color='green', fg_color='skyblue', height=40)
        self.Current_Shift.pack(side=ctk.LEFT)
        
        self.bottom_heading = ctk.CTkLabel(self.clock_header, text="Designed by VR Technologies", text_color='green', fg_color='skyblue',
                                        font=('calibri', 25, 'bold'), width=10, height=40)
        self.bottom_heading.pack(side=ctk.LEFT, expand=True)

        self.clock_label = ctk.CTkLabel(self.clock_header, text_color='green', fg_color='skyblue',
                                        font=('calibri', 25, 'bold'), width=10, height=40)
        self.clock_label.pack(side=ctk.RIGHT)
        self.my_clock()

        # Read configuration file
        # host, port = self.read_config()
        # # Set host and port values if they exist in the configuration file
        # if host and port:
        #     PLC_reg.host = host
        #     PLC_reg.port = port

    # Method to update UI based on serial data
    def update_ui(self):
        try:
            serial_data = read_serial_data('COM6', 9600)

            if serial_data == "1":  # Compare with string "1"
                batch_file = "testing.bat"
                hex_file = "C:\\Users\\anura\\OneDrive\\Documents\\test.hex"

                # Run the batch file with the hex file path as an argument
                result = subprocess.run([batch_file, hex_file], capture_output=True, text=True)

                # Print the output of the batch file
                if 'Result Code: 1' in result.stdout:
                    self.ng_count_1 +=1
                    print("Error:", result.stderr)
                    self.OK_NG_Status_1.configure(text='NG', text_color='red', font=('Helvetica', 90, 'bold'))
                    self.NG_Counter_1.configure(text=self.ng_count_1, font=('Helvetica', 90, 'bold'))

                    try:
                        conn = sqlite3.connect("C:\\Users\\anura\\OneDrive\\Documents\\Flasher\\Database\\test.db")
                        con = conn.cursor()
                        con.execute("INSERT INTO Line_1 (TIMESTAMP, DATE, DEVICE_ID, FIRMWARE_VER, DEVICE_CODE, STATUS) VALUES(?,?,?,?,?,?)",
                                    (datetime.datetime.now(), self.current_date, self.device_ID, self.firmware_ver, self.device_code, 'NG'))
                        conn.commit()
                        conn.close()
                        print("Data inserted successfully!")
                    except sqlite3.Error as e:
                        print("SQLite error:", e)
                    except Exception as e:
                        print("Error:", e)
                else:
                    if "Operation successful" in result.stdout:
                        try:
                            self.device_ID = re.search(r"Device:\s*(\w+)", result.stdout).group(1)
                            self.firmware_ver = re.search(r"Boot Firmware Version:\s*(\w+.\w+)", result.stdout).group(1)
                            self.device_code = re.search(r"Device Code:\s*(\w+ \w+ \w+)", result.stdout).group(1)
                            print(f"Device ID: {self.device_ID}")
                            print(f"Firmaware Version: {self.firmware_ver}")
                            print(f"Device Code: {self.device_code}")
                            try:
                                conn = sqlite3.connect("C:\\Users\\anura\\OneDrive\\Documents\\Flasher\\Database\\test.db")
                                con = conn.cursor()
                                con.execute("INSERT INTO Line_1 (TIMESTAMP, DATE, DEVICE_ID, FIRMWARE_VER, DEVICE_CODE, STATUS) VALUES(?,?,?,?,?,?)",
                                            (datetime.datetime.now(), self.current_date, self.device_ID, self.firmware_ver, self.device_code, 'OK'))
                                conn.commit()
                                conn.close()
                                print("Data inserted successfully!")
                            except sqlite3.Error as e:
                                print("SQLite error:", e)
                            except Exception as e:
                                print("Error:", e)

                        except Exception as e:
                            print(f"Error: {e}")
                        self.ok_count_1 +=1
                        print("Operation was successful!")
                        self.OK_NG_Status_1.configure(text='OK', text_color='green', font=('Helvetica', 90, 'bold'))
                        self.OK_Counter_1.configure(text=self.ok_count_1, font=('Helvetica', 90, 'bold'))
                    else:
                        print("Unexpected output:", result.stdout)
            else:
                pass
        except Exception as e:
            print(f"Error: {e}")
        # Call this method recursively to continuously check for serial data
        self.root.after(1000, self.update_ui)

# ********************************* Sidebar Menu ********************************* #
    def my_menu(self):
        def close_menu():
            self.menu_frame.destroy()
            self.menu_button.configure(text='Menu', command=self.my_menu)
        
        def close_app():
            exit_app = messagebox.askquestion('Exit Application', 'Do you really want to exit!')
            if exit_app == 'yes':
                print('Application Closed!')
                self.root.destroy()
            else:
                pass
        
        def switch_page(btn, page):
            for child in self.menu_frame.winfo_children():
                if isinstance(child, ctk.CTkButton):
                    child['text_color'] = 'white'
            btn['text_color'] = 'red'
            
            for child in self.main_frame.winfo_children():
                child.destroy()
                self.root.update()
            
            page()


        self.menu_frame = ctk.CTkFrame(self.root, fg_color='#82b8ed', width=200, corner_radius=0)

        home_button = ctk.CTkButton(self.menu_frame, text='Home', corner_radius=20, font=('bold', 20), border_color='black',
                            height=70, hover_color='#2de391', text_color='black', border_width=1, command=lambda: switch_page(home_button, self.home_page))
        home_button.pack(padx=30,pady=5,expand='true', side=ctk.TOP)

        Setting_button = ctk.CTkButton(self.menu_frame, text='Setting', corner_radius=20, font=('bold', 20), border_color='black',
                            height=70, hover_color='#2de391', text_color='black', border_width=1, command=lambda: switch_page(Setting_button, self.setting_page))
        Setting_button.pack(padx=30,pady=5,expand='true', side=ctk.TOP)

        Data_button = ctk.CTkButton(self.menu_frame, text='Data', corner_radius=20, font=('bold', 20), border_color='black',
                            height=70, hover_color='#2de391', text_color='black', border_width=1, command=lambda: switch_page(Data_button, self.Data_page))
        Data_button.pack(padx=30,pady=5,expand='true', side=ctk.TOP)

        Exit_button = ctk.CTkButton(self.menu_frame, text='Exit', corner_radius=20, font=('bold', 20), border_color='black',
                            height=70, hover_color='#2de391', text_color='black', border_width=1, command=close_app)
        Exit_button.pack(padx=30,pady=5,expand='true', side=ctk.TOP)

        self.menu_frame.place(x=0, y=60, relheight=0.92, relwidth=0.2)
        self.menu_button.configure(text='X', command=close_menu)

# ********************************* Home Page ********************************* #
    def home_page(self):
        my_home = ctk.CTkFrame(self.main_frame)
        
        # **************** Station_1 **************** #
        log_frame_1 = ctk.CTkFrame(my_home,  corner_radius=0, bg_color='transparent', fg_color='skyblue')

        self.Station_1 = ctk.CTkButton(log_frame_1, text='Station-1', corner_radius=20, font=('bold', 30), border_color='black',
                            height=50, border_width=1, state='DISABLED')
        self.Station_1.pack(pady=20, padx=10, fill=ctk.X)
        
        self.qr_lable_1 = ctk.CTkButton(log_frame_1, text='Barcode', corner_radius=10, font=('bold', 20), border_color='black',
                            height=30, width=200, border_width=1, state='DISABLED', fg_color='#8ee8a6', text_color='black')
        self.qr_lable_1.pack(pady=(30,10), padx=10)

        self.qr_box_1 = ctk.CTkTextbox(log_frame_1, height=50, width=300, fg_color='lightgray', text_color='black',font=('bold', 20))
        self.qr_box_1.pack()    # Barcode will come here

        self.part_status_1 = ctk.CTkButton(log_frame_1, text='Flashing Status', corner_radius=10, font=('bold', 20), border_color='black',
                            height=30, width=200, border_width=1, state='DISABLED', fg_color='#8ee8a6', text_color='black')
        self.part_status_1.pack(pady=(40,10), padx=10)
        self.OK_NG_Status_1 = ctk.CTkLabel(log_frame_1, text='Status', fg_color='gray',corner_radius=10,
                                         width=130, height=130, font=('Helvetica', 30, 'bold'))
        self.OK_NG_Status_1.pack(pady=0, padx=10)
        
        self.Count_1 = ctk.CTkButton(log_frame_1, text='Production', corner_radius=10, font=('bold', 20), border_color='black',
                            height=30, width=200, border_width=1, state='DISABLED', fg_color='#8ee8a6', text_color='black')
        self.Count_1.pack(pady=(40,10), padx=10)
        self.OK_Counter_1 = ctk.CTkLabel(log_frame_1, text='Count', fg_color='#49f24e',corner_radius=10, text_color='black',
                                         width=100, height=100, font=('Helvetica', 30, 'bold'))
        self.OK_Counter_1.pack(pady=0, padx=(40,0), side=ctk.LEFT)
        self.NG_Counter_1 = ctk.CTkLabel(log_frame_1, text='Count', fg_color='#f23333',corner_radius=10, text_color='black',
                                         width=100, height=100, font=('Helvetica', 30, 'bold'))
        self.NG_Counter_1.pack(pady=0, padx=(0,40), side=ctk.RIGHT)

        log_frame_1.pack(fill=ctk.BOTH, expand=True, side=ctk.LEFT)

        # **************** Station_2 **************** #
        log_frame_2 = ctk.CTkFrame(my_home,  corner_radius=0, bg_color='transparent', fg_color='skyblue')
        
        self.Station_2 = ctk.CTkButton(log_frame_2, text='Station-2', corner_radius=20, font=('bold', 30), border_color='black',
                            height=50, border_width=1, state='DISABLED')
        self.Station_2.pack(pady=20, padx=10, fill=ctk.X)
        
        self.qr_lable_2 = ctk.CTkButton(log_frame_2, text='Barcode', corner_radius=10, font=('bold', 20), border_color='black',
                            height=30, width=200, border_width=1, state='DISABLED', fg_color='#8ee8a6', text_color='black')
        self.qr_lable_2.pack(pady=(30,10), padx=10)

        self.qr_box_2 = ctk.CTkTextbox(log_frame_2, height=50, width=300, fg_color='lightgray', text_color='black',font=('bold', 20))
        self.qr_box_2.pack()

        self.part_status_2 = ctk.CTkButton(log_frame_2, text='Flashing Status', corner_radius=10, font=('bold', 20), border_color='black',
                            height=30, width=200, border_width=1, state='DISABLED', fg_color='#8ee8a6', text_color='black')
        self.part_status_2.pack(pady=(40,10), padx=10)
        self.OK_NG_Status_2 = ctk.CTkLabel(log_frame_2, text='Status', fg_color='gray',corner_radius=10,
                                         width=130, height=130, font=('Helvetica', 30, 'bold'))
        self.OK_NG_Status_2.pack(pady=0, padx=10)
        
        self.Count_2 = ctk.CTkButton(log_frame_2, text='Production', corner_radius=10, font=('bold', 20), border_color='black',
                            height=30, width=200, border_width=1, state='DISABLED', fg_color='#8ee8a6', text_color='black')
        self.Count_2.pack(pady=(40,10), padx=10)
        self.OK_Counter_2 = ctk.CTkLabel(log_frame_2, text='Count', fg_color='#49f24e',corner_radius=10, text_color='black',
                                         width=100, height=100, font=('Helvetica', 30, 'bold'))
        self.OK_Counter_2.pack(pady=0, padx=(40,0), side=ctk.LEFT)
        self.NG_Counter_2 = ctk.CTkLabel(log_frame_2, text='Count', fg_color='#f23333',corner_radius=10, text_color='black',
                                         width=100, height=100, font=('Helvetica', 30, 'bold'))
        self.NG_Counter_2.pack(pady=0, padx=(0,40), side=ctk.RIGHT)

        log_frame_2.pack(fill=ctk.BOTH, expand=True, side=ctk.LEFT)

        # **************** Station_3 **************** #
        log_frame_3 = ctk.CTkFrame(my_home,  corner_radius=0, bg_color='transparent', fg_color='skyblue')
        self.Station_3 = ctk.CTkButton(log_frame_3, text='Station-3', corner_radius=20, font=('bold', 30), border_color='black',
                            height=50, border_width=1, state='DISABLED')
        self.Station_3.pack(pady=20, padx=10, fill=ctk.X)
        
        self.qr_lable_3 = ctk.CTkButton(log_frame_3, text='Barcode', corner_radius=10, font=('bold', 20), border_color='black',
                            height=30, width=200, border_width=1, state='DISABLED', fg_color='#8ee8a6', text_color='black')
        self.qr_lable_3.pack(pady=(30,10), padx=10)

        self.qr_box_3 = ctk.CTkTextbox(log_frame_3, height=50, width=300, fg_color='lightgray', text_color='black',font=('bold', 20))
        self.qr_box_3.pack()

        self.part_status_3 = ctk.CTkButton(log_frame_3, text='Flashing Status', corner_radius=10, font=('bold', 20), border_color='black',
                            height=30, width=200, border_width=1, state='DISABLED', fg_color='#8ee8a6', text_color='black')
        self.part_status_3.pack(pady=(40,10), padx=10)
        self.OK_NG_Status_3 = ctk.CTkLabel(log_frame_3, text='Status', fg_color='gray',corner_radius=10,
                                         width=130, height=130, font=('Helvetica', 30, 'bold'))
        self.OK_NG_Status_3.pack(pady=0, padx=10)

        # Modify OK_NG Status
        # self.OK_NG_Status_1.configure(text='OK', text_color='Green', font=('Helvetica', 90, 'bold'))
        # self.OK_NG_Status_2.configure(text='NG', text_color='red', font=('Helvetica', 90, 'bold'))
        # self.OK_NG_Status_3.configure(text='OK', text_color='Green', font=('Helvetica', 90, 'bold'))
        
        self.Count_3 = ctk.CTkButton(log_frame_3, text='Production', corner_radius=10, font=('bold', 20), border_color='black',
                            height=30, width=200, border_width=1, state='DISABLED', fg_color='#8ee8a6', text_color='black')
        self.Count_3.pack(pady=(40,10), padx=10)
        self.OK_Counter_3 = ctk.CTkLabel(log_frame_3, text='Count', fg_color='#49f24e',corner_radius=10, text_color='black',
                                         width=100, height=100, font=('Helvetica', 30, 'bold'))
        self.OK_Counter_3.pack(pady=0, padx=(40,0), side=ctk.LEFT)
        self.NG_Counter_3 = ctk.CTkLabel(log_frame_3, text='Count', fg_color='#f23333',corner_radius=10, text_color='black',
                                         width=100, height=100, font=('Helvetica', 30, 'bold'))
        self.NG_Counter_3.pack(pady=0, padx=(0,40), side=ctk.RIGHT)
        log_frame_3.pack(fill=ctk.BOTH, expand=True, side=ctk.LEFT)

        # Initial log messages
        # msg = "Application started. \n"
        # log(self.pcb_log_1, msg)
        # log(self.pcb_log_2, msg)
        # log(self.pcb_log_3, msg)

        # self.upload_file(self.pcb_log_1, file_list_1, 'file_list_1.txt')
        # self.upload_file(self.pcb_log_2, file_list_1, 'file_list_2.txt')
        # self.upload_file(self.pcb_log_3, file_list_2, 'file_list_3.txt')

        my_home.pack(fill=ctk.BOTH, expand=True)
        # self.update_ui()
        # Start the update_ui function on a separate thread
        update_thread = threading.Thread(target=self.update_ui)
        update_thread.daemon = True  # Daemonize the thread so it automatically shuts down when the main program exits
        update_thread.start()

# ********************************* Setting Page ********************************* #
    def setting_page(self):
        if check_password() == True:
            my_setting = ctk.CTkFrame(self.main_frame, fg_color='skyblue', corner_radius=0)

            save_button = ctk.CTkButton(my_setting, text="Save")
            save_button.pack(pady=10)

            my_setting.pack(fill=ctk.BOTH, expand=True)

# ********************************* Data Page ********************************* #
    def Data_page(self):
        my_data = ctk.CTkFrame(self.main_frame, fg_color='skyblue', corner_radius=0)

        # data_head_frame = tb.Frame(my_data, bootstyle="info")
        # data_head_frame.pack(side=tb.TOP, fill=tb.X)
        # # data_head_frame.pack_propagate(False)
        # data_head_frame.configure(height=50)

        data_head_frame = ctk.CTkFrame(my_data, fg_color='#bbed55', corner_radius=0)
        data_head_frame.pack(side=ctk.TOP, fill=ctk.X)
        data_head_frame.pack_propagate(False)
        data_head_frame.configure(height=50)

        start_date_label = ctk.CTkLabel(data_head_frame, text='Start Date: ', text_color='black',
                                        fg_color='#bbed55', corner_radius=5, font=('bold', 20), bg_color='transparent')
        start_date_label.pack(pady=10, padx=10, side=tb.LEFT)
        start_date = tb.DateEntry(data_head_frame, firstweekday=0, bootstyle='primery')
        start_date.pack(pady=10, padx=10, side=tb.LEFT)
        starting_date = start_date.entry.get()
        print(starting_date)

        end_date_label = ctk.CTkLabel(data_head_frame, text='End Date: ', text_color='black',
                                        fg_color='#bbed55', corner_radius=5, font=('bold', 20), bg_color='transparent')
        end_date_label.pack(pady=10, padx=10, side=tb.LEFT)
        end_date = tb.DateEntry(data_head_frame, firstweekday=0, bootstyle='primery')
        end_date.pack(pady=10, padx=10, side=tb.LEFT)
        ending_date = start_date.entry.get()
        # print(starting_date)

        # data_fetch_button = ctk.CTkButton(data_head_frame, text='Fetch Data', border_color='black')

        optionmenu_var = ctk.StringVar(value="Station 1")  # set initial value
        combobox = ctk.CTkOptionMenu(master=data_head_frame,
                                            values=["Station 1", "Station 2", "Station 3"],
                                            command=lambda: optionmenu_callback(),
                                            width=150,
                                            bg_color='#158aff',
                                            variable=optionmenu_var)
        combobox.pack(padx=10, pady=10, side=ctk.LEFT)

        # auto_page_lbl = ctk.CTkLabel(my_data, text="this is auto", font=('Arial', 15), fg_color='black')
        # auto_page_lbl.pack(pady=80)
        my_data.pack(fill=ctk.BOTH, expand=True)

        def optionmenu_callback(choice):
            print(f"Data will show between from {choice}")

        self.head_frame.configure(fg_color='#158aff')
        self.clock_label.configure(fg_color='skyblue', text_color='green')
        self.Current_Shift.configure(fg_color='skyblue', text_color='green')

# ********************************* Real Time Clock ********************************* #
    def my_clock(self):
        self.current_time = datetime.datetime.now().strftime('%H:%M:%S %p')
        self.current_date = datetime.datetime.today().strftime('%d-%M-%Y')
        # self.Count_lable.configure(text=self.count)
        # self.count += 1
        # print(self.current_date)
        self.clock_label.configure(text=f'Date:{self.current_date}\tTime:{self.current_time}')
        self.Current_Shift.configure(text=f'Shift: {self.Current_Sift}')
        T1 = "08:00:00"
        T2 = "14:00:00"
        T3 = "20:00:00"
        self.clock_label.after(1000, self.my_clock)
        if (self.current_time > T1) and (self.current_time < T2):
            # print("Shift A")
            self.Current_Sift = 'A'
        elif (self.current_time > T2) and (self.current_time < T3):
            # print("Shift B")
            self.Current_Sift = 'B'
        else:
            # print("Shift C")
            self.Current_Sift = 'C'

# ********************* Create Log & Status ****************************** #
    def create_log_widget(self, parent, row, column):
        # Create and return a Text widget for logging
        log_widget = ctk.CTkTextbox(parent, height=20, width=54, state=ctk.DISABLED)
        log_widget.grid(row=row, column=column, padx=5, pady=5)
        return log_widget

    def create_status_label(self, parent, text, row, column):
        # Create and return a Label widget for displaying status
        status_label = ctk.CTkLabel(parent, text=text, fg_color='green', bg_color='white', width=30, height=5, font=('Helvetica', 12))
        status_label.grid(row=row, column=column, padx=5, pady=5)
        return status_label
    
# ********************* Change Path ********************************** #
    def change_path(self):
        # Ask the user to select a new path
        new_path = filedialog.askdirectory(title='Change Path')

        if new_path:
            print(f"Path Changed To: {new_path}")
            log_message = f"Path Changed To: {new_path} \n"
            log(self.path_log_text, log_message)

            # Update the last changed path
            self.last_path = new_path

            # Update the last changed path in the config file
            self.write_last_path(new_path)

    def read_last_path(self):
        try:
            with open("Path.txt", 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            return None

    def write_last_path(self, path):
        with open("Path.txt", 'w') as file:
            file.write(path)
    
# ********************* File Upload ********************************** #
    def file_selection_window(self, id, txt_file):
        list_of_files = []
        with open(txt_file) as f:
            myfile = f.read().split('\n')
            for file in myfile:
                list_of_files.append(file)
        def select_files():
            # Open file dialog and allow multiple file selection
            files = filedialog.askopenfilenames()

            # Convert result to a list
            file_list = list(files)

            # Add selected files to the listbox
            for file in file_list:
                listbox.insert(tk.END, file)

            # Update selected_files list with the new files
            list_of_files.extend(file_list)
            self.store_files(list_of_files, txt_file)

            log_message = f"{files} added Successfully.\n"
            log(id, log_message)

        def delete_file():
            # Get the index of the selected item
            selected_index = listbox.curselection()
            if selected_index:
                # Remove file from selected_files list
                delete = list_of_files.pop(selected_index[0])
                listbox.delete(selected_index)
                
            self.store_files(list_of_files, txt_file)
            log_message = f"{delete} deleted Successfully.\n"
            log(id, log_message)

        # Create a new window
        files_window = tk.Toplevel()
        files_window.title("File Selection")  # Set window title

        # Create listbox object
        listbox = tk.Listbox(files_window, height=10,
                        width=40,
                        bg="grey",
                        activestyle='dotbox',
                        font="Helvetica",
                        fg="yellow")

        # Fill listbox with previously selected files
        for file in list_of_files:
            listbox.insert(tk.END, file)

        # Define a label for the list
        label = tk.Label(files_window, text="Files List")

        # create a button to select files
        select_button = tk.Button(files_window, text="Select Files", command=select_files)

        # create a button to delete selected file
        delete_button = tk.Button(files_window, text="Delete File", command=delete_file)

        # pack the widgets
        label.pack()
        listbox.pack()
        select_button.pack()
        delete_button.pack()

    def upload_file(self, id, file_names, txt_file):
        temp_file_list = []
        try:
            last_path = self.read_last_path()
            initial_dir = last_path if last_path and os.path.exists(last_path) else "/"

            for file_name in file_names:
                file_path = os.path.join(initial_dir, file_name)
                if os.path.exists(file_path):
                    print(file_path)
                    temp_file_list.append(file_path)  # Append full file path instead of just the name
                    log_message = f"File Uploaded Successfully.\n"
                    self.write_last_path(last_path)
                    log(id, log_message)
                else:
                    print(f"File '{file_name}' not found in the initial directory.")
                    log(id, f"File '{file_name}' not found in the initial directory.")
            self.store_files(temp_file_list, txt_file)
        except Exception as e:
            log_message = f"Error Uploading File: {str(e)}\n"
            print(log_message)
            my_log.info(log_message)
            log(id, log_message)
        
        my_log.info(log_message)
        
        # Store selected files in separate files
        # self.store_files(selected_files, "file_list_1.txt")
        # self.store_files(selected_files, "file_list_2.txt")

    def store_files(self, file_list, file_name):
        with open(file_name, 'w') as file:
            for item in file_list:
                file.write("%s\n" % item)

    # def reset_screen(self):
    #     self.pcb_status_1.configure(text='-', text_color='gray',font=('Helvetica', 25, 'bold'))
    #     self.pcb_status_2.configure(text='-', text_color='gray',font=('Helvetica', 25, 'bold'))
    #     self.pcb_status_3.configure(text='-', text_color='gray',font=('Helvetica', 25, 'bold'))
        
    # def File_For_Flash(self):
    #     # msg = "Flashing... \n"
    #     # log(self.pcb_log_1, msg)
    #     # log(self.pcb_log_2, msg)
    #     # log(self.pcb_log_3, msg)

    #     # msg = "Flashing Done. \n"
    #     # log(self.pcb_log_1, msg)
    #     # log(self.pcb_log_2, msg)
    #     # log(self.pcb_log_3, msg)

    #     self.pcb_status_1.configure(text='OK', text_color='green',font=('Helvetica', 40, 'bold'))
    #     self.pcb_status_2.configure(text='OK', text_color='green',font=('Helvetica', 40, 'bold'))
    #     self.pcb_status_3.configure(text='OK', text_color='red',font=('Helvetica', 40, 'bold'))


# ********************************* Change PLC Config ********************************* #
    # def change_config(self):
    #     def new_config():
    #         confirm = messagebox.askyesno(title='Save', message='Do you want to save this ?')
    #         if confirm:
    #             plc.host = n_host.get()
    #             plc.port = n_port.get()
    #             print(plc.host)
    #             print(plc.port)
    #             popup.destroy()
    #         else:
    #             popup.destroy()
    #     # Example usage:
    #     plc = PLC_reg()
    #     print(plc.host)  # Output: 192.168.250.1
    #     print(plc.port)  # Output: 1200

    #     popup = ctk.CTkToplevel(root)
    #     popup.title("Popup Window")

    #     host_label = ctk.CTkLabel(popup, text="New Host")
    #     host_label.pack(padx=20, pady=10)

    #     n_host = ctk.CTkEntry(popup)
    #     n_host.pack(pady=5, padx=5)

    #     port_label = ctk.CTkLabel(popup, text="New Port")
    #     port_label.pack(padx=20, pady=10)

    #     n_port = ctk.CTkEntry(popup)
    #     n_port.pack(padx=5, pady=5)

    #     save_button = ctk.CTkButton(popup, text="Save", command=new_config)
    #     save_button.pack(pady=10)  

if __name__ == '__main__':
    root = ctk.CTk()
    app = FlashingApp(root)
    # pass_check = check_password()
    # if pass_check:
    #     app = FlashingApp(root)
    # else:
    #     root.destroy()
    root.mainloop()