# import tkinter as tk
# import customtkinter as ctk
# from tkinter import Text, Label, messagebox, simpledialog, Entry, filedialog
# from hashlib import sha256  # For password hashing
# import logging as my_log
# from datetime import datetime
# import os
# # from Methods.MyFunctions import min_win_size, log


# def log(log_text, message):
#     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     log_message = f"{current_time} - {message}\n"
#     log_text.config(state=tk.NORMAL)
#     log_text.insert(tk.END, log_message)
#     log_text.config(state=tk.DISABLED)
#     log_text.see(tk.END)
# # from pymodbus.client import ModbusTcpClient
# # from pymodbus import exceptions as ConnectionException

# # Const Variable declaration
# Setting_Password = '1234'
# file_path = ''
# Host = ''
# Port = ''
# file_cache = []

# my_log.basicConfig(filename='Log.txt', level=my_log.INFO, format='%(asctime)s - %(message)s')

# class MyApp:
#     def __init__(self, window):
#         self.window = window
#         self.window.title("Dashboard")
#         # min_win_size(self.window, 800, 500)
#         self.window.geometry('500x500')

#         # Window open in full screen default
#         self.window.attributes('-fullscreen', True)  # For Windows
#         self.window.attributes('-fullscreen', True)  # For Linux

#         # Header frame and labels for log_status
#         self.header_frame = tk.Frame()
#         self.header_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        
#         # Initialize Labels and buttons for different pages
#         self.log_status_label_1 = None
#         self.last_path = None
#         self.path_log_text = None
#         # self.upload_button = None
#         self.change_path_button = None
#         self.host_label = None
#         self.host_entry = None
#         self.port_label = None
#         self.port_entry = None
#         self.connect_button = None
#         self.delete_file_button = None
#         self.file_listbox = None
#         self.client = None
#         self.status_label = None

#         # Initialize the home page
#         self.home_page()

#         # Buttons for different pages
#         self.home_button = tk.Button(self.header_frame, text='Home', command=self.home_page, font=('Helvetica', 15),
#                                      highlightbackground='green', activeforeground='red', activebackground='skyblue',
#                                      width=18, height=3)
#         self.home_button.grid(column=1, row=1, padx=(10, 0))  # Add right padding

#         self.setting_button = tk.Button(self.header_frame, text='Settings', command=self.Setting_page,
#                                         font=('Helvetica', 15), highlightbackground='green', activeforeground='red',
#                                         activebackground='skyblue', width=18, height=3)
#         self.setting_button.grid(column=2, row=1, padx=(10, 0))  # Add right padding

#         self.path_button = tk.Button(self.header_frame, text='Paths', command=self.paths_page, font=('Helvetica', 15),
#                                      highlightbackground='green', activeforeground='red', activebackground='skyblue',
#                                      width=18, height=3)
#         self.path_button.grid(column=3, row=1, padx=(10, 0))  # Add right padding

#         self.exit_button = tk.Button(self.header_frame, text='Exit', command=self.Exit_App, font=('Helvetica', 15),
#                                      highlightbackground='green', activeforeground='red', activebackground='skyblue',
#                                      width=18, height=3)
#         self.exit_button.grid(column=4, row=1, padx=(10, 0))  # Add right padding

# # ******************************** Home Page Start ******************************** #
#     def home_page(self):
#         # Hide other pages, set title, and create widgets for the home page
#         self.hide_page('Path')
#         self.hide_page('Setting')
#         self.window.title('Home')

#         home_frame = tk.Frame(self.window)
#         home_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
#         for i in range(3):
#             # Labels for log statuses
#             log_status_label = tk.Label(home_frame, text=f'Log Status {i + 1}', font=('Helvetica', 30), foreground='blue')
#             log_status_label.grid(column=i, row=1)

#             # Text widgets for logs
#             pcb_log = self.create_log_widget(home_frame, row=2, column=i)

#             # Buttons for actions
#             Select_File = tk.Button(home_frame, text='Select Files', font=('Helvetica', 8), activeforeground='green',
#                                      activebackground='orange', width=18, height=3, command=self.File_For_Flash)
#             Select_File.grid(row=3, column=i)

#             Flash_Button = tk.Button(home_frame, text='Program', font=('Helvetica', 8), activeforeground='green',
#                                      activebackground='orange', width=18, height=3, command=self.File_For_Flash)
#             Flash_Button.grid(row=4, column=i)

#             # Labels for process status
#             pcb_status = self.create_status_label(home_frame, text=f'Status_{i + 1}', row=5, column=i)

#             # Store the widgets in instance variables if needed
#             setattr(self, f'log_status_label_{i + 1}', log_status_label)
#             setattr(self, f'PCB_log_{i + 1}', pcb_log)
#             setattr(self, f'Select_File_{i + 1}', Select_File)
#             setattr(self, f'Flash_Button_{i + 1}', Flash_Button)
#             setattr(self, f'PCB_Status_{i + 1}', pcb_status)

#         # Initial log messages
#         msg = "Application started. \n"
#         log(self.PCB_log_1, msg)
#         log(self.PCB_log_2, msg)
#         log(self.PCB_log_3, msg)

#     def File_For_Flash(self):
#         self.upload_file()
# # ******************************** Setting Page Start ******************************** #
#     def Setting_page(self):
#         # Check password and show setting page or access denied message
#         if self.check_password():
#             self.hide_page('Home')
#             self.hide_page('Path')
#             self.window.title('Setting')

#             setting_frame = tk.Frame(self.window)
#             setting_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

#             # Label and entry widgets for PLC communication settings
#             self.log_status_label_1 = tk.Label(setting_frame, text='Communicate with PLC', font=('Helvetica', 35), foreground='blue')
#             self.log_status_label_1.grid(column=1, row=2)

#             self.host_label = Label(setting_frame, text='PLC Host:', width=40, font=('Helvetica', 20))
#             self.host_label.grid(row=3, column=1, padx=10, pady=10)
#             self.host_entry = Entry(setting_frame, width=70)
#             self.host_entry.grid(row=4, column=1, padx=10, pady=10)

#             self.port_label = Label(setting_frame, text='PLC Port:', width=40, font=('Helvetica', 20))
#             self.port_label.grid(row=5, column=1, padx=10, pady=10)
#             self.port_entry = Entry(setting_frame, width=70)
#             self.port_entry.grid(row=6, column=1, padx=10, pady=10)

#             # Button to connect to PLC
#             self.connect_button = tk.Button(setting_frame, text="Connect", font=('Helvetica', 8), activeforeground='green',
#                                      activebackground='orange', width=18, height=3, command=self.connect_to_plc)
#             self.connect_button.grid(row=7, column=1, columnspan=2, pady=10)

#             self.processing_label = Label(setting_frame, text="", font=('Helvetica', 15))
#             self.processing_label.grid(row=8, column=1, columnspan=2, pady=10)

#             # Create the status_label here
#             self.status_label = Label(setting_frame, text="", font=('Helvetica', 15))
#             self.status_label.grid(row=9, column=1, columnspan=2, pady=10)

#         else:
#             messagebox.showinfo("Access Denied", "Incorrect Password")

# # ******************************** Path Page Start ******************************** #
#     def paths_page(self):
#         # Hide other pages, set title, and create widgets for the paths page
#         self.hide_page('Home')
#         self.hide_page('Setting')
#         self.window.title('Files Path')

#         path_frame = tk.Frame(self.window)
#         path_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

#         self.test_label = Label(path_frame, text='Change Path', font=('Helvetica', 35), foreground='blue')
#         self.test_label.grid(row=1, column=0, columnspan=3)

#         # Text widget for displaying logs
#         self.path_log_text = self.create_log_widget(path_frame, row=2, column=0)

#         # # Button to trigger file upload
#         # self.upload_button = tk.Button(path_frame, text="Upload File", command=self.upload_file)
#         # self.upload_button.grid(row=2, column=0, padx=10, pady=10)

#         # Button to change the path
#         self.change_path_button = tk.Button(path_frame, text="Change Path", command=self.change_path)
#         self.change_path_button.grid(row=3, column=0, padx=10, pady=10)

#         # Listbox for displaying uploaded files
#         self.file_listbox = tk.Listbox(path_frame, height=10, width=50, selectmode=tk.SINGLE)
#         self.file_listbox.grid(row=2, column=1, padx=10, pady=10)

#         # Button to select a file for deletion
#         # self.select_file_button = tk.Button(path_frame, text="Select File", command=self.select_file_for_deletion)
#         # self.select_file_button.grid(row=2, column=1, padx=10, pady=10)

#         # Button to delete the selected file
#         self.delete_file_button = tk.Button(path_frame, text="Delete File", command=self.delete_selected_file)
#         self.delete_file_button.grid(row=3, column=1, padx=10, pady=10)
#         # print(f'File List Size: {len(file_cache)}')

#     def select_file_for_deletion(self):
#         # Get the selected index from the listbox
#         selected_index = self.file_listbox.curselection()

#         # Check if any item is selected
#         if selected_index:
#             # Set the selected index as the current selection
#             self.file_listbox.selection_set(selected_index)

#     def delete_selected_file(self):
#         # Get the selected index from the listbox
#         selected_index = self.file_listbox.curselection()

#         # Check if any item is selected
#         if selected_index:
#             # Get the selected file path
#             selected_file = self.file_listbox.get(selected_index)

#             # Delete the file from the cache and update the listbox
#             file_cache.remove(selected_file)
#             self.update_file_listbox()

#     def update_file_listbox(self):
#         # Clear the existing items in the listbox
#         self.file_listbox.delete(0, tk.END)

#         # Add the updated file list to the listbox
#         for file_content in file_cache:
#             self.file_listbox.insert(tk.END, file_content)
# # ********************* File Upload Logic ********************************** #
#     def upload_file(self):
#         try:
#             # Read the last path from Path.txt
#             self.last_path = self.read_last_path()

#             # If last_path is not None and exists, use it as the initial directory
#             initial_dir = self.last_path if self.last_path and os.path.exists(self.last_path) else "/"

#             # Ask the user to select a file
#             file_paths = filedialog.askopenfilenames(title='Upload File', initialdir=initial_dir)

#             if file_paths:
#                 for file_path in file_paths:
#                     if os.path.exists(file_path):
#                         with open(file_path, 'r') as my_file:
#                             file_content = my_file.read()
#                     file_cache.append(( os.path.basename(file_path), file_content ))

#                 print(f"File Uploaded Successfully From {file_path}")
#                 log_message = f"File Uploaded Successfully From {file_path} \n"
#                 log(self.path_log_text, log_message)

#                 # Update the last changed path in the config file
#                 self.write_last_path(self.last_path)

#                 # Update the listbox after uploading files
#                 self.update_file_listbox()

#             else:
#                 raise ValueError("No File Selected.")

#         except Exception as e:
#             log_message = f"Error Uploading File: {str(e)} \n"
#             my_log.info(log_message)
#             log(self.path_log_text, log_message)
#             print(log_message)
        
#         my_log.info(log_message)

# # ********************* Change Path Logic ********************************** #
#     def change_path(self):
#         # Ask the user to select a new path
#         new_path = filedialog.askdirectory(title='Change Path')

#         if new_path:
#             print(f"Path Changed To: {new_path}")
#             log_message = f"Path Changed To: {new_path} \n"
#             log(self.path_log_text, log_message)

#             # Update the last changed path
#             self.last_path = new_path

#             # Update the last changed path in the config file
#             self.write_last_path(new_path)

#     def read_last_path(self):
#         try:
#             with open("Path.txt", 'r') as file:
#                 return file.read().strip()
#         except FileNotFoundError:
#             return None

#     def write_last_path(self, path):
#         with open("Path.txt", 'w') as file:
#             file.write(path)

# # ********************* PLC Communication Logic ****************************** #
#     def connect_to_plc(self):
#         print('PLC Connection Button was clicked!')

#         # if self.status_label is not None:
#         #     self.status_label.config(text="")

#         # # Display processing status
#         # self.processing_label.config(text="Connecting...", fg="orange")
#         # self.window.update_idletasks()  # Force update to show the label immediately

#         # # Logic for connecting to PLC (Not Tested)
#         # host = self.host_entry.get()
#         # port = int(self.port_entry.get())

#         # try:
#         #     # Close the existing connection if any
#         #     if self.client:
#         #         self.client.close()

#         #     # Attempt to establish a new connection
#         #     self.client = ModbusTcpClient(host, port)
#         #     connection_status = self.client.connect()

#         #     if connection_status:
#         #         self.status_label.config(text="Connected to PLC", fg="green")
#         #         # Now you can perform read/write operations with the PLC using self.client
#         #         # For example:
#         #         # result = self.client.read_coils(0, 1)
#         #         # print(result.bits[0])
#         #     else:
#         #         self.status_label.config(text="Connection failed", fg="red")

#         # except ConnectionException as e:
#         #     self.status_label.config(text=f"Connection Error: {str(e)}", fg="red")
#         #     messagebox.showerror("Connection Error", f"Failed to connect to PLC: {str(e)}")
#         # except Exception as e:
#         #     self.status_label.config(text=f"Error: {str(e)}", fg="red")
#         #     messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
#         # finally:
#         #     self.window.after(2000, self.processing_label.config(text=""))

# # ********************* Hide Pages on Current Page Logic ********************* #
#     def hide_page(self, page_name):
#         # Hide widgets based on the current page
#         if page_name == 'Home':
#             widgets = [
#                 self.PCB_log_1, self.PCB_log_2, self.PCB_log_3,
#                 self.PCB_Status_1, self.PCB_Status_2, self.PCB_Status_3,
#                 self.log_status_label_1, self.log_status_label_2, self.log_status_label_3,
#                 self.Select_File_1, self.Select_File_2, self.Select_File_3,
#                 self.Flash_Button_1, self.Flash_Button_2, self.Flash_Button_3
#             ]
#             for widget in widgets:
#                 widget.grid_remove()
        
#         elif page_name == 'Setting':
#             widgets = [
#                 self.log_status_label_1,
#                 self.host_label, self.host_entry,
#                 self.port_label, self.port_entry,
#                 self.connect_button
#             ]
#             for widget in widgets:
#                 if widget is not None:
#                     widget.grid_remove()
#                 else:
#                     pass
#         elif page_name == 'Path':
#             widgets = [
#                 self.path_log_text,
#                 # self.upload_button,
#                 self.change_path_button,
#                 self.delete_file_button,
#                 self.file_listbox
#             ]
#             for widget in widgets:
#                 if widget is not None:
#                     widget.grid_remove()
#                 else:
#                     pass

# # ********************* Check Password Logic ********************************** #
#     def check_password(self):
#         # Ask for password using a dialog
#         password = simpledialog.askstring("Password", "Enter Password:", show='*')

#         # Check if the entered password is correct
#         hashed_password = sha256(password.encode()).hexdigest()
#         CORRECT_PASSWORD = sha256(Setting_Password.encode()).hexdigest()

#         return hashed_password == CORRECT_PASSWORD

# # ********************* Create Log & Status Logic ****************************** #
#     def create_log_widget(self, parent, row, column):
#         # Create and return a Text widget for logging
#         log_widget = Text(parent, height=20, width=54, state=tk.DISABLED)
#         log_widget.grid(row=row, column=column, padx=5, pady=5)
#         return log_widget

#     def create_status_label(self, parent, text, row, column):
#         # Create and return a Label widget for displaying status
#         status_label = Label(parent, text=text, bg='green', fg='white', width=30, height=5, font=('Helvetica', 12))
#         status_label.grid(row=row, column=column, padx=5, pady=5)
#         return status_label
    
#     # Add a method for exiting the application
#     def Exit_App(self):
#         print('Application Closed!')
#         self.window.destroy()


# def main():
#     window = tk.Tk()
#     app = MyApp(window)
#     window.mainloop()

# if __name__ == '__main__':
#     main()












# import tkinter as tk
# from tkinter import ttk

# root = tk.Tk()

# style = ttk.Style()

# style.layout('TNotebook.Tab', []) # turn off tabs

# count = 0

# def switch():
#     global count
#     if count % 2 == 0:
#         note.select(0)
#     else:
#         note.select(1)
#     count +=1

# check = tk.Button(root, text='click', command=switch)
# check.pack(padx=5,pady=5)

# note = ttk.Notebook(root)

# f1 = ttk.Frame(note)
# txt = tk.Text(f1, width=40, height=10)
# txt.insert('end', 'Page 0 : a text widget')
# txt.pack(expand=1, fill='both')
# note.add(f1)

# f2 = ttk.Frame(note)
# lbl = tk.Label(f2, text='Page 1 : a label')
# lbl.pack(expand=1, fill='both')
# note.add(f2)

# note.pack(expand=1, fill='both', padx=5, pady=5)

# def do_something():
#     note.select(1)
               
# root.after(3000, do_something)
# root.mainloop()







# ********************* For Singal Device ********************* #
# import pylink

# def get_flashing_status(hex_file_path):
#     # Initialize J-Link connection
#     jlink = pylink.JLink()

#     # Open J-Link connection
#     jlink.open()
    
#     # Connect to target device
#     jlink.connect('RX210', speed=1000)  # Specify the correct device name
    
#     # Erase target device
#     jlink.erase()

#     # Program target device with hex file
#     jlink.program(hex_file_path)

#     # Verify programmed memory
#     verify_result = jlink.verify(hex_file_path)

#     # Close J-Link connection
#     jlink.close()

#     return verify_result

# if __name__ == "__main__":
#     # Path to the HEX file to be flashed
#     hex_file_path = "example.hex"

#     try:
#         # Get flashing status
#         flashing_status = get_flashing_status(hex_file_path)
#         if flashing_status:
#             print("Flashing successful")
#         else:
#             print("Flashing failed")
#     except Exception as e:
#         print(f"Error: {e}")



# ********************* For Multiple Device ********************* #
# import pylink

# def get_flashing_status(hex_file_path, device_name, jlink_serial_numbers):
#     for serial_number in jlink_serial_numbers:
#         # Initialize J-Link connection
#         jlink = pylink.JLink(serial_no=serial_number)
        
#         # Open J-Link connection
#         jlink.open()
        
#         # Connect to target device
#         jlink.connect(device_name, speed=1000)
        
#         # Erase target device
#         jlink.erase()

#         # Program target device with hex file
#         jlink.program(hex_file_path)

#         # Verify programmed memory
#         verify_result = jlink.verify(hex_file_path)

#         # Close J-Link connection
#         jlink.close()

#         if not verify_result:
#             return False  # Return False if verification fails for any target
#     return True  # Return True if verification is successful for all targets

# if __name__ == "__main__":
#     # Path to the HEX file to be flashed
#     hex_file_path = "example.hex"

#     # Device name (R5F10BGFCLFB)
#     device_name = "RX210"  # Specify the correct device name
    
#     # Serial numbers of the J-Link debuggers connected to each IC
#     jlink_serial_numbers = ["12345678", "23456789", "34567890"]  # Replace with actual serial numbers

#     # Get flashing status
#     flashing_status = get_flashing_status(hex_file_path, device_name, jlink_serial_numbers)

#     if flashing_status:
#         print("Flashing successful for all ICs")
#     else:
#         print("Flashing failed for one or more ICs")


# import serial

# def send_command_to_arduino(command):
#     ser = serial.Serial('COM3', 9600) # Adjust COM port and baud rate as needed
#     ser.write(command.encode())
#     ser.close()

# send_command_to_arduino('1')









# ***************************** mrk3 2link ***************************** #
# import os
# import subprocess

# def flash_program(opt_command, hex_file_path):
#     # Check if the file exists at the specified path
#     if not os.path.exists(hex_file_path):
#         return False, f"Error: File '{hex_file_path}' not found."

#     else:
#         # Construct the command to download the program
#         print('File Path found!')
#         command = f'download EROM,"{hex_file_path}"'

#         try:
#             My_tool = "C:\\Users\\anura\\Downloads\\MRK3 2_Link\\MRK3Link_EXE_V1.92\\MRK3Link.exe"

#             if not os.path.exists(My_tool):
#                 return False, f"Error: Tool '{My_tool}' not found."
            
#             start_tool = subprocess.run([My_tool], capture_output=True, text=True, timeout=10, input=opt_command+'\n', check=True)
            
#             print('Tool also found.')
#             # Execute the command using subprocess
#             result = subprocess.run([My_tool, command], capture_output=True, text=True, timeout=10)  # Increased timeout to 120 seconds

#             print("Command Output:", result.stdout)
#             print("Command Error:", result.stderr)
#             print("Return Code:", result.returncode)
            
#             # Check if the process executed successfully
#             if result.returncode == 0:
#                 # Check if the output contains the success message
#                 if 'Download finished' in result.stdout:
#                     return True, "Program flashed successfully."
#                 else:
#                     return False, "Failed to flash program."
#             else:
#                 return False, "Error occurred while flashing program."

#         except subprocess.TimeoutExpired:
#             return False, "Timeout: Command execution took longer than expected."
#         except Exception as e:
#             return False, f"Error: {str(e)}"

# # Example usage
# hex_file_path = "C:/Users/anura/OneDrive/Documents/sketch_mar12a.ino.hex"

# # Check if the file exists before attempting to flash it
# opt = '0'
# if os.path.exists(hex_file_path):
#     success, message = flash_program(opt,hex_file_path)
#     print(message)
# else:
#     print(f"Error: File '{hex_file_path}' not found.")



import tkinter as tk
from PIL import Image, ImageTk

# Create main window
root = tk.Tk()

# Set window title
root.title("Image Viewer")

head_frame = tk.Frame(root)
head_frame.pack(side=tk.TOP, fill=tk.X)
head_frame.pack_propagate(False)
head_frame.configure(height=60)

# Load image
image_path = "Icons\sandhar_logo.png"  # Replace "path_to_image.jpg" with the path to your image file
image = Image.open(image_path)
# Resize image
new_width = 100  # Set the new width here
new_height = 80  # Set the new height here
resized_image = image.resize((new_width, new_height), 5)

# Convert resized image to PhotoImage
photo = ImageTk.PhotoImage(resized_image)

# Create a label to display the image
image_label = tk.Label(head_frame, image=photo)
image_label.pack()

# Run the tkinter event loop
root.mainloop()





# import subprocess
# import os
# import re

# def run_MRK3_2Link():
#     batch_file_path = "MRK3.bat"
#     result = subprocess.run([batch_file_path], capture_output=True, text=True, shell=True)
#     if result.returncode != 0:
#         if 'Error' in result.stdout:
#             try:
#                 eror = re.search(r"Error:\s*(\w+ \w+ \w+ \w+ \w+)", result.stdout).group(1)
#                 eror_1 = re.search(r"Error:\s*(\w+ \w+ \w+ \w+ \w+ \w+ \w+ \w+ \w+)", result.stdout).group(1)
#                 return f"Error: {eror}\nError: {eror_1}"
#             except Exception as e:
#                 return f"Error: {e}"
#     else:
#         if "Download finished" in result.stdout:
#             return "Operation was successful!"
#         else:
#             return ("Unexpected output:", result.stdout)
# message = run_MRK3_2Link()
# print(message)

    # try:
    #     path = "C:\\Users\\anura\\Downloads\\MRK3 2_Link\\MRK3Link_EXE_V1.92\\MRK3Link.exe"
    #     cmd = ["--usb", "0"]
    #     cmd_1 = 'download EROM,"C:\\Users\\anura\\OneDrive\\Documents\\sketch_mar12a.ino.hex"'
    #     if not os.path.exists(path):
    #         print('Path not found.')
    #         return False, 'Path not found.'

    #     # Open tool
    #     subprocess.run([path] + cmd + [cmd_1], shell=False)
    #     return True, "Tool opened successfully."
    # except Exception as e:
    #     return False, f"Error: {str(e)}"

# Example usage
# success, message = open_command_prompt()
# print(message)



# import subprocess
# def open_mrk3link_auto_select(selection):
#     path = "C:\\Users\\anura\\Downloads\\MRK3 2_Link\\MRK3Link_EXE_V1.92\\MRK3Link.exe"
#     try:
#         # Start the MRK3Link process
#         process = subprocess.Popen([path], stdin=subprocess.PIPE, text=True)

#         # Send the selection to the MRK3Link process
#         process.communicate(input=str(selection))

#         return True, "MRK3Link opened with automatic selection."
#     except Exception as e:
#         return False, f"Error: {str(e)}"

# # Example usage: Automatically select option 1
# selection = 0
# success, message = open_mrk3link_auto_select(selection)
# print(message)



# ***************************** Send Data to Arduino ***************************** #
# import serial
# import time

# # Define the serial port and baud rate
# serial_port = 'COM6'  # Adjust this to the correct port for your Arduino
# baud_rate = 9600

# # Initialize serial communication
# ser = serial.Serial(serial_port, baud_rate)
# time.sleep(2)  # Allow time for Arduino to reset after connection

# # Function to send commands for controlling LEDs
# def send_command(command):
#     print(f"Sending command: {command}")
#     ser.write(command.encode())
#     time.sleep(1)  # Wait for Arduino to process command

# # Send commands to turn LED1 on and off
# while True:
#     new_com_led1 = input("Enter command for LED1 (1 for ON, 0 for OFF): ")
#     if new_com_led1 in ['0', '1']:
#         send_command(new_com_led1)
#     else:
#         print("Invalid command. Please enter '0' or '1'.")

#     new_com_led2 = input("Enter command for LED2 (1 for ON, 0 for OFF): ")
#     if new_com_led2 in ['0', '1']:
#         send_command(new_com_led2)
#     else:
#         print("Invalid command. Please enter '0' or '1'.")

#     if new_com_led1 == '2' or new_com_led2 == '2':
#         break

# # Close serial connection
# ser.close()








# ***************************** Renesas with Batch file ***************************** #
# import subprocess

# def run_batch_script(script_path):
#     try:
#         # Run the batch script and capture output
#         result = subprocess.run(script_path, shell=True, capture_output=True, text=True)
        
#         # Check if the script ran successfully
#         if result.returncode == 0:
#             # Return the output of the script
#             return True, result.stdout
#         else:
#             # Return False and the error message if the script failed
#             return False, result.stderr
#     except Exception as e:
#         # Return False and the exception message if an error occurred
#         return False, str(e)

# # Example usage
# script_path = "testing.bat"
# success, output = run_batch_script(script_path)
# if success:
#     print("Script output:", output)
# else:
#     print("Error:", output)


# ***** Testing_2 *****
# import subprocess
# import serial
# import time

# def read_serial_data(serial_port, baud_rate):
#     # Initialize serial communication
#     ser = serial.Serial(serial_port, baud_rate)
#     time.sleep(2)  # Allow time for Arduino to reset after connection
#     if ser.in_waiting > 0:
#         # Read data from Arduino
#         data = ser.readline().decode().strip()
#         return data

# # Define the path to the batch file and the hex file
# batch_file = "testing.bat"
# hex_file = "C:\\Users\\anura\\OneDrive\\Documents\\test.hex"

# while True:
#     serial_data = read_serial_data('COM6', 9600)

#     if serial_data == "1":  # Compare with string "1"
#         # Run the batch file with the hex file path as an argument
#         result = subprocess.run([batch_file, hex_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

#         # Print the output of the batch file
#         print("Standard Output:", result.stdout)

#         # Check the error code
#         if result.returncode != 0:
#             print("Error:", result.stderr)



# ***** Testing_3 *****
# import subprocess
# import tkinter as tk
# from tkinter import filedialog

# def run_batch_file():
#     batch_file_path = "testing.bat"
#     result = subprocess.run([batch_file_path, hex_file], capture_output=True, text=True, shell=True)
#     if result.returncode != 0:
#         print("Error:", result.stderr)
#     else:
#         if "Operation successful" in result.stdout:
#             print("Operation was successful!")
#         else:
#             print("Unexpected output:", result.stdout)
            
# def browse_file():
#     global hex_file
#     hex_file = filedialog.askopenfilename(filetypes=[("Hex Files", "*.hex")])

# # Create a Tkinter window
# window = tk.Tk()
# window.title("Run Batch File")

# # Add a button to browse for the hex file
# browse_button = tk.Button(window, text="Browse Hex File", command=browse_file)
# browse_button.pack(pady=10)

# # Add a button to run the batch file
# run_button = tk.Button(window, text="Run Batch File", command=run_batch_file)
# run_button.pack(pady=10)

# # Run the Tkinter event loop
# window.mainloop()






# ****************** Receive Data from Arduino ****************** #
# import serial
# import time

# # Define the serial port and baud rate
# serial_port = 'COM6'  # Adjust this to the correct port for your Arduino
# baud_rate = 9600

# # Initialize serial communication
# ser = serial.Serial(serial_port, baud_rate)
# time.sleep(2)  # Allow time for Arduino to reset after connection

# # Main loop to continuously receive and process commands from Arduino
# while True:
#     if ser.in_waiting > 0:
#         # Read data from Arduino
#         data = ser.readline().decode().strip()
        
#         # Process the received data (you can add your own logic here)
#         print("Received command from Arduino:", data)
        
#         # Example: If Arduino sends 'LED_ON', turn on an LED
#         if data == "LED_ON":
#             # Code to turn on LED
#             print("Turning LED on")
        
#         # Example: If Arduino sends 'LED_OFF', turn off an LED
#         elif data == "LED_OFF":
#             # Code to turn off LED
#             print("Turning LED off")
            
#         # Add more conditions as needed
        
#     # Add any other Python code here

# # Close serial connection when done
# ser.close()
