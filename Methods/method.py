import os
import customtkinter as ctk
import datetime
import serial
import subprocess
import time
import re

hex_file = "C:\\Users\\anura\\OneDrive\\Documents\\test.hex"

def read_serial_data(serial_port, baud_rate):
    # Initialize serial communication
    ser = serial.Serial(serial_port, baud_rate)
    ser.timeout = 0.1  # Set a timeout for read operations (adjust as needed)
    time.sleep(2)  # Allow time for Arduino to reset after connection
    # Read data from Arduino
    data = ser.readline().decode().strip()
    # Close serial connection
    ser.close()
    return data


def run_batch_file():
    batch_file_path = "testing.bat"
    result = subprocess.run([batch_file_path, hex_file], capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
    else:
        if "Operation successful" in result.stdout:
            print("Operation was successful!")
        else:
            print("Unexpected output:", result.stdout)

def run_MRK3_2Link():
    batch_file_path = "MRK3.bat"
    result = subprocess.run([batch_file_path], capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        if 'Error' in result.stdout:
            try:
                eror = re.search(r"Error:\s*(\w+ \w+ \w+ \w+ \w+)", result.stdout).group(1)
                eror_1 = re.search(r"Error:\s*(\w+ \w+ \w+ \w+ \w+ \w+ \w+ \w+ \w+)", result.stdout).group(1)
                return f"Error: {eror}\nError: {eror_1}"
            except Exception as e:
                return f"Error: {e}"
    else:
        if "Download finished" in result.stdout:
            return "Operation was successful!"
        else:
            return ("Unexpected output:", result.stdout)

def read_qr_code():
    try:
        # Open serial connection to the QR scanner
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust port and baud rate as needed

        data = ser.readline().strip().decode('utf-8')  # Read a line of data from the scanner
        if data:  # If data is not empty
            print("QR Code Scanned:", data)
    except serial.SerialException as e:
        print("Error:", e)

def upload_file(file_names, selected_files):
    try:
        last_path = read_last_path()
        initial_dir = last_path if last_path and os.path.exists(last_path) else "/"

        for file_name in file_names:
            file_path = os.path.join(initial_dir, file_name)
            if os.path.exists(file_path):
                selected_files.append(file_path)  # Append full file path instead of just the name
                log_message = f"File Uploaded Successfully From {file_path}\n"
                write_last_path(last_path)
            else:
                print(f"File '{file_name}' not found in the initial directory.")
    except Exception as e:
        log_message = f"Error Uploading File: {str(e)}\n"
        print(log_message)
    
    # Store selected files in separate files
    store_files(selected_files, "file_list_1.txt")
    store_files(selected_files, "file_list_2.txt")

def write_last_path(path):
    with open("Path.txt", 'w') as file:
        file.write(path)
    
def read_last_path():
    try:
        with open("Path.txt", 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def store_files(file_list, file_name):
    with open(file_name, 'w') as file:
        for item in file_list:
            file.write("%s\n" % item)

def log(log_text, message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{current_time} - {message}\n"
    log_text.configure(state=ctk.NORMAL)
    log_text.insert(ctk.END, log_message)
    log_text.configure(state=ctk.DISABLED)
    log_text.see(ctk.END)

def dashed_line(canvas, x1, y1, x2, y2, dash_length=2, color='black'):
    # Draw the top line
    canvas.create_line(x1, y1, x2, y1, dash=(dash_length, dash_length), fill=color)
    # Draw the bottom line
    canvas.create_line(x1, y2, x2, y2, dash=(dash_length, dash_length), fill=color)
    # Draw the left line
    canvas.create_line(x1, y1, x1, y2, dash=(dash_length, dash_length), fill=color)
    # Draw the right line
    canvas.create_line(x2, y1, x2, y2, dash=(dash_length, dash_length), fill=color)
# # Create a Canvas widget
# canvas = tk.Canvas(root, width=200, height=100)
# canvas.pack()
# # Draw the dashed rectangle on the canvas
# draw_dashed_rectangle(canvas, 10, 10, 190, 90, dash_length=4, color='blue')









# def upload_file(self, file_names, selected_files):
#         try:
#             last_path = self.read_last_path()
#             initial_dir = last_path if last_path and os.path.exists(last_path) else "/"

#             for file_name in file_names:
#                 file_path = os.path.join(initial_dir, file_name)
#                 if os.path.exists(file_path):
#                     selected_files.append(file_path)  # Append full file path instead of just the name
#                     log_message = f"File Uploaded Successfully From {file_path}\n"
#                     self.write_last_path(last_path)
#                 else:
#                     print(f"File '{file_name}' not found in the initial directory.")
#         except Exception as e:
#             log_message = f"Error Uploading File: {str(e)}\n"
#             print(log_message)
        
#         # Store selected files in separate files
#         self.store_files(selected_files, "file_list_1.txt")
#         self.store_files(selected_files, "file_list_2.txt")

#     def write_last_path(self, path):
#         with open("Path.txt", 'w') as file:
#             file.write(path)
        
#     def read_last_path(self):
#         try:
#             with open("Path.txt", 'r') as file:
#                 return file.read().strip()
#         except FileNotFoundError:
#             return None

#     def store_files(self, file_list, file_name):
#         with open(file_name, 'w') as file:
#             for item in file_list:
#                 file.write("%s\n" % item)
    













# ********************** J-Link Programmer ********************** #
# import os
# import subprocess
# import pylink

# def erase_target(jlink):
#     print("Erasing target device...")
#     jlink.erase()

# def verify_target(jlink, hex_file_path):
#     print("Verifying programmed memory...")
#     return jlink.verify(hex_file_path)

# def program_target(jlink, hex_file_path):
#     print("Programming target device...")
#     # Launch J-Link Commander process to program the target device
#     cmd = f"JLink.exe -device RX210 -if SWD -speed 1000 -autoconnect 1 -CommanderScript {hex_file_path}"
#     subprocess.run(cmd, shell=True)

# def get_flashing_status(hex_file_path, device_name, jlink_serial_numbers):
#     for serial_number in jlink_serial_numbers:
#         # Initialize J-Link connection
#         jlink = pylink.JLink(serial_no=serial_number)
        
#         # Open J-Link connection
#         jlink.open()
        
#         # Connect to target device
#         jlink.connect(device_name, speed=1000)  # Specify the correct device name
        
#         # Erase target device
#         erase_target(jlink)

#         # Program target device
#         program_target(jlink, hex_file_path)

#         # Verify programmed memory
#         verify_result = verify_target(jlink, hex_file_path)

#         # Close J-Link connection
#         jlink.close()

#         if not verify_result:
#             return False  # Return False if verification fails for any target
#     return True  # Return True if verification is successful for all targets

# if __name__ == "__main__":
#     # Path to the HEX file to be flashed
#     hex_file_path = "example.hex"

#     # Device name (R5F10BGFCLFB)
#     device_name = "RX210"  # Replace with the correct device name
    
#     # Serial numbers of the J-Link debuggers connected to each IC
#     jlink_serial_numbers = ["12345678", "23456789", "34567890"]  # Replace with actual serial numbers

#     # Get flashing status
#     flashing_status = get_flashing_status(hex_file_path, device_name, jlink_serial_numbers)

#     if flashing_status:
#         print("Flashing successful for all ICs")
#     else:
#         print("Flashing failed for one or more ICs")
