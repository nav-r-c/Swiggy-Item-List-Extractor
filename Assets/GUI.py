from tkinter import *
from tkinter import messagebox
from Assets.extractor import Extractor
import Assets.consts as c
import Assets.pushToDB as ptd
from Assets.Table_Generator import Table_Generator

class GUI:
    def __init__(self):

        self.window=Tk()

        self.window.geometry('1000x500')

        self.bgImage=PhotoImage(file=c.BG_IMAGE_PATH)
        self.bgImageLabel=Label(self.window,image=self.bgImage)
        self.bgImageLabel.place(x=0,y=0)

        self.canvas=Canvas(self.window,height='350',width='700',bg='orange')
        self.canvas.place(x=325,y=175)

        self.greetingWidget=Label(self.window,text="Welcome to PESU Eateries!!",font="Calibri 24 bold",bg=None)
        self.greetingWidget.place(x=475,y=190)

        self.titleWidget=Label(self.window,text='Enter the Swiggy-URL of the restaurant:',font='Courier 8')
        self.titleWidget.place(x=330,y=250)

        self.UrlEntryWidget=Entry(self.window,borderwidth='0')
        self.UrlEntryWidget.place(x=625,y=250)
        
        self.restaurant_name=self.UrlEntryWidget.get()

        self.submitButtonImage=PhotoImage(file=c.BUTTON_IMAGE_PATH)
        self.submitButton=Button(self.window,image=self.submitButtonImage,command=self.submitButtonClick,border=0)
        self.UrlEntryWidget.bind('<Return>',self.enterButton)
        self.submitButton.place(x=510,y=280)

        self.window.mainloop()
            

    def submitButtonClick(self):
        # MyLabel2=Label(self.window,text="Here's the menu of "+self.UrlEntryWidget.get()+". Have a good meal!")
        # MyLabel2.pack()

        self.extractorObj = Extractor(
            restUrl = self.submission(),
            filename=c.FILENAME,
            maxLineLimit = c.MAX_LINE_LIMIT
        )
        self.sqlPushObject = ptd.Data_Operations()

        extractProcess = self.extractorObj.extract()

        if extractProcess == True:
            tableCreated = self.sqlPushObject.createTable(c.FILENAME)
            if tableCreated:
                self.sqlPushObject.add_items_to_table(c.FILENAME,c.FILE_STORAGE + c.FILENAME)
            messagebox.showinfo("Notification!",f"Your response has been saved succesfully into {c.FILENAME}.txt. Table created and appended into.")

            #temporaily calling a tksheet
            self.table = Table_Generator()
            root = Tk()
            table1= self.table.get_all_contents(root,c.FILENAME, display_category=True)
            table1.pack()


        else:
            messagebox.showinfo("ERROR!!","There was an error trying to access your url, please enter a valid url.")

    def enterButton(self, event):
        self.submitButtonClick()
            
    def submission(self):
        return self.UrlEntryWidget.get()
