import tkinter as tk
import script
from tkinter import ttk, PhotoImage
from PIL import ImageTk,Image
class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #background
        self.configure(background="#74caf9")
        #title    
#        label = tk.Label(self, bg='#74caf9', text="Dashboard", font=controller.title_font)
#        label.grid(row=0, columnspan=4, pady=10)
        #pic title
        image = Image.open('images\\dashboard.png')
        photo = ImageTk.PhotoImage(image)
        self.photolabel = tk.Label(self, image=photo, bg='#74caf9')
        self.photolabel.image = photo 
        self.photolabel.grid(row=0, columnspan=4, pady=10, padx=50)
        
        #search button that triggers search_profiles function
        searchLabel = tk.Label(self, bg='#74caf9', text ="Search by ID: ", font=controller.label_font)
        searchLabel.grid(row=1, column=0, padx=250)

        #text to be searched by search_profiles function
        searchEntry = tk.Entry(self)
        searchEntry.grid(row=2, column=0, pady=10, padx=250)
        
        searchB = tk.Button(self, text="Search", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: self.searchProfiles(searchEntry.get()))
        searchB.grid()
        #create button that triggers create_new function
        createLabel = tk.Label(self, bg='#74caf9', text ="Create a profile page" , font=controller.label_font)
        createLabel.grid()
        createB = tk.Button(self, text="Create", bg="#0759a5", fg="#ffffff", width=15,
                           command=lambda: controller.show_frame("QuestionPage")) 
        createB.grid()
        
        logoutB = tk.Button(self, text="Logout", bg="#0759a5", fg="#ffffff", width=10,
                           command=lambda: controller.show_frame("Login")) 
        logoutB.grid(pady = 5)
        
        
    def searchProfiles(self, pid):
        profileArr = script.database.searchDB(pid)
        profileArr = profileArr.tolist()
        print(profileArr)
        patientprofilewindow = MainPage.profileWindow(profileArr)
    
        print("This will call the search page")

# Creates new profile sends user to questionaire page 
    def profileWindow(profilearray):
        patient = tk.Tk()         
        patient.title('Patient Profile')
        patient.geometry('600x600-500+50')
        patient.configure(background="#74caf9")
        patient.grid()
        #pic title
        
        patientIDstr = "PatientID: {}".format(profilearray[0])
        IDLabel = tk.Label(patient, text =patientIDstr, font="-size 15", bg="#74caf9")
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
                "Cell Volume: ", "White Blood Cell Count: ", "Red Blood Cell Count: ", "Herniated Disc: %", "Brain Tumor: %"]

        geninfostr = "General Information"
        IDLabel = tk.Label(patient, text =geninfostr, font="-size 12", bg="#74caf9")
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
        IDLabel = tk.Label(patient, text =medstr, font="-size 12", bg="#74caf9")
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
        labLabel = tk.Label(patient, text =labstr, font="-size 12", bg="#74caf9")
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