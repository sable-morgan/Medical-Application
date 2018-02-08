# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 23:07:37 2017

@author: Norvell
"""

import tkinter as tk
import script
import neuralNetwork, imagingNeuralNetwork, brainNeuralNetwork, spineNeuralNetwork, maskNeuralNetwork
import houseDB
from tkinter import ttk, PhotoImage
from PIL import ImageTk,Image
import tkinter.messagebox
from tkinter import font  as tkfont
database = houseDB.HouseDB()
class AdminMainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global result
        result = ""
        self.controller = controller
        self.configure(background="#74caf9")
        #set the font of the titles
        self.title_font = tkfont.Font(family='Times New Roman', size=22, weight="bold")
        self.label_font = tkfont.Font(family='Arial', size=12, weight="bold")
        #title    
#        label = tk.Label(self, bg="#74caf9", text="Administration Dashboard", font=controller.title_font)
#        label.grid(row=0, columnspan=3, pady=10)
        #pic title
        image = Image.open('images\\admin.png')
        photo = ImageTk.PhotoImage(image)
        self.photolabel = tk.Label(self, image=photo, bg='#74caf9')
        self.photolabel.image = photo 
        self.photolabel.grid(row=0, columnspan=3, pady=10, padx=50)

        #search button that triggers search_profiles function
        searchLabel = tk.Label(self, bg="#74caf9", text ="Search by ID: ", font=controller.label_font)
        searchLabel.grid(row=1, column=0, pady=5, padx=250)
        #text to be searched by search_profiles function
        searchEntry = tk.Entry(self, width=20)
        searchEntry.grid(row=2, column=0, pady=5, padx=250)
        
        searchB = tk.Button(self, text="Search", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: self.searchProfiles(searchEntry.get()))
        searchB.grid()

        #create button that triggers create_new function
        createLabel = tk.Label(self, bg="#74caf9", text ="Create a profile page" , font=controller.label_font)
        createLabel.grid()

        createB = tk.Button(self, text="Create", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: controller.show_frame("QuestionPage")) 
        createB.grid()
        
        logoutB = tk.Button(self, text="Logout", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: controller.show_frame("Login")) 
        logoutB.grid(pady = 5)
        
        # admin options
        adminLabel = tk.Label(self, bg="#74caf9", text ="Additional Options" , font=controller.label_font)
        adminLabel.grid(pady=10)
        
        updateButton = tk.Button(self, text="Update Neural Network", bg="#0759a5", fg="#ffffff", width=25,
                           command=lambda: self.updateNNPage())
        updateButton.grid(pady=5)
        
        userButton = tk.Button(self, text="User Options", bg="#0759a5", fg="#ffffff", width=25,
                           command=lambda: self.userPage())
        userButton.grid()
    
    def updateNNPage(self):
        self.update = tk.Tk()         
        self.update.title('Update Neural Network')
        self.update.geometry('650x350-400+50')
        self.update.configure(background="#74caf9")
        self.update.iconbitmap('images\\favicon.ico')
        self.update.grid()
        
        global result      
        
        #pic title
        image = Image.open('images\\admin.png')
        photo = ImageTk.PhotoImage(image)
        self.photolabel = tk.Label(self, image=photo, bg='#74caf9')
        self.photolabel.image = photo 
        self.photolabel.grid(row=0, columnspan=3, pady=10, padx=50)
        
        updateLabel = tk.Label(self.updatePage, text="Update Neural Network Page", font="-size 22", bg="#74caf9")
        updateLabel.grid(row=0, columnspan=3, pady=10, padx=100)

        updateNNButton = tk.Button(self.updatePage, text="Update Diagnosis", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: self.updateNN()) 
        updateNNButton.grid(row=6, column=0, columnspan=1)
        
        updateImagingButton = tk.Button(self.updatePage, text="Update Imaging NN", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: self.updateImaging()) 
        updateImagingButton.grid(row=6, column=1, columnspan=1)
        updateBrainButton = tk.Button(self.updatePage, text="Update Brain NN", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: self.updateBrain()) 
        updateBrainButton.grid(row=7, column=1, pady=5, columnspan=1)
        updateSpineButton = tk.Button(self.updatePage, text="Update Spine NN", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: self.updateSpine()) 
        updateSpineButton.grid(row=8, column=1, columnspan=1)
        updateMaskButton = tk.Button(self.updatePage, text="Update Mask NN", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: self.updateMask()) 
        updateMaskButton.grid(row=9, column=1, pady=5, columnspan=1)
        
        
        updateAllButton = tk.Button(self.updatePage, text="Update All", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: self.updateAll()) 
        updateAllButton.grid(row=6, column=2, columnspan=1)
        
    def updateNN(self):
        
        script.diag.train_neural_network()
        
        testNNacc, testNNmatrix = script.diag.test_neural_network()
        testNNLabel1 = tk.Label(self.updatePage, text=testNNacc, font="-size 10", bg="#74caf9")
        testNNLabel1.grid(row=9, pady=10, padx=50)
        testNNLabel2 = tk.Label(self.updatePage, text=testNNmatrix, font="-size 10", bg="#74caf9")
        testNNLabel2.grid(row=12, pady=10)
    
    def updateMask(self):
        #resultsLabel = tk.Label(self.update, text="Updating Please Wait...", font="-size 20", bg="#74caf9")
        #resultsLabel.grid(row=7, columnspan=3, pady=10, padx=50)
        script.MNN.train_neural_network()
        trainMask = "Tumor Neural Net:"
        trainMaskLabel = tk.Label(self.updatePage, text=trainMask, font="-size 10", bg="#74caf9")
        trainMaskLabel.grid(row=23, pady=10, padx=50)
        
        testMaskacc, testMaskmatrix = script.MNN.test_neural_network()
        testMaskLabel1 = tk.Label(self.updatePage, text=testMaskacc, font="-size 10", bg="#74caf9")
        testMaskLabel1.grid(row=24, rowspan=3, pady=10, padx=50)
        testMaskLabel2 = tk.Label(self.updatePage, text=testMaskmatrix, font="-size 10", bg="#74caf9")
        testMaskLabel2.grid(row=25, rowspan=3, pady=10, padx=50)
    def updateImaging(self):
        #resultsLabel = tk.Label(self.update, text="Updating Please Wait...", font="-size 20", bg="#74caf9")
        #resultsLabel.grid(row=7, columnspan=3, pady=10, padx=50)
        
        script.INN.train_neural_network()
        trainImaging = "Imaging Neural Net:"
        trainImagingLabel = tk.Label(self.updatePage, text=trainImaging, font="-size 10", bg="#74caf9")
        trainImagingLabel.grid(row=8, pady=10, padx=50)
        
        testImagingacc, testImagingmatrix = script.INN.test_neural_network()
        testImagingLabel1 = tk.Label(self.updatePage, text=testImagingacc, font="-size 10", bg="#74caf9")
        testImagingLabel1.grid(row=9, rowspan=4, pady=10, padx=50)
        testImagingLabel2 = tk.Label(self.updatePage, text=testImagingmatrix, font="-size 10", bg="#74caf9")
        testImagingLabel2.grid(row=10, rowspan=4, pady=10, padx=50)
    def updateBrain(self):
        #resultsLabel = tk.Label(self.update, text="Updating Please Wait...", font="-size 20", bg="#74caf9")
        #resultsLabel.grid(row=7, columnspan=3, pady=10, padx=50)
        
        
        script.BNN.train_neural_network()
        trainBrain = "Brain Neural Net:"
        trainBrainLabel = tk.Label(self.updatePage, text=trainBrain, font="-size 10", bg="#74caf9")
        trainBrainLabel.grid(row=12, pady=10, padx=50)
        
        testBrainacc,testBrainmatrix = script.BNN.test_neural_network()
        testBrainLabel = tk.Label(self.updatePage, text=testBrainacc, font="-size 10", bg="#74caf9")
        testBrainLabel.grid(row=13, rowspan=6, pady=10, padx=50)
        testBrainLabel = tk.Label(self.updatePage, text=testBrainacc, font="-size 10", bg="#74caf9")
        testBrainLabel.grid(row=14, rowspan=6, pady=10, padx=50)
    def updateSpine(self):
        #resultsLabel = tk.Label(self.update, text="Updating Please Wait...", font="-size 20", bg="#74caf9")
        #resultsLabel.grid(row=7, columnspan=3, pady=10, padx=50)
        #script.SNN.train_neural_network()
        trainSpine = "Spine Neural Net:"
        trainSpineLabel = tk.Label(self.updatePage, text=trainSpine, font="-size 10", bg="#74caf9")
        trainSpineLabel.grid(row=19, column=1, pady=10, padx=50)
        
        testSpineacc, testSpinematrix = script.SNN.test_neural_network()
        testSpineLabel1 = tk.Label(self.updatePage, text=testSpineacc, font="-size 10", bg="#74caf9")
        testSpineLabel1.grid(row=20, column=1, pady=10, padx=50)
        testSpineLabel2 = tk.Label(self.updatePage, text=testSpinematrix, font="-size 10", bg="#74caf9")
        testSpineLabel2.grid(row=21, column=1, padx=50)
    def updateAll(self):
        AdminMainPage.updateNN()
        AdminMainPage.updateImaging()
        AdminMainPage.updateBrain()
        AdminMainPage.updateSpine()
        AdminMainPage.updateMask()
    
    def userPage(self):
        userManagement = tk.Tk()
        userManagement.title('User Management')
        userManagement.geometry('600x300-500+50')
        userManagement.configure(background="#74caf9")
        userManagement.iconbitmap('images\\favicon.ico')
        userManagement.grid()
        
        label = tk.Label(userManagement,bg='#74caf9', text="User Management Page", font="-size 30")
        label.grid(row=1, columnspan=3, pady=20, padx=50, sticky=tk.E)
        
        createUserButton = tk.Button(userManagement, text="Create New User", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: self.createNewUser()) 
        createUserButton.grid(row=6, column=1, columnspan=1)
        
        deleteUserButton = tk.Button(userManagement, text="Delete User", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: self.deleteUser()) 
        deleteUserButton.grid(row=6, column=2, columnspan=1)
        
    def createNewUser(self):
        self.userManagement = tk.Tk()         
        self.userManagement.title('Create New User')
        self.userManagement.geometry('600x400-500+50')
        self.userManagement.configure(background="#74caf9")
        self.userManagement.iconbitmap('images\\favicon.ico')
        self.userManagement.grid()
    
        label = tk.Label(self.userManagement,bg='#74caf9', text="Add New User", font="-size 30")
        label.grid(row=1, columnspan=3, pady=20, padx=100, sticky=tk.E)
        
        #username label and input
        newUserLabel = tk.Label(self.userManagement,fg='#000000',bg='#74caf9', text='New Username: ')
        newUserLabel.grid(row=2, column=1, pady=10)
        newUserName = tk.Entry(self.userManagement)
        newUserName.grid(row=2, column=2)
        
        #password label and unput
        newPwordLabel = tk.Label(self.userManagement,fg='#000000',bg='#74caf9', text='New Password: ')
        newPwordLabel.grid(row=3, column=1, pady=10)
        newPassword = tk.Entry(self.userManagement, show='*') 
        newPassword.grid(row=3, column=2)

        confirmPwordLabel = tk.Label(self.userManagement,fg='#000000',bg='#74caf9', text='Confirm Password: ')
        confirmPwordLabel.grid(row=4, column=1, pady=10)
        confirmPassword = tk.Entry(self.userManagement, show='*') 
        confirmPassword.grid(row=4, column=2)
        
        sec_questionstr="What course is this application for?"
        secLabel = tk.Label(self.userManagement,fg='#000000',bg='#74caf9', text='Security Question: \nWhat course is this application for?')
        secLabel.grid(row=5, column=1, pady=10, padx=10)
        
        answerLabel = tk.Label(self.userManagement,fg='#000000',bg='#74caf9', text='Answer: ')
        answerLabel.grid(row=6, column=1, pady=10)
        answerE = tk.Entry(self.userManagement)
        answerE.grid(row=6, column=2)
        
        self.accessV = tk.StringVar(self.userManagement, value = 'User')
        entry1 = tk.Radiobutton(self.userManagement, text="Admin", variable=self.accessV, value='admin', bg="#74caf9")
        entry1.grid(row=7, column=1)
        entry2 = tk.Radiobutton(self.userManagement, text='User', variable=self.accessV, value='User', bg="#74caf9")
        entry2.grid(row=7, column=2)
        
        signupButton = tk.Button(self.userManagement, text='Submit', bg="#0759a5", fg="#ffffff",
        command=lambda: self.writeToDB(newUserName.get(),newPassword.get(), confirmPassword.get(), sec_questionstr,answerE.get(), self.accessV.get()))
        signupButton.grid(row=8, columnspan=3, pady=20, padx=20)
        
    def writeToDB(self, user,password, confirm, sec_ques,sec_ans, access):
        if(password == confirm):    
            script.database.writeUser(user,password,sec_ques,sec_ans, access)
            tk.messagebox.showinfo('Success', 'The new user has been added')
            self.userManagement.destroy()
        else:
            tk.messagebox.showerror('Error', 'The passwords do not match!')
        
    def deleteUser(self):
        self.userManagement = tk.Tk()         
        self.userManagement.title('Delete User')
        self.userManagement.geometry('600x300-500+50')
        self.userManagement.configure(background="#74caf9")
        self.userManagement.iconbitmap('images\\favicon.ico')
        self.userManagement.grid()
    
        label = tk.Label(self.userManagement,bg='#74caf9', text="Remove User", font="-size 30")
        label.grid(row=1, columnspan=3, pady=20, padx=100, sticky=tk.E)
        
        #username label and input
        userNameL = tk.Label(self.userManagement,fg='#000000',bg='#74caf9', text='Username: ')
        userNameL.grid(row=2, column=0, pady=10, sticky=tk.E)
        userName = tk.Entry(self.userManagement)
        userName.grid(row=2, column=1, sticky=tk.E)
        
        confirmUserNameL = tk.Label(self.userManagement,fg='#000000',bg='#74caf9', text='Confirm Username: ')
        confirmUserNameL.grid(row=3, column=0, pady=10, sticky=tk.E)
        confirmUserName = tk.Entry(self.userManagement)
        confirmUserName.grid(row=3, column=1, sticky=tk.E)
        
        deleteButton = tk.Button(self.userManagement, text='Submit', bg="#0759a5", fg="#ffffff",
        command=lambda: self.deleteFromDB(userName.get(), confirmUserName.get()))
        deleteButton.grid(row=4, columnspan=3, pady=20, padx=10)
        
    def deleteFromDB(self, user, confirmUser):
        if(user == confirmUser):
            script.database.deleteUser(user)
            tk.messagebox.showinfo('Success', 'The user has been deleted')
            self.userManagement.destroy()
        else:
            tk.messagebox.showerror('Error', 'The usernames do not match!')
        
    def searchProfiles(self, pid):
        profileArr = script.database.searchDB(pid)
        profileArr = profileArr.tolist()
        print(profileArr)
        patientprofilewindow = AdminMainPage.profileWindow(profileArr)
    
        print("This will call the search page")

# Creates new profile sends user to questionaire page 
    def profileWindow(profilearray):
        patient = tk.Tk()         
        patient.title('Patient Profile')
        patient.geometry('600x600-500+50')
        patient.configure(background="#74caf9")
        patient.grid()
        patientIDstr = "PatientID: {}".format(profilearray[0])
        IDLabel = tk.Label(patient, text =patientIDstr, font="Helvetica 14 bold", bg="#74caf9")
        IDLabel.grid(row=0, column=0, columnspan=3)
        questionList = ["Age","Sex", "Weight", "Height", "Diet", "Prior Heart Attack",
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
                "Sudden, severe headache", "Loss of balance", "Blood Pressure: ", "Specific Gravity: ",
                "Albumin: ", "Sugar Rating: ", "Red Blood Cells: ", "Pus Levels: ", "Pus Clump: ", "Bacteria Levels: ",
                "Blood Glucose Levels: ", "Blood Urea Level: ", "Creatinine: ", "Sodium: ", "Potassium: ", "Hemoglobin: ",
                "Cell Volume: ", "White Blood Cell Count: ", "Red Blood Cell Count: ", "Herniated Disc: ", "Brain Tumor: "]

        geninfostr = "General Information"
        IDLabel = tk.Label(patient, text =geninfostr, font="Helvetica 12 bold", bg="#74caf9")
        IDLabel.grid(row=1, column=0, columnspan=4, padx=30, sticky= tk.W)
        
        agestr = "Age: {}".format(profilearray[1])
        ageLabel = tk.Label(patient, text =agestr,font="-size 10", bg="#74caf9")
        ageLabel.grid(row=2, column=0, padx=30, sticky= tk.W)
        
        weightstr = "Weight: {}".format(profilearray[2])
        weightLabel = tk.Label(patient, text =weightstr, font="-size 10", bg="#74caf9")
        weightLabel.grid(row=3, column=0, padx=30, sticky= tk.W) 
        
        heightstr = "Height: {}".format(profilearray[3])
        heightLabel = tk.Label(patient, text =heightstr, font="-size 10", bg="#74caf9")
        heightLabel.grid(row=4, column=0, padx=30, sticky= tk.W)
        
        bmistr = "BMI: {}".format(profilearray[4])
        bmiLabel = tk.Label(patient, text =bmistr, font="-size 10", bg="#74caf9")
        bmiLabel.grid(row=5, column=0, padx=30, sticky= tk.W)
        
        if(profilearray[5] == '0'):
            appstr = "Appetite: Good"
        else:
            appstr = "Appetite: Poor"
        appLabel = tk.Label(patient, text =appstr, font="-size 10", bg="#74caf9")
        appLabel.grid(row=6, column=0, padx=30, sticky= tk.W)
        #columns = neuralNetwork.database.getCols()
        label = [None] * 100
        rownum = 2
        
        medstr = "Medical History"
        IDLabel = tk.Label(patient, text =medstr, font="Helvetica 12 bold", bg="#74caf9")
        IDLabel.grid(row=1, column=6, sticky= tk.W)
        for i in range(7,71):
            if(profilearray[i] == '0'):
                #do nothing
                continue
            else:
                label[i] = tk.Label(patient, text =questionList[i-2], font="-size 10", bg="#74caf9")
                label[i].grid(row=rownum, column=6, sticky= tk.W)
                rownum = rownum+1
            
        labstr = "Lab Results"
        labLabel = tk.Label(patient, text =labstr, font="Helvetica 12 bold", bg="#74caf9")
        labLabel.grid(row=1, column=12, padx=30, sticky= tk.W)
        rownum = 2
        for i in range(71,90):
            if(i in [75,76,77,78]):
                if(profilearray[i] == '0'):
                    profilearray[i] = 'Normal'
            
            PHstr = "{}{}".format(questionList[i-2],profilearray[i])
            if(questionList[i-2] == "Red Blood Cell Count: "):
                PHstr = "{}{} million".format(questionList[i-2],profilearray[i])
            if(questionList[i-2] == "Herniated Disc: "):
                PHstr = "{}{}%".format(questionList[i-2],profilearray[i])
            if(questionList[i-2] == "Brain Tumor: "):
                PHstr = "{}{}%".format(questionList[i-2],profilearray[i])
            label[i] = tk.Label(patient, text =PHstr, font="-size 10", bg="#74caf9")
            label[i].grid(row=rownum, column=12, padx=30, sticky=tk.W)
            rownum = rownum+1
        if((profilearray[90] == '0') or (profilearray[90] == '0.0')):
            profilearray[90] = 'No condition'
        if((profilearray[90] == '1') or (profilearray[90] == '1.0')):
            profilearray[90] = 'Kidney Disease'
        if((profilearray[90] == '2') or (profilearray[90] == '2.0')):
            profilearray[90] = 'Herniated Disc'
        if((profilearray[90] == '3') or (profilearray[90] == '3.0')):
            profilearray[90] = 'Brain Tumor'
        PHstr = "Diagnosis: {}".format(profilearray[90])
        label[90] = tk.Label(patient, text =PHstr, font="Helvetica 14 bold", bg="#74caf9")
        label[90].grid(row=0, column=6,columnspan=10, sticky=tk.W)
