from tkinter import *
import tkinter as tk
import os
import glob
from tkinter import filedialog as fd
import shutil

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

def popup_msg(message):
    popup = tk.Tk();
    def leave():
        popup.destroy()

    popup.wm_title("Error")
    label = tk.Label(popup, text = message, font = NORM_FONT)
    label.pack(side = "top", fill = "x", pady = 10)
    B1 = tk.Button(popup, text = "Ok", command = popup.destroy)
    B1.pack()
    popup.mainloop()


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

def clear():
    if not os.path.exists('input_csv') or  not os.listdir('input_csv'):
        popup_msg('No csv files to process...')
    else:
        # delete all csvs from csv_storage directory
        filelist = glob.glob(os.path.join('input_csv', "*.csv"))
        for f in filelist:
            os.remove(f)
        

root = Tk()
root.title('Csv merger')
root.iconbitmap(r"icon.ico")
root['bg'] = '#6BE873'
'''
photo = PhotoImage(file = "icon_background.png")
w = Label(root, image=photo)
w.pack()
'''
root.geometry('750x500')

frame = tk.Frame(root)
frame.pack()


add_button = tk.Button(frame,
                       text = 'Add csv',
                       command = add_csv)
add_button.pack()

clear_button = tk.Button(frame,
                         text = 'Clear',
                         command = clear)
clear_button.pack()




root.mainloop()
