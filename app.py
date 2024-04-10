import customtkinter as ctk
import ttkbootstrap as tb
import tkinter as tk
import datetime
from tkinter import simpledialog, messagebox, filedialog, ttk
from hashlib import sha256
import os
import logging as my_log
from PLC_connect import PLC_reg
from Methods.method import log


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
        self.root.title('LaserMarking')

        self.root.attributes('-fullscreen', True)

        self.Current_Sift = ' '
        self.count = 0

        self.head_frame = ctk.CTkFrame(self.root, fg_color='#158aff', corner_radius=0)
        self.head_frame.pack(side=ctk.TOP, fill=ctk.X)
        self.head_frame.pack_propagate(False)
        self.head_frame.configure(height=60)

        note = ttk.Notebook(root)
        f1 = ttk.Frame(note)
        note.add(f1)

        self.menu_button = ctk.CTkButton(self.head_frame, text='Menu', fg_color='#158aff', font=('bold', 20), corner_radius=0,
                                  hover_color='black', border_width=0, height=60, width=75, command=self.my_menu)
        self.menu_button.pack(side=ctk.LEFT)

        self.head_title = ctk.CTkLabel(self.head_frame,text='Flashing Dashboard', fg_color='#158aff',
                                       text_color='white', font=('calibri', 55, 'bold'))
        self.head_title.pack(side=ctk.TOP)

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill=ctk.BOTH, expand=True)
        self.home_page()

        self.clock_header = ctk.CTkFrame(self.root)
        self.clock_header.pack(side=ctk.BOTTOM, fill=ctk.X)
        self.clock_header.pack_propagate(False)
        self.clock_header.configure(height=40)
        # Create clock label
        self.clock_label = ctk.CTkLabel(self.clock_header, text_color='green', fg_color='black',
                                        font=('calibri', 25, 'bold'), width=10, height=40)
        self.clock_label.pack(side=ctk.RIGHT)

        self.Current_Shift = ctk.CTkLabel(self.clock_header, font=('calibri', 25, 'bold'),
                                          text_color='green', fg_color='black', height=40)
        self.Current_Shift.pack(side=ctk.LEFT)
        self.my_clock()

        # Read configuration file
        host, port = self.read_config()
        # Set host and port values if they exist in the configuration file
        if host and port:
            PLC_reg.host = host
            PLC_reg.port = port

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


        self.menu_frame = ctk.CTkFrame(self.root, fg_color='darkgray', width=200, corner_radius=0)

        home_button = ctk.CTkButton(self.menu_frame, text='Home', corner_radius=20, font=('bold', 20), border_color='black',
                            height=70, hover_color='black', border_width=1, command=lambda: switch_page(home_button, self.home_page))
        home_button.pack(padx=30,pady=5,expand='true', side=ctk.TOP)

        Setting_button = ctk.CTkButton(self.menu_frame, text='Setting', corner_radius=20, font=('bold', 20), border_color='black',
                            height=70, hover_color='black', border_width=1, command=lambda: switch_page(Setting_button, self.setting_page))
        Setting_button.pack(padx=30,pady=5,expand='true', side=ctk.TOP)

        Data_button = ctk.CTkButton(self.menu_frame, text='Data', corner_radius=20, font=('bold', 20), border_color='black',
                            height=70, hover_color='black', border_width=1, command=lambda: switch_page(Data_button, self.Data_page))
        Data_button.pack(padx=30,pady=5,expand='true', side=ctk.TOP)

        Exit_button = ctk.CTkButton(self.menu_frame, text='Exit', corner_radius=20, font=('bold', 20), border_color='black',
                            height=70, hover_color='black', border_width=1, command=close_app)
        Exit_button.pack(padx=30,pady=5,expand='true', side=ctk.TOP)

        self.menu_frame.place(x=0, y=50, relheight=0.95)
        self.menu_button.configure(text='X', command=close_menu)

# ********************************* Home Page ********************************* #
    def home_page(self):
        my_home = ctk.CTkFrame(self.main_frame)

        head_frame = ctk.CTkFrame(my_home, height=100)
        sn1_lable = ctk.CTkLabel(head_frame, text='Part 1: ', font=('bold', 30), text_color='#61892F')
        sn1_lable.pack(fill=ctk.X, side=ctk.LEFT, expand=True)
        sn1_text = ctk.CTkTextbox(head_frame, height=50, border_color='green',font=('bold', 15), border_width=1, corner_radius=0)
        sn1_text.pack(fill=ctk.X, expand=True, side=ctk.LEFT, padx=10, pady=15)

        sn2_lable = ctk.CTkLabel(head_frame, text='Part 2: ', font=('bold', 30), text_color='#61892F')
        sn2_lable.pack(fill=ctk.X, side=ctk.LEFT, expand=True)
        sn2_text = ctk.CTkTextbox(head_frame, height=50, border_color='green',font=('bold', 15), border_width=1, corner_radius=0)
        sn2_text.pack(fill=ctk.X, expand=True, side=ctk.LEFT, padx=10, pady=15)

        sn3_lable = ctk.CTkLabel(head_frame, text='Part 3: ', font=('bold', 30), text_color='#61892F')
        sn3_lable.pack(fill=ctk.X, side=ctk.LEFT, expand=True)
        sn3_text = ctk.CTkTextbox(head_frame, height=50, border_color='green',font=('bold', 15), border_width=1, corner_radius=0)
        sn3_text.pack(fill=ctk.X, expand=True, side=ctk.LEFT, padx=10, pady=15)
        head_frame.pack(fill=ctk.X)
        
        log_frame_1 = ctk.CTkFrame(my_home)
        self.log_status_label_1 = ctk.CTkLabel(log_frame_1, text=f'Log 1', font=('bold', 30), text_color='red', corner_radius=20)
        self.log_status_label_1.pack(pady=10, padx=10, side=ctk.TOP)
        self.pcb_log_1 = ctk.CTkTextbox(log_frame_1, height=250, width=400, border_color='green', border_width=1, text_color='green', font=('bold', 15)) #, state=ctk.DISABLED
        self.pcb_log_1.pack(pady=10, padx=10)
        self.select_file = ctk.CTkButton(log_frame_1, text='Select Files', corner_radius=20, font=('bold', 20), border_color='black',
                            height=50, hover_color='#61892F', border_width=1, command= lambda: self.file_selection_window(self.pcb_log_1,'file_list_1.txt'))
        self.select_file.pack(pady=10, padx=10)
        self.pcb_status_1 = ctk.CTkLabel(log_frame_1, text='Status', fg_color='gray',corner_radius=10,
                                         width=80, height=80, font=('Helvetica', 25, 'bold'))
        self.pcb_status_1.pack(pady=10, padx=10)
        log_frame_1.pack(fill=ctk.BOTH, expand=True, side=ctk.LEFT)

        log_frame_2 = ctk.CTkFrame(my_home)
        self.log_status_label_2 = ctk.CTkLabel(log_frame_2, text=f'Log 2', font=('bold', 30), text_color='red', corner_radius=20)
        self.log_status_label_2.pack(pady=10, padx=10, side=ctk.TOP)
        self.pcb_log_2 = ctk.CTkTextbox(log_frame_2, height=250, width=400, border_color='green', border_width=1, text_color='green', font=('bold', 15)) #, state=ctk.DISABLED
        self.pcb_log_2.pack(pady=10, padx=10)
        self.select_file = ctk.CTkButton(log_frame_2, text='Select Files', corner_radius=20, font=('bold', 20), border_color='black',
                            height=50, hover_color='#61892F', border_width=1, command= lambda: self.file_selection_window(self.pcb_log_2,'file_list_2.txt'))
        self.select_file.pack(pady=10, padx=10)
        self.pcb_status_2 = ctk.CTkLabel(log_frame_2, text='Status', fg_color='gray',corner_radius=10,
                                         width=80, height=80, font=('Helvetica', 25, 'bold'))
        self.pcb_status_2.pack(pady=10, padx=10)
        log_frame_2.pack(fill=ctk.BOTH, expand=True, side=ctk.LEFT)

        log_frame_3 = ctk.CTkFrame(my_home)
        self.log_status_label_3 = ctk.CTkLabel(log_frame_3, text=f'Log 3', font=('bold', 30), text_color='red', corner_radius=20)
        self.log_status_label_3.pack(pady=10, padx=10, side=ctk.TOP)
        self.pcb_log_3 = ctk.CTkTextbox(log_frame_3, height=250, width=400, border_color='green', border_width=1, text_color='green', font=('bold', 15)) #, state=ctk.DISABLED
        self.pcb_log_3.pack(pady=10, padx=10)
        self.select_file = ctk.CTkButton(log_frame_3, text='Select Files', corner_radius=20, font=('bold', 20), border_color='black',
                            height=50, hover_color='#61892F', border_width=1, command= lambda: self.file_selection_window(self.pcb_log_3,'file_list_3.txt'))
        self.select_file.pack(pady=10, padx=10)
        self.pcb_status_3 = ctk.CTkLabel(log_frame_3, text='Status', fg_color='gray',corner_radius=10,
                                         width=80, height=80, font=('Helvetica', 25, 'bold'))
        self.pcb_status_3.pack(pady=10, padx=10)
        log_frame_3.pack(fill=ctk.BOTH, expand=True, side=ctk.LEFT)

        self.flash_button = ctk.CTkButton(log_frame_2, text='Flash', corner_radius=20, font=('bold', 20), border_color='black',
                            height=50, hover_color='orange', border_width=1, command=self.File_For_Flash)
        self.flash_button.pack(pady=5, padx=5, side=ctk.LEFT)
        self.reset_button = ctk.CTkButton(log_frame_2, text='Reset', corner_radius=20, font=('bold', 20), border_color='black',
                            height=50, hover_color='orange', border_width=1, command=self.reset_screen)
        self.reset_button.pack(pady=5, padx=5, side=ctk.RIGHT)

        # Initial log messages
        msg = "Application started. \n"
        log(self.pcb_log_1, msg)
        log(self.pcb_log_2, msg)
        log(self.pcb_log_3, msg)

        self.upload_file(self.pcb_log_1, file_list_1, 'file_list_1.txt')
        self.upload_file(self.pcb_log_2, file_list_1, 'file_list_2.txt')
        self.upload_file(self.pcb_log_3, file_list_2, 'file_list_3.txt')

        my_home.pack(fill=ctk.BOTH, expand=True)

# ********************************* Setting Page ********************************* #
    def setting_page(self):
        if check_password() == True:
            my_setting = ctk.CTkFrame(self.main_frame)

            plc = PLC_reg()

            def save_config(new_host, new_port):
                with open("config.txt", "w") as f:
                    f.write(f"{new_host},{new_port}")

            def new_config():
                confirm = messagebox.askyesno(title='Save', message='Do you want to save this ?')
                try:
                    if confirm:
                        plc.host = n_host.get()
                        plc.port = n_port.get()
                        print(plc.host)
                        print(plc.port)
                        save_config(plc.host, plc.port)
                        my_log(f"New IP and Port is now Updated.")
                except Exception as e:
                    my_log(f'Error: {e}')
            
            PLC_conf_frame = ctk.CTkFrame(my_setting)
            PLC_conf_frame.pack(fill=ctk.BOTH, expand=True)

            default_add = ctk.CTkLabel(my_setting, text=f"PLC Default IP: {plc.host}    Port: {plc.port}", font=('Arial', 15), fg_color='black')
            default_add.pack(padx=20, pady=10)

            host_label = ctk.CTkLabel(PLC_conf_frame, text="New Host")
            host_label.pack(padx=20, pady=10)

            n_host = ctk.CTkEntry(PLC_conf_frame)
            n_host.pack(pady=5, padx=5)

            port_label = ctk.CTkLabel(PLC_conf_frame, text="New Port")
            port_label.pack(padx=20, pady=10)

            n_port = ctk.CTkEntry(PLC_conf_frame)
            n_port.pack(padx=5, pady=5)

            save_button = ctk.CTkButton(PLC_conf_frame, text="Save", command=new_config)
            save_button.pack(pady=10)

            my_setting.pack(fill=ctk.BOTH, expand=True)

# ********************************* Data Page ********************************* #
    def Data_page(self):
        my_data = ctk.CTkFrame(self.main_frame)

        # data_head_frame = tb.Frame(my_data, bootstyle="info")
        # data_head_frame.pack(side=tb.TOP, fill=tb.X)
        # # data_head_frame.pack_propagate(False)
        # data_head_frame.configure(height=50)

        data_head_frame = ctk.CTkFrame(my_data, fg_color='#bbed55', corner_radius=0)
        data_head_frame.pack(side=ctk.TOP, fill=ctk.X)
        data_head_frame.pack_propagate(False)
        data_head_frame.configure(height=50)

        start_date_label = ctk.CTkLabel(data_head_frame, text='Select Start Date: ', text_color='orange',
                                        fg_color='blue', corner_radius=5, font=('bold', 15), bg_color='#158aff')
        start_date_label.pack(pady=10, padx=10, side=tb.LEFT)
        start_date = tb.DateEntry(data_head_frame, firstweekday=0, bootstyle='primery')
        start_date.pack(pady=10, padx=10, side=tb.LEFT)
        starting_date = start_date.entry.get()
        print(starting_date)

        end_date_label = ctk.CTkLabel(data_head_frame, text='Select Last Date: ', text_color='orange',
                                        fg_color='blue', corner_radius=5, font=('bold', 15), bg_color='#158aff')
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
        self.clock_label.configure(fg_color='black', text_color='green')
        self.Current_Shift.configure(fg_color='black', text_color='green')

# ********************************* Real Time Clock ********************************* #
    def my_clock(self):
        current_time = datetime.datetime.now().strftime('%H:%M:%S %p')
        current_date = datetime.datetime.today().strftime('%d-%M-%Y')
        # self.Count_lable.configure(text=self.count)
        # self.count += 1
        # print(current_date)
        self.clock_label.configure(text=f'Date:{current_date}\tTime:{current_time}')
        self.Current_Shift.configure(text=f'Shift: {self.Current_Sift}')
        T1 = "08:00:00"
        T2 = "14:00:00"
        T3 = "20:00:00"
        self.clock_label.after(1000, self.my_clock)
        if (current_time > T1) and (current_time < T2):
            # print("Shift A")
            self.Current_Sift = 'A'
        elif (current_time > T2) and (current_time < T3):
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

    def reset_screen(self):
        self.pcb_status_1.configure(text='Status', text_color='gray',font=('Helvetica', 25, 'bold'))
        self.pcb_status_2.configure(text='Status', text_color='gray',font=('Helvetica', 25, 'bold'))
        self.pcb_status_3.configure(text='Status', text_color='gray',font=('Helvetica', 25, 'bold'))
        
    def File_For_Flash(self):
        msg = "Flashing... \n"
        log(self.pcb_log_1, msg)
        log(self.pcb_log_2, msg)
        log(self.pcb_log_3, msg)

        msg = "Flashing Done. \n"
        log(self.pcb_log_1, msg)
        log(self.pcb_log_2, msg)
        log(self.pcb_log_3, msg)

        self.pcb_status_1.configure(text='OK', text_color='green',font=('Helvetica', 40, 'bold'))
        self.pcb_status_2.configure(text='OK', text_color='green',font=('Helvetica', 40, 'bold'))
        self.pcb_status_3.configure(text='NG', text_color='red',font=('Helvetica', 40, 'bold'))


# ********************************* Change PLC Config ********************************* #
    def change_config(self):
        def new_config():
            confirm = messagebox.askyesno(title='Save', message='Do you want to save this ?')
            if confirm:
                plc.host = n_host.get()
                plc.port = n_port.get()
                print(plc.host)
                print(plc.port)
                popup.destroy()
            else:
                popup.destroy()
        # Example usage:
        plc = PLC_reg()
        print(plc.host)  # Output: 192.168.250.1
        print(plc.port)  # Output: 1200

        popup = ctk.CTkToplevel(root)
        popup.title("Popup Window")

        host_label = ctk.CTkLabel(popup, text="New Host")
        host_label.pack(padx=20, pady=10)

        n_host = ctk.CTkEntry(popup)
        n_host.pack(pady=5, padx=5)

        port_label = ctk.CTkLabel(popup, text="New Port")
        port_label.pack(padx=20, pady=10)

        n_port = ctk.CTkEntry(popup)
        n_port.pack(padx=5, pady=5)

        save_button = ctk.CTkButton(popup, text="Save", command=new_config)
        save_button.pack(pady=10)
    
    def read_config(self):
        try:
            with open("config.txt", "r") as f:
                data = f.read().split(",")
                return data[0], data[1]
        except FileNotFoundError:
            return None, None
        

if __name__ == '__main__':
    root = ctk.CTk()
    app = FlashingApp(root)
    # pass_check = check_password()
    # if pass_check:
    #     app = FlashingApp(root)
    # else:
    #     root.destroy()
    root.mainloop()