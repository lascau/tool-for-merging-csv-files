from tkinter import *
import tkinter as tk
import os
import glob
from tkinter import filedialog as fd
import shutil
import pandas as pd
from os import walk
from tkinter import messagebox

# plotting
import matplotlib.pyplot as plt
import numpy as np


label_csvs = []
check_buttons = []
check_buttons_output = []

def popup_msg(message):
    popup = tk.Toplevel()
    def leave():
        popup.destroy()

    w = 300
    h = 70
    
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w)/ 2
    y = (sh - h) / 2 - 50
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))  
    popup.wm_title("Error")
    popup.iconbitmap(r"error_icon.ico")
    label = tk.Label(popup, text = message, font = ("Helvetica", 10))
    label.pack(side = "top", fill = "x", pady = 10)
    B1 = tk.Button(popup, text = "Ok", command = popup.destroy)
    B1.pack()
    #popup.mainloop()


def add_csv():
    file = fd.askopenfile()
    if file: 
        if file.name.endswith('.csv'):
            current_directory = os.getcwd()
            input_directory = os.path.join(current_directory, r'input_csv')
            if not os.path.exists(input_directory):
                os.makedirs(input_directory)
            shutil.copy(file.name, input_directory)
            #print(file.name)
        else:
            popup_msg('Please choose a file with csv extenstion!')
    #print('hello')
    draw_input_files()    

def clear():
    if not os.path.exists('input_csv') or  not os.listdir('input_csv'):
        popup_msg('No csv files to delete!')
    else:
        MsgBox = tk.messagebox.askquestion ('Delete multiple items','Are you sure you want to delete all files from your input directory?',icon = 'warning')
        if MsgBox == 'yes':
            # delete all csvs from input_csv directory
            input_file_list = glob.glob(os.path.join('input_csv', "*.csv"))
            for f in input_file_list:
                os.remove(f)

            output_file_list = glob.glob(os.getcwd() + '\\output_csv\\output.csv')
            for f in output_file_list:
                os.remove(f)

            for label in label_csvs:
                label.place_forget()
            for check_button in check_buttons:
                check_button.place_forget()
            for check_button in check_buttons_output:
                check_button.place_forget()
            check_buttons_output.clear()
            # draw_input_files()
            # draw_output_file()

_vars = []
checked_boxes = []
_files = []

def merge():
    if not os.path.exists('input_csv') or  not os.listdir('input_csv'):
        popup_msg('No csv files to merge...')
    else:
        checked_boxes.clear()
        cache = []
        for check_button, _var, file in zip(check_buttons, _vars, _files):
            if _var.get():
                checked_boxes.append(check_button.cget("text"))
                cache.append([check_button.cget("text"), file])
                print(check_button.cget("text"))
        
        files = []
        for (dirpath, dirnames, filenames) in walk(os.getcwd() + '/input_csv'):
            files.extend(filenames)
        columns_list = []
        columns_names_list = []
        current_directory = os.getcwd()
        output_directory = os.path.join(current_directory, r'output_csv')
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for file in files:
            current_file_path = os.getcwd() + '/input_csv/' + file
            data = pd.read_csv(current_file_path)
            #print(file)
            for col in data.columns:
                if [col, file] in cache:
                    columns_names_list.append(col)
                    columns_list.append(data[col])

        merged_data = pd.DataFrame(zip(*columns_list),
                            columns = columns_names_list)
        merged_data.to_csv('output_csv/output.csv')
        os.startfile(os.getcwd() + '/output_csv')

        for check_button in check_buttons_output:
            check_button.place_forget()
        draw_output_file()
        cache.clear()
        columns_list.clear()
        columns_names_list.clear()
        _vars.clear()
        _files.clear()

def open_input_directory():
    os.startfile(os.getcwd() + '/input_csv')

def open_output_directory():
    os.startfile(os.getcwd() + '/output_csv')

def draw_input_files():
    # sort csv decreasing by date
    input_files = list(filter(os.path.isfile, glob.glob(os.path.join('input_csv', "*.csv"))))
    input_files.sort(key=lambda x: os.path.getmtime(x))

    files = []
    for input_file in input_files:
       files.append(input_file[input_file.find('\\') + 1:])
    
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()
    new_x, new_y = 250, 300

    for file in files:
        new_y += 50
        label = Label(root, text = '  -' + file, font = "50")
        label.config(font=("Courier", 20))
        label.place(x = new_x, y = new_y)
        label_csvs.append(label)
        current_file_path = os.getcwd() + '/input_csv/' + file
        data = pd.read_csv(current_file_path)

        new_y += 50;
        for col in data.columns:
            curr_var = IntVar()
            check_button = Checkbutton(root, text=col, variable=curr_var, font=("Courier", 20))
            check_button.place(x = new_x, y = new_y)
            _vars.append(curr_var)
            check_buttons.append(check_button)
            _files.append(file)
            new_y += 50;

_vars_output = []

def draw_output_file():
    if os.listdir(os.getcwd() + '/output_csv'):
        output_data = pd.read_csv(os.getcwd() + '/output_csv/output.csv')
        new_x, new_y = 1100, 300

        new_y += 50;
        for col in output_data.columns:
            if col != 'Unnamed: 0':
                curr_var = IntVar()
                check_button = Checkbutton(root, text=col, variable=curr_var, font=("Courier", 20))
                check_button.place(x = new_x, y = new_y)
                _vars_output.append(curr_var)
                check_buttons_output.append(check_button)
                new_y += 50;
    

def draw_histogram():

    checked_boxes = []
    
    for check_button, _var in zip(check_buttons_output, _vars_output):
        if _var.get():
            checked_boxes.append(check_button.cget("text"))
    print(checked_boxes)
    # draw
    output_data = pd.read_csv(os.getcwd() + '/output_csv/output.csv')
    if len(checked_boxes) == 1:
        print(checked_boxes[0])
        x = output_data[checked_boxes[0]]
        x.to_numpy()
        print(x)
        plt.hist(x, density=False, bins=1000)
        plt.xlabel(checked_boxes[0]);
        plt.show()
    
    check_buttons_output.clear()
    _vars_output.clear()
    draw_output_file()

def draw_scatter():
    checked_boxes = []
    
    for check_button, _var in zip(check_buttons_output, _vars_output):
        if _var.get():
            checked_boxes.append(check_button.cget("text"))
    print(checked_boxes)
    # draw
    output_data = pd.read_csv(os.getcwd() + '/output_csv/output.csv')
    if len(checked_boxes) == 1:
        print(checked_boxes[0])
        output_col = output_data[checked_boxes[0]]
        mp = dict() 
        for e in output_col: 
            if e in mp.keys(): 
                mp[e] += 1
            else: 
                mp[e] = 1
              
        _x = list()
        _y = list()
        for elem in mp.keys():
            _x.append(elem)
            _y.append(mp[elem])
        print(_x)
        print(_y)
        plt.bar(_x, _y, align="center")
        plt.xlabel(checked_boxes[0]);
        plt.ylabel('Frequency')
        plt.show()
    
    check_buttons_output.clear()
    _vars_output.clear()
    draw_output_file()

def draw_line_graph():
    
    checked_boxes = []
    
    for check_button, _var in zip(check_buttons_output, _vars_output):
        if _var.get():
            checked_boxes.append(check_button.cget("text"))
    print(checked_boxes)
    # draw
    output_data = pd.read_csv(os.getcwd() + '/output_csv/output.csv')
    if len(checked_boxes) == 1:
        print(checked_boxes[0])
        output_col = output_data[checked_boxes[0]]
        mp = dict() 
        for e in output_col: 
            if e in mp.keys(): 
                mp[e] += 1
            else: 
                mp[e] = 1
              
        _x = list()
        _y = list()
        for elem in mp.keys():
            _x.append(elem)
            _y.append(mp[elem])
        print(_x)
        print(_y)
        plt.plot(_x, _y)
        plt.xlabel(checked_boxes[0]);
        plt.ylabel('Frequency')
        plt.show()
    
    check_buttons_output.clear()
    _vars_output.clear()
    draw_output_file()
    
root = Tk()
root.title('Csv merger')
root.state('zoomed')
root.iconbitmap(os.getcwd() + r"/assets/icon.ico")
root['bg'] = '#c7c074'
'''
photo = PhotoImage(file = "icon_background.png")
w = Label(root, image=photo)
w.pack()
'''
root.geometry('750x500+120+120')


frame = tk.Frame(root)



photo_merge = PhotoImage(file=os.getcwd() + '/assets/merging.png')
merge_button = tk.Button(root, image = photo_merge, command = merge)

x_total = root.winfo_screenwidth()
y_total = root.winfo_screenheight()

merge_button.place(x = x_total / 2 - 100 , y = y_total / 2 + 300)

w = Label(root, text ='Your input directory:', font = "50")
w.config(font=("Courier", 30))
w.place(x = 250, y = 300)

o = Label(root, text = 'Your output directory:', font = "50")
o.config(font=("Courier", 30))
o.place(x = 1100, y = 300)

# row 1 utility
photo = PhotoImage(file=os.getcwd() + '/assets/browse_input.png')
browse_button = tk.Button(root, image = photo, command=open_input_directory)
browse_button.place(x = 500, y = 10)

photo3 = PhotoImage(file=os.getcwd() + '/assets/add_csv_icon.png')
browse_button = tk.Button(root, image = photo3, command=add_csv)
browse_button.place(x = 600, y = 10)

photo4 = PhotoImage(file=os.getcwd() + '/assets/recycle bin.png')
clear_button = tk.Button(root, image = photo4, command = clear)
clear_button.place(x = 700, y = 10)


photo2 = PhotoImage(file=os.getcwd() + '/assets/browse_output.png')
browse_button = tk.Button(root, image = photo2, command=open_output_directory)
browse_button.place(x = 815, y = 10)

# row 2 visualisation
photo5 = PhotoImage(file=os.getcwd() + '/assets/histogram.png')
browse_button = tk.Button(root, image = photo5, command=draw_histogram)
browse_button.place(x = 500, y = 150)

photo6 = PhotoImage(file=os.getcwd() + '/assets/scatter.png')
browse_button = tk.Button(root, image = photo6, command=draw_scatter)
browse_button.place(x = 600, y = 150)

photo7 = PhotoImage(file=os.getcwd() + '/assets/line-graph.png')
browse_button = tk.Button(root, image = photo7, command=draw_line_graph)
browse_button.place(x = 700, y = 150)

draw_input_files()

root.mainloop()
