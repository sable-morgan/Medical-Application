import tkinter as tk
import labPage
import login
import script
import resultsPage
import topHead_Brain_tumorDetection
import backHead_Brain_tumorDetection
from tkinter import ttk, PhotoImage
from PIL import ImageTk,Image
import tkinter.messagebox
class ImagePage(tk.Frame):
    imageArgs = ['0']*19
    firstLayer = 3
    secondLayer = 0
    image_reco = 2
    imagestr = ""
    stats = ""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#74caf9")
        #background image
        self.grid()
        #page title    
#        label = tk.Label(self, bg='#74caf9', text="Image Processing", font=controller.title_font)
#        label.grid(row=0, columnspan=3, pady=10, padx=150)
        #pic title
        image = Image.open('images\\image.png')
        photo = ImageTk.PhotoImage(image)
        self.photolabel = tk.Label(self, image=photo, bg='#74caf9')
        self.photolabel.image = photo 
        self.photolabel.grid(row=0, columnspan=3, pady=10, padx=50)

        self.image_reco = 0
        self.upload_button = tk.Button(self, text="Upload...", width=10, bg="#0759a5", fg="#ffffff", command=self.upload, font=controller.label_font)
        self.upload_button.grid(row=1, columnspan=3, pady=10, padx=200)
        self.imagelabel = tk.Label(self, bg='#74caf9', text="", font=("Helvetica", 10))
        self.imagelabel.grid(row=4, columnspan=3)
        self.precisionLabel = tk.Label(self, bg='#74caf9', text="", font=("Arial", 10))
        self.precisionLabel.grid(row=5, column=0)
        #button to go back to the Labs page
        backButn = tk.Button(self, text = "Back", width=10, bg="#0759a5", fg="#ffffff", command=lambda: controller.show_frame("LabPage"))
        backButn.grid(row=3, column=0, pady=10, padx=10)
        #button to skip to the Image page
        skipButn = tk.Button(self, text = "Skip", width=10, bg="#0759a5", fg="#ffffff", command=lambda: self.skip())
        skipButn.grid(row=3, column=1, pady=10)
        #button to submit the vals go to the Image Page
        submitButn = tk.Button(self, text = "Diagnosis", width=10, bg="#0759a5", fg="#ffffff", command=lambda: self.toResults())
        submitButn.grid(row=3, column=2, pady=10)
    
    def skip(self):
        ImagePage.imageArgs[17] = '1'
        ImagePage.imageArgs[18] = '1'
        #print(ImagePage.imageArgs)
        self.imagelabel = tk.Label(self, bg='#11AAFF', text='', font=("Helvetica", 10))
        self.imagelabel.grid(row=4, columnspan=3)
        self.photolabel = tk.Label(self, text=' ', bg='#74caf9')
        self.photolabel.grid(row=5, column=1)
        self.toResults()
        #print(imageUI.variables)
        #print(len(imageUI.variables))

    def upload(self):
        #c = imageProccessing()
        ImagePage.imagestr = str(tk.filedialog.askopenfilename(initialdir = "E:/Images",title = "Choose an image",filetypes = (("PNG files","*.png"),("JPEG files","*.jpg"),("All files","*.*"))))
        filestr = ImagePage.imagestr
        self.imagelabel.grid_forget()
        self.imagelabel = tk.Label(self, bg='#74caf9', text=filestr, font=("Arial", 10))

        self.imagelabel.grid(row=4, columnspan=3)
        ImagePage.firstLayer = script.INN.predict_neural_network(ImagePage.imagestr)
        if (ImagePage.firstLayer==0):
            ImagePage.imageArgs[17] = '0'
            ImagePage.secondLayer = script.BNN.predict_neural_network(ImagePage.imagestr)
            if(ImagePage.secondLayer == 0):
                mask_image = backHead_Brain_tumorDetection.segmentTumourInFile(ImagePage.imagestr)
                ImagePage.image_reco, percentage = script.MNN.predict_neural_network(mask_image , 0)

                metrics = list(ImagePage.stats.values())
                precstr = "precision: {} \n recall: {} \n f-measure: {}".format(metrics[0],metrics[1],metrics[2])
                self.precisionLabel = tk.Label(self, bg='#74caf9', text=precstr, font=("Arial", 10))
                
            else:
                mask_image = topHead_Brain_tumorDetection.process_files(ImagePage.imagestr)
                ImagePage.image_reco, percentage = script.MNN.predict_neural_network(mask_image , 1)
                metrics = list(ImagePage.stats.values())
                precstr = "precision: {} \n recall: {} \n f-measure: {}".format(metrics[0],metrics[1],metrics[2])
                self.precisionLabel = tk.Label(self, bg='#74caf9', text=precstr, font=("Arial", 10))
            if(login.Login.accessLevel == "admin"):
                self.precisionLabel.grid(row=5, column=0, columnspan=2, sticky=tk.W)
            if(ImagePage.image_reco == 1):
                ImagePage.imageArgs[18] = str(percentage)
            elif(ImagePage.image_reco == 0):
                ImagePage.imageArgs[18] = '1'
                #print (self.image_reco)
        if (ImagePage.firstLayer==1):
            ImagePage.imageArgs[18] = '1'
            ImagePage.secondLayer, percentage = script.SNN.predict_neural_network(ImagePage.imagestr)
            if(ImagePage.secondLayer == 0):
                ImagePage.imageArgs[17] = str(percentage)
            elif(ImagePage.secondLayer == 1):
                ImagePage.imageArgs[17] = '1'
        image = Image.open(self.imagestr)
        image = image.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        #Backhead brain tumor detection 
            
        
        
        self.photolabel = tk.Label(self, image=photo, bg='#11AAFF')
        self.photolabel.image = photo 
        self.photolabel.grid(row=5, column=1)
        #if(self.image_reco == 1):
        #    labPage.LabPage.args.append('1')
        #else:
        #    labPage.LabPage.args.append('0')
            
    def toResults(self):
        self.photolabel.grid_forget()
        self.imagelabel.grid_forget()
        self.precisionLabel.grid_forget()
        resultsPage.ResultsPage.lVariables = ImagePage.imageArgs
        self.controller.show_frame("ResultsPage")