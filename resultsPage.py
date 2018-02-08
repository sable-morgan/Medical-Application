import tkinter as tk
import script
import neuralNetwork
import imageProcessingUI
import labPage
import login
import os
from PIL import Image, ImageTk
#new page        

tumorDetected = 0

imageName = "String"
class ResultsPage(tk.Frame):
    qVariables = []
    lVariables = []
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#74caf9")
        #page title
        resultsLabel = tk.Label(self, text ="The Results", bg="#74caf9", font=self.controller.title_font)
        resultsLabel.grid(row=0, columnspan=3, pady=10, padx=200)
        #pic title
        image = Image.open('images\\diagnosis.png')
        photo = ImageTk.PhotoImage(image)
        self.photolabel = tk.Label(self, image=photo, bg='#74caf9')
        self.photolabel.image = photo 
        self.photolabel.grid(row=0, columnspan=4, pady=10, padx=50)        
        #id number here
        self.idLabel = tk.Label(self, text ="Patient ID: ",bg="#74caf9", font=self.controller.label_font)
        self.idLabel.grid(row=1, columnspan=3, pady=10, padx=50)
        
        #the diagonsis here
        self.diaLabel = tk.Label(self, text ="N/A",  bg="#74caf9",  font=self.controller.label_font)
        self.diaLabel.grid(row=2, columnspan=3, pady=10, padx=50)
        
        #image name and/or view
        self.imgLabel = tk.Label(self, text ="No Image Uploaded", bg="#74caf9", font=self.controller.label_font)
        self.idLabel = tk.Label(self, text ="Patient ID: ",  bg="#74caf9", font=self.controller.label_font)
        self.idLabel.grid(row=1, columnspan=3, pady=10, padx=50)
        
        #the diagonsis here
        self.diaLabel = tk.Label(self, text ="N/A",  bg="#74caf9",  font=self.controller.label_font)
        self.diaLabel.grid(row=2, columnspan=3, pady=10, padx=50)
        
        #image name and/or view
        self.imgLabel = tk.Label(self, text ="No Image Uploaded", bg="#74caf9", font=self.controller.label_font)
        self.imgLabel.grid(row=3, columnspan=3, pady=10, padx=50)
        
        
        self.photolabel = tk.Label(self, text="", bg='#74caf9')
        self.photolabel.grid(row=6, column=0,padx=10)
        #calculate button
        self.calcButn = tk.Button(self, text = "Calculate Diagnosis",  bg="#0759a5", fg="#ffffff", command=lambda: self.results())
        self.calcButn.grid(row=4, column=1, pady=10)
        self.grid() 
        
    def results(self):
        #print(ResultsPage.qVariables)
        #print(ResultsPage.lVariables)
        
        variables = ResultsPage.qVariables+ResultsPage.lVariables
        print(variables)
        finalDiag = script.diag.predict_neural_network(variables)
        self.calcButn.grid_forget()
        self.idLabel.grid_forget()
        self.idLabel = tk.Label(self, text ="Patient ID: "+script.diag.pid[0],  bg="#74caf9", font=self.controller.label_font)
        self.idLabel.grid(row=1, columnspan=3, pady=10, padx=50)
        self.imgLabel.grid_forget()
        self.diaLabel = tk.Label(self, text =finalDiag,  bg="#74caf9", font=self.controller.label_font)
        self.diaLabel.grid(row=2, columnspan=3, pady=10, padx=25)
        #Backhead brain tumor detection 

        if(imageProcessingUI.ImagePage.firstLayer == 3):
            if(variables[len(variables)-2] == '0'):
                self.imgLabel = tk.Label(self, text ="No Image Uploaded",  bg="#74caf9", font=self.controller.label_font)
                self.imgLabel.grid(row=3, columnspan=3, pady=10, padx=50)
        if(imageProcessingUI.ImagePage.firstLayer == 1):
            imagestr = imageProcessingUI.ImagePage.imagestr
            image = Image.open(imagestr)
            image = image.resize((200, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            #Backhead brain tumor detection 

            self.photolabel = tk.Label(self, image=photo, bg='#74caf9')

            self.photolabel.image = photo 
            self.photolabel.grid(row=5, column=1)
            if(imageProcessingUI.ImagePage.secondLayer == 1):
                self.imgLabel = tk.Label(self, text ="Spine: Healthy",  bg='#74caf9', font=self.controller.label_font)
                self.imgLabel.grid(row=3, columnspan=3, pady=10, padx=50)
            elif(imageProcessingUI.ImagePage.secondLayer == 0):
                self.imgLabel = tk.Label(self, text ="Spine: Herniated Disc detected",  bg='#74caf9', font=self.controller.label_font)
                self.imgLabel.grid(row=3, columnspan=3, pady=10, padx=50)
        if(imageProcessingUI.ImagePage.firstLayer == 0):
            imagestr = "{}_segmentation.png".format(os.path.splitext(imageProcessingUI.ImagePage.imagestr)[0])
            image = Image.open(imagestr)
            image = image.resize((200, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            #Backhead brain tumor detection 

            self.photolabel = tk.Label(self, image=photo, bg='#74caf9')

            self.photolabel.image = photo 
            self.photolabel.grid(row=5, column=1)
            if(imageProcessingUI.ImagePage.secondLayer == 0):
                brainstr = "Coronal Brain Scan: "
            elif(imageProcessingUI.ImagePage.secondLayer == 1):
                brainstr = "Sagittal Brain Scan: "
            elif(imageProcessingUI.ImagePage.secondLayer == 2):
                brainstr = "Axial Brain Scan: "
            if(imageProcessingUI.ImagePage.image_reco == 0):
                brainstr = brainstr + "Healthy"
                self.imgLabel = tk.Label(self, text =brainstr,  bg='#74caf9', font=("Helvetica", 10))
                self.imgLabel.grid(row=3, columnspan=3, pady=10, padx=50)
            elif(imageProcessingUI.ImagePage.image_reco == 1):
                brainstr = brainstr + "Tumor Detected"
                self.imgLabel = tk.Label(self, text =brainstr,  bg='#74caf9', font=("Helvetica", 10))
                self.imgLabel.grid(row=3, columnspan=3, pady=10, padx=50)
        
        self.approveButn = tk.Button(self, width=10, text = "Approve",  bg="#0759a5", fg="#ffffff", command=lambda: self.approve((neuralNetwork.NeuralNet.pid+self.qVariables), (neuralNetwork.NeuralNet.pid+self.lVariables), (neuralNetwork.NeuralNet.pid+neuralNetwork.NeuralNet.diag)))
        self.approveButn.grid(row=5, column=0, padx=10)
        
        self.denyButn = tk.Button(self, width=10, text = "Deny",  bg="#0759a5", fg="#ffffff", command=lambda: self.deny((neuralNetwork.NeuralNet.pid+self.qVariables), (neuralNetwork.NeuralNet.pid+self.lVariables), (neuralNetwork.NeuralNet.pid+neuralNetwork.NeuralNet.diag)))
        self.denyButn.grid(row=5, column=2)
        
        
#approve diagnosis    
    def approve(self, qArray, lArray, dArray):
        self.idLabel.grid_forget()
        self.imgLabel.grid_forget()
        self.diaLabel.grid_forget()
        self.photolabel.grid_forget()
        self.approveButn.grid_forget()
        self.denyButn.grid_forget()
        self.idLabel = tk.Label(self, text ="Patient ID: ",  bg="#74caf9", font=self.controller.label_font)
        self.idLabel.grid(row=1, columnspan=3, pady=10, padx=50)
        self.diaLabel = tk.Label(self, text ="N/A",  bg="#74caf9",  font=self.controller.label_font)
        self.diaLabel.grid(row=2, columnspan=3, pady=10, padx=50)
        self.imgLabel = tk.Label(self, text ="No Image Uploaded", bg="#74caf9", font=self.controller.label_font)
        self.imgLabel.grid(row=3, columnspan=3, pady=10, padx=50)
        self.photolabel = tk.Label(self, text="", bg='#74caf9')
        self.photolabel.grid(row=6, column=0,padx=10)
        self.calcButn = tk.Button(self, text = "Calculate Diagnosis",  bg="#0759a5", fg="#ffffff", command=lambda: self.results())
        self.calcButn.grid(row=4, column=1, pady=10)
        imageProcessingUI.ImagePage.imageArgs = ['0']*19
        imageProcessingUI.ImagePage.firstLayer = 3
        imageProcessingUI.ImagePage.secondLayer = 0
        imageProcessingUI.ImagePage.image_reco = 2
        imageProcessingUI.ImagePage.imagestr = ""
        self.qVariables = []
        self.lVariables = []
        labPage.LabPage.args = ['0'] * 19
#        print(qArray)
#        print(lArray)
#        print(dArray)
        neuralNetwork.database.writeDB(qArray, lArray, dArray)
        if(login.Login.accessLevel == "admin"):
            self.controller.show_frame("AdminMainPage")
        elif(login.Login.accessLevel == "User"):
            self.controller.show_frame("MainPage")

#deny diagnosis   
    def deny(self, qArray, lArray, dArray):
        self.idLabel.grid_forget()
        self.imgLabel.grid_forget()
        self.diaLabel.grid_forget()
        self.photolabel.grid_forget()
        self.approveButn.grid_forget()
        self.denyButn.grid_forget()
        self.idLabel = tk.Label(self, text ="Patient ID: ",  bg="#74caf9", font=self.controller.label_font)
        self.idLabel.grid(row=1, columnspan=3, pady=10, padx=50)
        self.diaLabel = tk.Label(self, text ="N/A",  bg="#74caf9",  font=self.controller.label_font)
        self.diaLabel.grid(row=2, columnspan=3, pady=10, padx=50)
        self.imgLabel = tk.Label(self, text ="No Image Uploaded", bg="#74caf9", font=self.controller.label_font)
        self.imgLabel.grid(row=3, columnspan=3, pady=10, padx=50)
        self.calcButn = tk.Button(self, text = "Calculate Diagnosis",  bg="#0759a5", fg="#ffffff", command=lambda: self.results())
        self.calcButn.grid(row=4, column=1, pady=10)
        self.photolabel = tk.Label(self, text="", bg='#74caf9')
        self.photolabel.grid(row=6, column=0,padx=10)
        
        imageProcessingUI.ImagePage.imageArgs = ['0']*19
        imageProcessingUI.ImagePage.firstLayer = 3
        imageProcessingUI.ImagePage.secondLayer = 0
        imageProcessingUI.ImagePage.image_reco = 2
        imageProcessingUI.ImagePage.imagestr = ""
        self.qVariables = []
        self.lVariables = []
        labPage.LabPage.args = ['0'] * 19
#        if(dArray[1] == '1'):
#            dArray[1] = '0'
#        else:
#            dArray[1] = '1'
#        database.writeDB(qArray, lArray, dArray)

        if(login.Login.accessLevel == "admin"):
            self.controller.show_frame("AdminMainPage")
        elif(login.Login.accessLevel == "User"):
            self.controller.show_frame("MainPage")