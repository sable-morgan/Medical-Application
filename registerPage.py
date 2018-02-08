import tkinter as tk
import script
from tkinter import ttk, PhotoImage
from PIL import ImageTk,Image
class Register(tk.Frame):#Any functions can use these global variables
    global newPassword 
    global newUserName
    global confirmPassword
    global answerE        
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#74caf9")
        #page title
#        label = tk.Label(self,bg='#74caf9', text="Welcome! Sign Up Here", font=controller.title_font)
#        label.grid(row=1, columnspan=3, pady=10, padx=200)
        #HOUSE LOGO
#        image = Image.open('images\\logo.png')
#        photo = ImageTk.PhotoImage(image)
#        self.photolabel = tk.Label(self, image=photo, bg='#74caf9')
#        self.photolabel.image = photo 
#        self.photolabel.grid(row=0, columnspan=4, pady=10, padx=200)
        image = Image.open('images\\signup.png')
        photo = ImageTk.PhotoImage(image)
        self.photolabel = tk.Label(self, image=photo, bg='#74caf9')
        self.photolabel.image = photo 
        self.photolabel.grid(row=0, columnspan=4, pady=10, padx=50)
        
        #username label and input
        self.newUserL = tk.Label(self,fg='#000000',bg='#74caf9',
                           font=controller.label_font, text='New Username: ').grid(row=2, column=0, pady=10, padx=100)
        newUserName = tk.Entry(self)
        newUserName.grid(row=2, column=0, sticky=tk.E)
        #password label and unput
        self.newPwordL = tk.Label(self,fg='#000000',bg='#74caf9',
                           font=controller.label_font, text='New Password: ').grid(row=3, column=0, pady=10, padx=100)
        newPassword = tk.Entry(self, show='*') 
        newPassword.grid(row=3, column=0, sticky=tk.E)

        self.confirmPwordL = tk.Label(self,fg='#000000',bg='#74caf9',
                           font=controller.label_font, text='Confirm Password: ').grid(row=4, column=0, pady=10, padx=100)
        confirmPassword = tk.Entry(self, show='*') 
        confirmPassword.grid(row=4, column=0, sticky=tk.E)
        
        sec_questionstr="What course is this application for?"
        self.secL = tk.Label(self,fg='#000000',bg='#74caf9',
                           font=controller.label_font, text='Security Question: \nWhat course is this application for?').grid(row=5, column=0, pady=10, padx=100)
        
        self.answerL = tk.Label(self,fg='#000000',bg='#74caf9',
                           font=controller.label_font, text='Answer: ').grid(row=6, column=0, pady=10, padx=100)
        answerE = tk.Entry(self)
        answerE.grid(row=6, column=0, sticky=tk.E)
        
        signupB = tk.Button(self, text='Submit', bg="#0759a5", fg="#ffffff", width=15, font=controller.label_font,
        command=lambda: Register.logintoWrite(newUserName.get(),newPassword.get(),confirmPassword.get(),sec_questionstr,answerE.get(), controller))
        signupB.grid(row=7, columnspan=3, pady=10, padx=200)
        
    def logintoWrite(user,password,confirmPass,sec_ques,sec_ans, controller):
        if (password == confirmPass):
            script.database.writeUser(user,password,sec_ques,sec_ans, "admin")
            controller.show_frame("Login")
        else:
             tk.messagebox.showerror('Error', 'The passwords do not match!')

