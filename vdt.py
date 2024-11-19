#!/usr/bin/python3

import obd
import colorama
import logging
import tkinter as tk
from tkinter import messagebox
from colorama import Fore, Style

colorama.init(autoreset=True)

def print_banner():
    print(Fore.CYAN + """
      _____                _      ___       _   
     /__   \\_ __ __ _  ___| | __ /___\\_   _| |_ 
       / /\\/ '__/ _` |/ __| |/ ///  // | | | __|
      / /  | | | (_| | (__|   </ \\_//| |_| | |_ 
      \\/   |_|  \\__,_|\\___|_|\\_\\___/  \\__,_|\\__|                                           
      Vehicle Diagnostic Tool
    """)

def connect_to_vehicle():
    connection = obd.OBD()  # auto-connects to USB or RF port
    if connection.status() == obd.OBDStatus.NOT_CONNECTED:
        print(Fore.RED + "Error: Could not connect to the vehicle.")
        return None
    return connection

def read_dtc_codes(connection):
    if connection:
        cmd = obd.commands.GET_DTC  # get diagnostic trouble codes
        response = connection.query(cmd)
        if response.is_successful():
            return response.value
        else:
            print(Fore.RED + "Error: Could not read DTC codes.")
    return None

def get_error_description(code):
    descriptions = {
        "P0001": "Fuel Volume Regulator Control Circuit/Open",
        "P0002": "Fuel Volume Regulator Control Circuit Range/Performance",
        "P0003": "Fuel Volume Regulator Control Circuit Low",
        "P0004": "Fuel Volume Regulator Control Circuit High",
        # Add more error codes and descriptions as needed
    }
    return descriptions.get(code, "Unknown error code")

def log_dtc_codes(codes):
    if codes:
        for code in codes:
            description = get_error_description(code)
            logging.info(f"Code: {code}, Description: {description}")

def generate_report(codes):
    with open('report.txt', 'w') as report_file:
        report_file.write("Diagnostic Report\n")
        report_file.write("=================\n")
        for code in codes:
            description = get_error_description(code)
            report_file.write(f"Code: {code}, Description: {description}\n")

def show_dtc_codes(codes):
    if codes:
        result = "Diagnostic Trouble Codes (DTC):\n"
        for code in codes:
            description = get_error_description(code)
            result += f"Code: {code}, Description: {description}\n"
        messagebox.showinfo("DTC Codes", result)
    else:
        messagebox.showinfo("DTC Codes", "No DTC codes found.")

def main():
    logging.basicConfig(filename='diagnostic.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    print_banner()
    root = tk.Tk()
    root.title("Vehicle Diagnostic Tool")

    def on_check():
        connection = connect_to_vehicle()
        if connection:
            dtc_codes = read_dtc_codes(connection)
            print_dtc_codes(dtc_codes)
            log_dtc_codes(dtc_codes)
            generate_report(dtc_codes)
            show_dtc_codes(dtc_codes)

    check_button = tk.Button(root, text="Check DTC Codes", command=on_check)
    check_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
