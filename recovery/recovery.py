import argparse
import datetime
import os
import wmi
import winreg
import win32com.client
import win32evtlog
import logging
import winapps
import tkinter as tk
from tkinter import ttk, Canvas
#import seaborn as sns
#import pandas as pd

from browser_history import get_history

def create_timeline_window(events):
    timeline_window = tk.Toplevel()
    timeline_window.title("Timeline")
    timeline_window.geometry("800x600")

    canvas = Canvas(timeline_window, bg="white")
    canvas.pack(fill="both", expand=True, side="left")
    scrollbar = ttk.Scrollbar(timeline_window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    draw_timeline(canvas, events)

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def draw_timeline(canvas, events):
    canvas_width = canvas.winfo_reqwidth()
    timeline_height = (len(events) + 1) * 30
    y_step = (timeline_height) // (len(events) + 1) 
    y = 10 + y_step
    for datetime, event in events:
        canvas.create_line(canvas_width // 2, 10, canvas_width // 2, y)
        x = canvas_width // 2
        canvas.create_line(x, y, x + 10, y)
        canvas.create_text(x + 20, y, anchor="w", text=f"{datetime.strftime('%d-%m-%Y')} - {event}")

        y += y_step


class DirectoryTreeView:
    def __init__(self, master, directory):
        self.master = master
        self.master.title(f"Directory Tree - {directory}")
        self.master.geometry("800x600")
        style = ttk.Style()
        style.theme_use("clam")

        self.treeview = ttk.Treeview(self.master)
        self.treeview.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(self.master, orient="vertical", command=self.treeview.yview)
        vsb.pack(side="right", fill="y")

        self.treeview.configure(yscrollcommand=vsb.set)
        self.treeview.bind("<<TreeviewOpen>>", self.on_treeview_open)

        self.treeview.heading("#0", text=directory, anchor="w")
        root_node = self.treeview.insert("", "end", text=directory, open=True)

        self.populate_treeview(root_node, directory)

    def populate_treeview(self, parent, parent_path):
        for filename in os.listdir(parent_path):
            path = os.path.join(parent_path, filename)
            if os.path.isdir(path):
                try:
                    node = self.treeview.insert(parent, "end", text=filename, open=False)
                    self.populate_treeview(node, path)
                except PermissionError:
                    pass
            else:
                self.treeview.insert(parent, "end", text=filename)

    def on_treeview_open(self, event):
        node = self.treeview.focus()
        if self.treeview.item(node, "text") == "":
            self.treeview.delete(*self.treeview.get_children(node))
            self.populate_treeview(node, self.treeview.item(node, "values")[0])

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Tool to get information about a Windows System"
    )
    parser.add_argument(
        '-s',
        metavar='start',
        help="Starting date of range in 'DD-MM-YYYY' format (by default: '01-01-1970')"
    )
    parser.add_argument(
        '-e',
        metavar='end',
        help="Ending date of range in 'DD-MM-YYYY' format (by default: today)"
    )
    parser = parser.parse_args()

    return parser.s, parser.e

def manage_dates(start, end):
    try:
        if start and not end:
            start = datetime.datetime.strptime(start, '%d-%m-%Y')
            end = datetime.datetime.now()
        elif end and not start:
            start = datetime.datetime.fromtimestamp(0)
            end = datetime.datetime.strptime(end, '%d-%m-%Y')
        elif not start and not end:
            start = datetime.datetime.now() - datetime.timedelta(days=365)
            end = datetime.datetime.now()
            print("No dates received, using by default one year range\n")
        elif start == end:
            print("Start and end dates are the same, using one day range\n")
            start = datetime.datetime.strptime(start, '%d-%m-%Y')
            end = start + datetime.timedelta(days=1)
        else:
            start = datetime.datetime.strptime(start, '%d-%m-%Y')
            end = datetime.datetime.strptime(end, '%d-%m-%Y')

            if end < start:
                print("End date is before start date, invert dates and execute? [y/n]")
                answer = input().lower()
                if answer == 'y':
                    start, end = end, start
                else:
                    if answer == 'n':
                        print("Exiting...")
                        exit()
                    else:
                        print("Invalid answer, try again")
                    exit()
    except:
        print("Invalid date format, try again")
        exit()
    return start, end

def reg_branch_changes(start, end):
    changes = set()

    key_types = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]

    for key in key_types:
        try:
            manage = winreg.OpenKey(key, "Softwarte\\Microsoft\\Windows\\CurrentVersion\\Run")
            timestamp = winreg.QueryInfoKey(manage)[2] / 10000000 - 11644473600
            date = datetime.datetime.fromtimestamp(timestamp)
            if start <= date <= end:
                changes.add((date, key))
        except:
            pass
    return changes

def get_files(route, extension):
    list = []
    for route, _, files in os.walk(route):
        for file in files:
            if extension is None or file.endswith("." + extension):
                list.append(os.path.join(route, file))
    return list

def recent_files(start, end):
    files = set()
    directory = os.environ['USERPROFILE'] + '\\AppData\\Roaming\\Microsoft\\Windows\\Recent'
    for file in os.listdir(directory):
        if file.endswith('.lnk'):
            shell = win32com.client.Dispatch("WScript.Shell")
            route = shell.CreateShortCut(directory + '\\' + file).targetpath

            if os.path.isfile(route):
                date = datetime.datetime.fromtimestamp(os.path.getctime(directory + '\\' + file))
                if start <= date <= end:
                    files.add((date, route))
    return files

def ficheros(ruta, extension):
    lista = []
    for ruta, _, ficheros in os.walk(ruta):
        for fichero in ficheros:
            if extension is None or fichero.endswith("." + extension):
                lista.append(os.path.join(ruta, fichero))
    return lista

def temp_files(start, end):
    files = set()
    directory = os.environ['USERPROFILE'] + '\\AppData\\Local\\Temp'
    for file in ficheros(directory, None):
        try:
            date = datetime.datetime.fromtimestamp(os.path.getctime(file))
            if start <= date <= end:
                files.add((date, file))
        except:
            pass
    return files

def running_apps():
    apps = []
    for app in conection.Win32_Process():
        apps.append(app.Name)
    return apps

def instaled_apps(start, end):
    apps = set(app.Name for app in conection.Win32_Product())
    applications = set()
    for app in winapps.list_installed():
        try:
            name = app.name
            date = app.install_date
            route = app.uninstall_string
            if not date and route:
                if route[0] == route[-1] == "\"":
                    route = route[1:-1]
                date = datetime.datetime.fromtimestamp(os.path.getctime(route))
            if date is not None and start.date() <= date <= end.date():
                applications.add((date, name))
                apps.remove(name)
        except:
            pass
    return applications, apps

def navegation_history(start, end):
    logging.disable(logging.CRITICAL)
    entries = set()
    histories = get_history().histories
    for entry in histories:
        date, url = entry
        date = date.replace(tzinfo=None)
        if start <= date <= end:
            entries.add((date, url))
    return entries

def connected_devices():
    def physical_units():
        devices = set()
        if not conection.Win32_PhysicalMedia():
            print("No physical devices connected")
        else:
            for device in conection.Win32_PhysicalMedia():
                if device.Name is not None:
                    devices.add(device.Name)
        return devices
    def extraible_units():
        devices = set()
        if not conection.Win32_CDROMDrive():
            devices.add("No CDROMs devices connected")
        else:
            for device in conection.Win32_CDROMDrive():
                if device.Name is not None:
                    devices.add(device.Name)
        if not conection.Win32_USBController():
            devices.add("Not USBs devices connected")
        else:
            for device in conection.Win32_USBController():
                if device.Name is not None:
                    devices.add(device.Name)
        return devices
    return physical_units().union(extraible_units())
    
def system_events():
    manage = win32evtlog.OpenEventLog(None, 'EventLogRegister')
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    registries = set()
    for registry in win32evtlog.ReadEventLog(manage, flags, 0):
        name = registry.SourceName
        date = registry.TimeWritten.date()
        if start.date() <= date <= end.date():
            registries.add((date, name))
    return registries

if __name__ == '__main__':
    start, end = parse_arguments()
    start, end = manage_dates(start, end)
    conection = wmi.WMI()
    changes = reg_branch_changes(start, end)
    print("Registry branches changes:")
    for date, change in sorted(changes):
        print("\t{}\t{}".format(date.strftime("%d-%m-%Y"), change))
    recents = recent_files(start, end)
    print("Recent files:")
    for date, file in sorted(recents):
        print("\t{}\t{}".format(date.strftime("%d-%m-%Y"), file))
    temps = temp_files(start, end)
    print("Temporary files:")
    for date, temp in sorted(temps):
        print("\t{}\t{}".format(date.strftime("%d-%m-%Y"), temp))
    running = running_apps()
    print("Running apps:")
    for app in running:
        print("\t" + app)
    instaled, no_date = instaled_apps(start, end)
    print("Instaled apps:")
    for (date, name) in sorted(instaled):
        print("\t{}\t{}".format(date.strftime('%d-%m-%Y'), name))
    print("Instaled apps with unknown date:")
    for name in no_date:
        print("\t\t" + name)
    history = navegation_history(start, end)
    print("Navegation history:")
    for entry in sorted(history):
        print("\t{}\t{}".format(entry[0].strftime("%d-%m-%Y"), entry[1]))
    devices = connected_devices()
    print("Connected devices:")
    for device in devices:
        print("\t" + device)
    registries = system_events()
    print("Event registries:")
    for (date, name) in sorted(registries):
        print("\t{}\t{}".format(date.strftime('%d-%m-%Y'), name))
    recents = {(date.date(),file) for date, file in recents}
    temps = {(date.date(), tmp) for date, tmp in temps}
    history = {(date.date(), url) for date, url in history}
    events = sorted(list(recents) + list(temps) + list(history) + list(registries) + list(instaled))
    root = tk.Tk()
    if events:
        create_timeline_window(events)
    DirectoryTreeView(root, os.path.expanduser("C:\Program Files"))
    root.mainloop()