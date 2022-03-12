import tkinter as tk
from tracemalloc import start
import Recordurbate
import config
import json
import subprocess
import os
from tkinter.simpledialog import askstring
from tkinter import PhotoImage, messagebox

state='0'
try:
    file=open('state.txt','r')
    state=file.read()
    file.close()
except:
    file=open('state.txt','w')
    file.write('0')
    file.close()
def change_state():
    global state
    if state=='0':
        file=open('state.txt','w')
        file.write('1')
        file.close()
        state='1'
        # print('1')
    else:
        file=open('state.txt','w')
        file.write('0')
        file.close()
        state='0'
        # print('0')

window=tk.Tk()
window.title("Recordurbate")
window.geometry("400x400")
# set window icon
photo = PhotoImage(file = "icon.png")
window.iconphoto(False, photo)



# add 3 buttons to the window with the text list, add, del, start and stop
buttons=[]
# add a listbox to the window
listbox=tk.Listbox(window, width=30, height=10)
listbox.grid(row=6, column=0, columnspan=5)
# add a scrollbar to the listbox
scrollbar=tk.Scrollbar(window)
scrollbar.grid(row=6, column=5, rowspan=5, sticky=tk.N+tk.S)
# set the height of the scrollbar to the listbox
# scrollbar.config(height='', command=listbox.yview)


# link the listbox and the scrollbar

listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=listbox.yview)

# fill the listbox with the streamers


def list_streamers():
    with open("/home/george/Documentos/pythonscripts/Recordurbate/recordurbate/configs/config.json", "r") as f:
        config = json.load(f)
    models=config["streamers"]
    # clear the listbox
    listbox.delete(0, tk.END)
    for model in models:
        listbox.insert(tk.END, model)
        print(model)
list_streamers()

def exec_path():
    local_dir_path=os.path.dirname(os.path.realpath(__file__))
    print(local_dir_path+'/Recordurbate.py')
    

def add_model():
    print("add")
    model = askstring("Input", "Input a streamer")
    print(model)
    with open("configs/config.json", "r") as f:
        config = json.load(f)
    config["streamers"].append(model)
    with open("configs/config.json", "w+") as f:
        json.dump(config, f, indent=4)
    list_streamers()        



def del_model():
    print("del")
    model = listbox.get(tk.ACTIVE)
    resp=messagebox.askyesno("askyesno", "Eliminar "+model+"?")
    if resp:
        with open("configs/config.json", "r") as f:
            config = json.load(f)
        config["streamers"].remove(model)
        with open("configs/config.json", "w+") as f:
            json.dump(config, f, indent=4)
        list_streamers()
    
started = False
# addu a label with a background image
img = tk.PhotoImage(file='recording.png')
img2 = tk.PhotoImage(file='recording1.png')
if state=='1':
    label=tk.Label(window, image=img)
else:
    label=tk.Label(window, image=img2)
label.grid(row=0, column=0, columnspan=5)

label1=tk.Label(window, text="Recordurbate")
label1.grid(row=1, column=0, columnspan=5)

# frameCnt = 12
# frames = [tk.PhotoImage(file='recordi.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]

def update(ind):

    index=0
    while index<ind:
        print(index)
        window.after(100, update1, index)
        index+=1
    window.after(100, update, ind)
# frameCnt1 = 12
# frames1 = [tk.PhotoImage(file='recordi1.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]




    



def update1(ind):

    label.configure(image=img2)
def start_recorder():
    started = True
    print("start")
    label.config(image=img)
    label1.config(text="Recording")
    change_state()
    
    # window.after(100, update, 10)
    # change_label_image()
    subprocess.call(["python3", "/home/george/Documentos/pythonscripts/Recordurbate/recordurbate/Recordurbate.py", "start"])
def stop_recorder():
    started = False
    print("stop")
    change_state()
    label.config(image=img2)
    label1.config(text="Recordurbate")
    # window.after(100, update1, 0)
    subprocess.call(["python3", "/home/george/Documentos/pythonscripts/Recordurbate/recordurbate/Recordurbate.py", "stop"])
    # change_label_image()

for i in range(3):
    buttons.append(tk.Button(window, text='List', width=5, height=1,command=list_streamers))
    buttons.append(tk.Button(window, text="Add", width=5, height=1,command=add_model))
    buttons.append(tk.Button(window, text="Del", width=5, height=1,command=del_model))
    buttons.append(tk.Button(window, text="Start", width=5, height=1,command=start_recorder))
    buttons.append(tk.Button(window, text="Stop", width=5, height=1,command=stop_recorder))
buttons[0].grid(row=8, column=0)
buttons[1].grid(row=8, column=1)
buttons[2].grid(row=8, column=2)
buttons[3].grid(row=8, column=3)
buttons[4].grid(row=8, column=4)

# update(0)

# get_exec_path()
# window.after(0, update, 0)

window.mainloop()