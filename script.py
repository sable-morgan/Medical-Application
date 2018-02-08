import tkinter as tk
from tkinter import ttk, PhotoImage
from tkinter import font  as tkfont
from PIL import ImageTk, Image
import os, sys
import neuralNetwork, imagingNeuralNetwork, brainNeuralNetwork, spineNeuralNetwork, maskNeuralNetwork
import houseDB, registerPage, login, mainPage, labPage, imageProcessingUI, resultsPage
import adminMainPage
import tkinter.messagebox
#need to import questionPage
#from black_White import imageProccessing 
#from PIL import Image, ImageTk
database = houseDB.HouseDB()

diag = neuralNetwork.NeuralNet()
INN = imagingNeuralNetwork.ImagingNeuralNet()
INN.setup_neural_network()
BNN = brainNeuralNetwork.BrainNeuralNet()
BNN.setup_neural_network()
SNN = spineNeuralNetwork.SpineNeuralNet()
SNN.setup_neural_network()
MNN = maskNeuralNetwork.MaskNeuralNet()
MNN.setup_neural_network()

questionvars = ['0'] * 70
questionlabels = database.getQuestionnaire()
questionArray = ['0'] * 70
#The House Application 
class HouseApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        #set the font of the titles
        self.title_font = tkfont.Font(family='Times New Roman', size=22, weight="bold")
        self.label_font = tkfont.Font(family='Arial', size=12, weight="bold")
        self.geometry("600x475-500+50")
        #background color
        self.configure(background="#74caf9")
        #adds favicon
        self.iconbitmap('images\\favicon.ico')
        #disables resizing the window size
        self.resizable (False, False)
        #container of frames
        container = tk.Frame(self)
        #title of the application
        self.title('House Medical Application')
        #pack the container with the frames
        container.pack(side="top", fill="both", expand=False)
        #set the size of the rows and columns
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #a tuple of frames
        self.frames = {}
        
        for F in (registerPage.Register, login.Login, Forgot, mainPage.MainPage, QuestionPage, labPage.LabPage, 
                  imageProcessingUI.ImagePage, resultsPage.ResultsPage, adminMainPage.AdminMainPage):
            
            pageName = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[pageName] = frame           
            frame.grid(row=0, column=0, sticky="nsew")
        if (database.checkForUser() == 0):
            self.show_frame("Register")
        else:
            self.show_frame("Login")

    def show_frame(self, pageName):
        '''Show a frame for the given page name'''
        frame = self.frames[pageName]
        frame.tkraise()

#new page
class Forgot(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#74caf9")
        
        #page title
#        label = tk.Label(self, bg='#74caf9', text="Forgot Password", font=controller.title_font)
#        label.grid(row=1, columnspan=4, pady=10, padx=200)
        #pic title
        image = Image.open('images\\forgot.png')
        photo = ImageTk.PhotoImage(image)
        self.photolabel = tk.Label(self, image=photo, bg='#74caf9')
        self.photolabel.image = photo 
        self.photolabel.grid(row=0, columnspan=4, pady=10, padx=50)
        #username label
        userL = tk.Label(self, bg='#74caf9', text='Username: ', font=controller.label_font).grid(row=2, 
                        column=0, pady=10, padx=100)
        #username text box
        userN = tk.Entry(self)
        userN.grid(row=2, column=0, sticky=tk.E)
        #security question
        secL = tk.Label(self, bg='#74caf9', text='Security Question: \nWhat course is this application for?', 
                        font=controller.label_font).grid(row=3, columnspan=3, padx=100)
        #answer label
        answerL = tk.Label(self, bg='#74caf9', text='Answer: ',
                           font=controller.label_font).grid(row=4, column=0, pady=10, padx=100)
        #answer text box
        answerE = tk.Entry(self)
        answerE.grid(row=4, column=0, sticky=tk.E)
        #new passwword label
        self.newPwordL = tk.Label(self, bg='#74caf9', text='New Password: ',
                                  font=controller.label_font).grid(row=5, 
                                                            column=0, pady=10, padx=100)
        #newpassword text box
        newPassword = tk.Entry(self, show='*') 
        newPassword.grid(row=5, column=0, sticky=tk.E)
        #confirm newpassword label
        self.confirmPwordL = tk.Label(self, bg='#74caf9', text='Confirm Password: ',
                                      font=controller.label_font).grid(row=6, 
                                                                column=0, pady=10, padx=100)
        #confirm newpassword text box
        confirmPassword = tk.Entry(self, show='*') 
        confirmPassword.grid(row=6, column=0, sticky=tk.E)
        sec_questionstr="What course is this application for?"
        #submit button
        submitB = tk.Button(self, text="Submit", bg="#0759a5", fg="#ffffff", width=15, font=controller.label_font,
                           command=lambda: Forgot.forgotPass(userN.get(),newPassword.get(), 
                            confirmPassword.get(),answerE.get(),controller))
        submitB.grid(row=7, columnspan=4, pady=10, padx=200)
        backB = tk.Button(self, text="Back to Login", bg="#0759a5", fg="#ffffff", width=15, font=controller.label_font,
                           command=lambda: self.controller.show_frame("Login"))
        backB.grid(row=7, column = 1)
        
    def forgotPass(user, newPass, confirmPass, secAns, controller):
        if(newPass == confirmPass):
            database.resetPass(str(user), str(newPass), str(secAns))
            controller.show_frame("Login")
        else:

            tk.messagebox.showerror('Error', 'The passwords do not match!')

#newpage
class QuestionPage(tk.Frame):
    
    def __init__(self, parent, controller):
        q_list = [0,2,3,51,54,60]
        tk.Frame.__init__(self, parent)
        self.configure(background="#74caf9")
        
        self.canvas = tk.Canvas(self, borderwidth=0,highlightthickness=0, background="#74caf9", height=270)
        self.frame = tk.Frame(self.canvas, background="#74caf9")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        
        self.canvas.grid(row=1,column=0)
        self.vsb.grid(row=1,column=2, sticky="ns")
        self.canvas.create_window((50,3), window=self.frame, anchor="nw", tags="self.frame") 

        #page title
#        resultsLabel = tk.Label(self, text ="Questionnaire", bg='#74caf9', font=controller.title_font)
#        resultsLabel.grid(row=0, columnspan=3, pady=10, padx=200)
        #pic title
        image = Image.open('images\\question.png')
        photo = ImageTk.PhotoImage(image)
        self.photolabel = tk.Label(self, image=photo, bg='#74caf9')
        self.photolabel.image = photo 
        self.photolabel.grid(row=0, columnspan=4, pady=10, padx=50)
        
        self.canvas.grid(row=1,column=0)
        self.vsb.grid(row=1,column=2, sticky="ns")
        self.canvas.create_window((50, 3), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        for i in range(0,69):
                question = ["Age (yr.)","Sex", "Weight(lb.)", "Height(in.)", "Diet", "Prior Heart Attack",
                "Irregular Heartbeat", "Valvular Murmurs", "Device implantation", "Congestive Heart Failure",
                "Coronary Artery Disease", "Cancer", "Hepatitis", "Rheumatic Fever","Asthma", "Emphysema",
                "C.O.P.D.", "TIA or Stroke", "Arthritis", "Deep Vein Thrombosis", "Kidney/Bladder Problems",
                "Chronic Cough", "Hypercholesterolemia", "Hypertension", "GERD (heartburn)", "Diabetes Mellitus",
                "Crohn’s Disease", "Irritable Bowel Syndrome", "Osteoporosis", "Sleep Apnea", "Pedal Edema",
                "Anemia", "Appendectomy", "Bowel Resection", "Cholecystectomy", "Colonoscopy", "Vascular Surgery",
                "Catheterizations", "Orthopedic Surgery", "Heart Attack before age 55", "Arthritis",
                "Muscle or Nerve Disease", "Diabetes Mellitus", "Seizures", "Difficulty Speaking", "Stomach Pain",
                "Back Pain", "Headaches", "Chest pain", "Is Chest Pain Exertional", "Is Chest Pain Radiate",
                "Pain Duration (hours)", "Lightheaded from the pain", "Do you experience nausea",
                "Rate the severity of this pain:", "Dizziness", "Fainting Spells", "Constipation, or Diarrhea",
                "Nausea or Indigestion", "Do you currently Smoke", "How many packs per day?",
                "History of Illicit drug use?", "Previous Motor Accident?","Urinary Symptoms",
                "Weakness or Numbness", "Loss of vision or dimming", "Difficulty/Loss of speech", 
                "Sudden, severe headache", "Loss of balance"]

                label = tk.Label(self.frame, text="%s" %question[i], width=22, bg="#74caf9")
                label.grid(row=(i+1), column=0, sticky=tk.E)
                questionvars[i] = tk.StringVar(value='0')
                if i in q_list:
                    entry1 = tk.Entry(self.frame, textvariable=questionvars[i])
                    entry1.grid(row=(i+1), column=2, sticky=tk.E)
                else:
                    if(i == 1):
                        entry1 = tk.Radiobutton(self.frame, text='Male', 
                                                variable=questionvars[i], value='0', bg="#74caf9")
                        entry1.grid(row=(i+1), column=1)
                        entry2 = tk.Radiobutton(self.frame, text='Female', 
                                                variable=questionvars[i], value='1', bg="#74caf9")
                        entry2.grid(row=(i+1), column=2)
                    else:
                        entry1 = tk.Radiobutton(self.frame, text='No', 
                                                variable=questionvars[i], value='0', bg="#74caf9")
                        entry1.grid(row=(i+1), column=1)
                        entry2 = tk.Radiobutton(self.frame, text='Yes', 
                                                variable=questionvars[i], value='1', bg="#74caf9")
                        entry2.grid(row=(i+1), column=2)
                    
        #button back to the main page        
        mainB = tk.Button(self, text="Back", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: controller.show_frame("MainPage"))
        mainB.grid(row=80, column=0, pady=10)
        #button to next page (Labs)
        nextB = tk.Button(self, text="Next", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: QuestionPage.toLabs(self, controller))
        nextB.grid(row=80, column=1, pady=10)        

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def toLabs(self, controller):
        for i in range(0,70):
            if(i<4):
                questionArray[i] = questionvars[i].get()
                if (questionArray[i]==''):
                    tkinter.messagebox.showerror('Error', 'Values cannot be empty.')
                    return 0
            if(i==4):
                if (int(questionArray[2])==0):
                    tkinter.messagebox.showerror('Error', 'Weight cannot be zero.')
                    return 0
                elif (int(questionArray[3])==0):
                    tkinter.messagebox.showerror('Error', 'Height cannot be zero.')
                    return 0
                else:
                    questionArray[4] = int(questionArray[2])/int(questionArray[3])


            if(i>4):
                questionArray[i] = questionvars[i-1].get()
                if (questionArray[i]==''):
                    tkinter.messagebox.showerror('Error', 'Values cannot be empty.')
                    return 0

        #print(questionArray)
        resultsPage.ResultsPage.qVariables = questionArray
        #print(resultsPage.ResultsPage.qVariables)
        controller.show_frame("LabPage")
    def mainPage(self, controller):
        print(login.Login.accessLevel)
        if(login.Login.accessLevel == "admin"):
            controller.show_frame("AdminMainPage")
        elif(login.Login.accessLevel == "User"):
            controller.show_frame("MainPage")

if __name__ == "__main__":
    
    app = HouseApp()
    app.mainloop()
    