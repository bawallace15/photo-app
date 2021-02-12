#!/usr/bin/python3
import sys
import tkinter
from PIL import Image, ImageTk
import time
import yaml
from pathlib import Path
from itertools import cycle

class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.pic_files = []
        self.pic = ''
        self.order = []

        with open('./config.yml', 'r') as f:
            self.config = yaml.safe_load(f)

        # set the order as alphabetical default pics
        self.pic_files = list(map(lambda x: str(x), list(Path(self.config['data-dir']).glob('*.jpg'))))
        picyaml = {'order': self.pic_files}
        with open('/photo-app/piclist.yml', 'w') as f:
            yaml.dump(picyaml, f)

        #set config for pics
        self.sleepTime = self.config['sleep-time']
        self.pictures = cycle(self.pic_files)

        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.overrideredirect(1)
        self.geometry(f"{self.w}x{self.h}+0+0")
        self.focus_set()    
        self.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        #root.bind("<Escape>", lambda e: (print('hi'))
        self.canvas = tkinter.Canvas(self,width=self.w,height=self.h)
        self.canvas.pack()
        self.canvas.configure(background='black')
        image = self.getPic()
        self.image_on_canvas = self.canvas.create_image(self.w/2,self.h/2,image=image)
        self.update_idletasks()
        self.update()
        time.sleep(self.sleepTime)

    def getPic(self):
        with open('/photo-app/piclist.yml', 'r') as f:
            picOrder = yaml.safe_load(f)['order']
        # load current list. if no change proceed
        if self.pic_files == picOrder:
            self. pic = next(self.pictures)
            print(f'\t{self.pic}')
            image = self.sizeImg(Image.open(self.pic))
            return image
        # if change reset cycle and move to i+1
        # TODO add capability for deleting pics
        # TODO add capability for adding pics in new order
        else:
            print('update found. recycling...')
            self.pic_files = picOrder
            self.pictures = cycle(self.pic_files)
            found = False
            while not found:
                if next(self.pictures) == self.pic:
                    self.pic = next(self.pictures)
                    print(f'\t{self.pic}')
                    image = self.sizeImg(Image.open(self.pic))
                    return image

    def sizeImg(self, pilImage):
        imgWidth, imgHeight = pilImage.size
        if imgWidth > self.w or imgHeight > self.h:
            ratio = min(self.w/imgWidth, self.h/imgHeight)
            imgWidth = int(imgWidth*ratio)
            imgHeight = int(imgHeight*ratio)
            pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(pilImage)
        return image

    # def getPic(self):
    #     #self.getPicList(self.config['data-dir'])
    #     self.pic = next(self.pictures)
    #     print(self.pic)
    #     image = self.sizeImg(Image.open(self.pic))
    #     return image

    def showSlides(self):
        image = self.getPic()
        self.canvas.itemconfig(self.image_on_canvas, image=image)
        self.update_idletasks()
        self.update()
        time.sleep(self.sleepTime)
        self.showSlides()

if __name__ == '__main__':
    #pics = getPics(config['data-dir'])
    #for pic in cycle(pics):
    #pilImage = Image.open(pic)
    #showPIL(pilImage,5)
    app = App()
    try:
        app.showSlides()
        app.mainloop()
    except KeyboardInterrupt:
        print('exiting...')
        app.destroy()
            