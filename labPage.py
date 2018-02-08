import tkinter as tk
from tkinter.filedialog import askopenfilename
import numpy as np
import imageProcessingUI
from tkinter import ttk, PhotoImage
from PIL import ImageTk,Image
import tkinter.messagebox

class LabPage(tk.Frame):
    args = ['0'] * 19
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#74caf9")
        #background image
        #page title
#        label = tk.Label(self, bg='#74caf9', text ="Lab Results", font=controller.title_font)
#        label.grid(row=0, columnspan=3, pady=10, padx=200)
        #pic title
        image = Image.open('images\\labs.png')
        photo = ImageTk.PhotoImage(image)
        self.photolabel = tk.Label(self, image=photo, bg='#74caf9')
        self.photolabel.image = photo 
        self.photolabel.grid(row=0, columnspan=3, pady=10, padx=50)

        #creating a button that opens file dialog box when clicked
        browseButn = tk.Button(self, text = 'Browse...', bg="#0759a5", fg="#ffffff", command=self.browsefile, font=controller.label_font)
        browseButn.grid(row=1, columnspan=3, pady=10, padx=200)
        
        #button to go back to the Questionnaire
        backButn = tk.Button(self, text = "Back", width=10, bg="#0759a5", fg="#ffffff", command=lambda: controller.show_frame("QuestionPage"))
        backButn.grid(row=3, column=0, pady=10, padx=10)
        #button to skip to the Image page
        skipButn = tk.Button(self, text = "Skip", width=10, bg="#0759a5", fg="#ffffff", command=lambda: self.skip())
        skipButn.grid(row=3, column=1, pady=10, padx=10)
        #button to submit the vals go to the Image Page
        submitButn = tk.Button(self, text = "Next", width=10, bg="#0759a5", fg="#ffffff", command=lambda: controller.show_frame("ImagePage"))
        submitButn.grid(row=3, column=2, pady=10, padx=10)
        #create the listbox
        self.fileNames= []
        #packs items in frame
        self.grid()
        
    def browsefile(self):
        #takes the filepath name
        filepath=askopenfilename (filetypes=(("CSV file", "*.csv"),  ("All files", "*.*")), title="Choose a file")
        if filepath:
            #adds the filepath name on the fileNames list
            self.fileNames.append(filepath)
            #the path is shown with a label
            path= tk.Label(self, text=filepath, bg="#0759a5", fg="#ffffff")
            data = np.loadtxt(filepath, delimiter=',', dtype="U12")
            i = 0
            data = data.tolist()
            for i in range(0,17):
                LabPage.args[i] = data[i]
            #adds the label to the window
            #print (LabResults.args)
            imageProcessingUI.ImagePage.imageArgs = LabPage.args
            path.grid(row=2,column=1)
        print(LabPage.args[i])
        return data
        
    def skip(self):
        for i in range(0,17):
                LabPage.args[i] = '0'
        print(LabPage.args)
        imageProcessingUI.ImagePage.imageArgs = LabPage.args
        self.controller.show_frame("ImagePage")