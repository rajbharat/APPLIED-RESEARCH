from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk

import os
from prediction import pre
from stat import S_ISREG, ST_CTIME, ST_MODE

from tensorflow.keras import backend as K
from keras import backend as K







class App:
    def __init__(self, root):
        self.root = root
        self.root.title("App")
        self.root.geometry("1300x700")

        # self.root.resizable(0, 0)
        self.current=0
        self.path_frame = Frame(self.root)
        self.path_frame.pack(pady=20)
        self.main_frame=None



        lb = Button(self.path_frame, fg="#ffffff", bg="#0f4f4d", text="Browse path :", command=self.folder_dialog)
        lb.config(height=2, width=12)
        lb.pack(side=LEFT)

        self.folder_path = Label(self.path_frame, width=75, font=('arial', 12), relief="groove",height=2)
        self.folder_path.pack(side=LEFT, padx=20)

        self.predict_btn = Button(self.path_frame, text="Predict",command=lambda: self.btn_click(),height=2)
        self.predict_btn.pack(side=LEFT,padx=20)

        self.processbar=Label(self.root, width=75, font=('arial', 12),fg='red')


        self.base_dir=""


    def display(self,base_dir):
        K.clear_session()

        base_dir=base_dir+'/'

        obj=pre()
        obj.predict_test(base_dir)


        self.processbar.pack_forget()
        base_dir = base_dir + '/'
        self.img_path=[base_dir+"img/"+i for i in os.listdir(base_dir+'img/')]
        self.img_path = ((os.stat(path), path) for path in self.img_path)
        data = ((stat[ST_CTIME], path) for stat, path in self.img_path if S_ISREG(stat[ST_MODE]))
        self.image_list = []
        for cdate, path in sorted(data):
            self.image_list.append(path)



        self.main_frame = Frame(self.root)
        self.main_frame.pack()


        self.label = Label(self.main_frame, width=500, height=400)
        self.label.pack()

        self.text_label = Label(self.main_frame, width=100, height=10)
        self.text_label.pack()

        self.btn_frame=Frame(self.main_frame)
        self.frame1 = Frame(self.btn_frame)
        self.frame1.pack()
        self.frame2 = Frame(self.btn_frame)
        Button(self.frame2, text='Quit', command=root.quit,width=9, height=2).pack()
        self.frame2.pack(side=LEFT)

        self.frame5 = Frame(self.btn_frame)
        self.b3 = Button(self.frame5, text='First', command=lambda: self.first_btn(),width=9, height=2)
        self.b3.pack()
        self.frame5.pack(side=LEFT,padx=10)

        self.frame6 = Frame(self.btn_frame)
        self.b6 = Button(self.frame6, text='last', command=lambda: self.last_btn(),width=9, height=2)
        self.b6.pack()
        self.frame6.pack(side=LEFT,padx=10)



        self.frame4 = Frame(self.btn_frame)
        self.b2 = Button(self.frame4, text='Next picture', command=lambda: self.move(+1),height=2)
        self.b2.pack()
        self.frame4.pack(side=LEFT,padx=10)

        self.frame3= Frame(self.btn_frame)
        self.b1=Button(self.frame3, text='Previous picture', command=lambda: self.move(-1),height=2)
        self.b1.pack()
        self.frame3.pack(side=LEFT,padx=10)
        self.move(0)

        self.btn_frame.pack()

    def first_btn(self):
        self.current=0
        self.move(0)
        self.b1.pack_forget()
    def last_btn(self):
        self.current=len(self.image_list)-1
        self.move(0)
        self.b2.pack_forget()



    def move(self,delta):

        # if not (0 <= self.current + delta < len(self.image_list)):
        #     messagebox.showinfo('End', 'No more image.')
        #     return

        print(self.current+delta)
        if self.current+delta<=0:
            self.b1.pack_forget()
        else:
            self.b1.pack(side=RIGHT,padx=40)
        print(len(self.image_list))
        if self.current==len(self.image_list)-2:
            self.b2.pack_forget()
        else:
            self.b2.pack(side=LEFT,padx=40)

        self.current += delta
        image = Image.open(self.image_list[self.current])

        if "nomask" in self.image_list[self.current]:
            self.text_label.config(text="No mask on this Image",fg="red")
        else:
            self.text_label.config(text="")
        photo = ImageTk.PhotoImage(image)
        self.label['image'] = photo
        self.label.photo = photo


    def folder_dialog(self):
        filename = filedialog.askdirectory(initialdir="/")
        if filename:
            self.folder_path.config(text=filename)
            self.base_dir = filename
        if self.main_frame != None:
            self.main_frame.pack_forget()



    def btn_click(self):
        if self.main_frame != None:
            self.main_frame.pack_forget()


        self.processbar.config(text="Please wait for prediction ......")
        self.processbar.pack()
        # self.processbar.update_idletasks()
        self.processbar.update()


        self.display(self.base_dir)




root = Tk()
App(root)
root.mainloop()




