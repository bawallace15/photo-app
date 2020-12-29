#!/usr/bin/python3
import sys
import tkinter
from PIL import Image, ImageTk
import time
import yaml
from pathlib import Path
from itertools import cycle

def loadConfig():
    with open('./config.yml', 'r') as f:
        config = yaml.safe_load(f)
    return config

def getPics(photoPath):
    pics = Path(photoPath).glob('*')
    return list(pics)

def showPIL(pilImage, showtime):
    #top level widget class
    root = tkinter.Tk()
    #get the window width and height
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry(f"{w}x{h}+0+0")
    root.focus_set()    
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    #root.bind("<Escape>", lambda e: (print('hi'))
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.update_idletasks()
    root.update()
    time.sleep(showtime)

if __name__ == '__main__':
    config = loadConfig()
    pics = getPics(config['data-dir'])
    for pic in cycle(pics):
        pilImage = Image.open(pic)
        showPIL(pilImage,5)
