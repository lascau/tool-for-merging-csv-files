from tkinter import *
import tkinter as tk
import os
import glob
from tkinter import filedialog as fd
import shutil
import pandas as pd
from os import walk

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

label_csvs = []

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
    label = tk.Label(popup, text = message, font = NORM_FONT)
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
        popup_msg('No csv files to process...')
    else:
        # delete all csvs from input_csv directory
        filelist = glob.glob(os.path.join('input_csv', "*.csv"))
        for f in filelist:
            os.remove(f)
    for label in label_csvs:
        #print(label)
        label.place_forget()
    draw_input_files()

def merge():
    if not os.path.exists('input_csv') or  not os.listdir('input_csv'):
        popup_msg('No csv files to merge...')
    else:
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
            print(file)
            for col in data.columns:
                columns_names_list.append(col)
                columns_list.append(data[col])

        merged_data = pd.DataFrame(zip(*columns_list),
                            columns = columns_names_list)
        merged_data.to_csv('output_csv/output.csv')
        os.startfile(os.getcwd() + '/output_csv')

def open_input_directory():
    os.startfile(os.getcwd() + '/input_csv')

def open_output_directory():
    os.startfile(os.getcwd() + '/output_csv')

def draw_input_files():
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()
    new_x, new_y = 250, 300
    files = []
    for (dirpath, dirnames, filenames) in walk(os.getcwd() + '/input_csv'):
        files.extend(filenames)
    for file in files:
        new_y += 50
        label = Label(root, text = '  -' + file, font = "50")
        label.config(font=("Courier", 20))
        label.place(x = new_x, y = new_y)
        label_csvs.append(label)
        current_file_path = os.getcwd() + '/input_csv/' + file
        data = pd.read_csv(current_file_path)

    #for col in data.columns:
    #    print(

root = Tk()
root.title('Csv merger')
root.iconbitmap(r"icon.ico")
root['bg'] = '#6BE873'
'''
photo = PhotoImage(file = "icon_background.png")
w = Label(root, image=photo)
w.pack()
'''
root.geometry('750x500+120+120')


frame = tk.Frame(root)



photo_merge = PhotoImage(file=os.getcwd() + '/merging.png')
merge_button = tk.Button(root, image = photo_merge, command = merge)

x_total = root.winfo_screenwidth()
y_total = root.winfo_screenheight()

merge_button.place(x = x_total / 2 - 100 , y = y_total / 2 + 300)

w = Label(root, text ='Your input directory:', font = "50")
w.config(font=("Courier", 30))
w.place(x = 250, y = 300)

photo = PhotoImage(file=os.getcwd() + '/browse_input.png')
browse_button = tk.Button(root, image = photo, command=open_input_directory)
browse_button.place(x = 500, y = 10)

photo3 = PhotoImage(file=os.getcwd() + '/add_csv_icon.png')
browse_button = tk.Button(root, image = photo3, command=add_csv)
browse_button.place(x = 600, y = 10)

photo4 = PhotoImage(file=os.getcwd() + '/recycle bin.png')
clear_button = tk.Button(root, image = photo4, command = clear)
clear_button.place(x = 700, y = 10)


photo2 = PhotoImage(file=os.getcwd() + '/browse_output.png')
browse_button = tk.Button(root, image = photo2, command=open_output_directory)
browse_button.place(x = 815, y = 10)

draw_input_files()

'''
var2 = tk.IntVar()
c2 = tk.Checkbutton(root, text='C++',variable=var2, onvalue=1, offvalue=0, command = add_row)
c2.pack()
'''
root.mainloop()
