from ttkbootstrap.constants import *
import ttkbootstrap as tb
import customtkinter as ctk
from tkinter import messagebox

class PLC_reg:
    def __init__(self):
        self.load_config()

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value
        self.save_config()

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value
        self.save_config()

    def save_config(self):
        with open("config.txt", "w") as f:
            f.write(f"{self._host},{self._port}")

    def load_config(self):    
        try:
            with open("config.txt", "r") as f:
                data = f.read().split(",")
                self._host = data[0]
                self._port = data[1]
        except FileNotFoundError:
            # If config file doesn't exist, use default values
            self._host = '192.168.250.1'
            self._port = '1200'

def open_popup():
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


root = tb.Window(themename='superhero')

root.title('Testing')
root.geometry('500x500')

new_root = ctk.CTkFrame(root)
new_root.pack(padx=0, pady=10, fill=X, side=tb.TOP)

my_frm = tb.Frame(new_root, bootstyle="info")
my_frm.pack(padx=0, pady=10, fill=X, side=tb.TOP)

new_labl = ctk.CTkLabel(my_frm, text='new text',fg_color='red')
new_labl.pack(padx=10, pady=10, side=ctk.LEFT)

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)

optionmenu_var = ctk.StringVar(value="Station 1")  # set initial value
combobox = ctk.CTkOptionMenu(master=my_frm,
                                    values=["Station 1", "Station 2", "Station 3"],
                                    command=optionmenu_callback,
                                    width=150,
                                    variable=optionmenu_var)
combobox.pack(padx=10, pady=10, side=ctk.LEFT)

start_date = tb.DateEntry(my_frm, firstweekday=0, bootstyle='primery')
start_date.pack(pady=10, padx=10)

date = tb.DateEntry(root, bootstyle='danger', firstweekday=0)
date.pack(pady=10)
# print(date.entry.get())

meter = tb.Meter(root, bootstyle='danger', subtext='Tkinter Bootstrap',
                 interactive=True, metertype='full', stripethickness=5,
                 amountused=0, textright='%', amounttotal=24)
meter.pack(pady=10)

my_lable = tb.Label(text='Hello world', font=('arial', 25), style='danger, inverse')
my_lable.pack(pady=5)

my_button = ctk.CTkButton(root, text='Click', corner_radius=10)
my_button.pack(pady=5)

plc_config = ctk.CTkButton(root, text='Config', command=open_popup)
plc_config.pack(padx=5,pady=5)

new_plc_config = PLC_reg()
print(new_plc_config.host)
print(new_plc_config.port)

root.mainloop()







# import tkinter as tk
# import customtkinter
# from tkcalendar import Calendar

# class YourApp:
#     def __init__(self, root):
#         self.root = root
#         self.create_widgets()

#     def create_widgets(self):
#         my_data = tk.Frame(self.root)
#         my_data.pack(fill=tk.BOTH, expand=True)

#         data_head_frame = tk.Frame(my_data)
#         data_head_frame.pack(side=tk.TOP, fill=tk.X)
#         data_head_frame.pack_propagate(False)
#         data_head_frame.configure(height=50)

#         start_date_label = customtkinter.CTkLabel(data_head_frame, text='Select Start Date: ')
#         start_date_label.pack(pady=10, padx=10, side=tk.LEFT)

#         start_date_entry = customtkinter.CustomDateEntry(data_head_frame)
#         start_date_entry.pack(pady=10, padx=10, side=tk.LEFT)

# root = tk.Tk()
# app = YourApp(root)
# root.mainloop()





# Menubar
# from tkinter import *

# def donothing():
#    x = 0
 
# root = Tk()
# menubar = Menu(root)
# filemenu = Menu(menubar, tearoff=0)
# filemenu.add_command(label="New", command=donothing)
# filemenu.add_command(label="Open", command=donothing)
# filemenu.add_command(label="Save", command=donothing)
# filemenu.add_separator()
# filemenu.add_command(label="Exit", command=root.quit)
# menubar.add_cascade(label="File", menu=filemenu)

# helpmenu = Menu(menubar, tearoff=0)
# helpmenu.add_command(label="Help Index", command=donothing)
# helpmenu.add_command(label="About...", command=donothing)
# menubar.add_cascade(label="Help", menu=helpmenu)

# root.config(menu=menubar)
# root.mainloop()
















# import serial
# import time

# # Define the serial port and baud rate
# serial_port = 'COM6'  # Adjust this to the correct port for your Arduino
# baud_rate = 9600

# # Initialize serial communication
# ser = serial.Serial(serial_port, baud_rate)
# time.sleep(2)  # Allow time for Arduino to reset after connection

# # Send commands to turn LED on and off
# # commands = ['1', '0']  # '1' for turning LED on, '0' for turning LED off
# command = input(f"Enter Command: ")

# while True:
#     print(f"Sending command: {command}")
#     ser.write(command.encode())
#     time.sleep(1)  # Wait for Arduino to process command
#     command = input(f"Enter Command: ")
#     if command == '2':
#         break

# # Close serial connection
# ser.close()