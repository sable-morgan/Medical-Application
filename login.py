import tkinter as tk
import script
from tkinter import ttk, PhotoImage
from PIL import ImageTk,Image
import automatedChecker
import threading

class Login(tk.Frame):
    global currentUname
    global currentPword
    global currentPword 
    global loginWind
    global currentUname
    global accessLevel
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="#11AAFF")
        Login.accessLevel = "User"
        #background image
        imagebg = Image.open('images\\background.jpg')
        photobg = ImageTk.PhotoImage(imagebg)
        self.photolabel = tk.Label(self, image=photobg)
        self.photolabel.image = photobg 
        self.photolabel.place(x=0, y=0)
        #page title
        label = tk.Label(self, bg='#74caf9', text="Medical Application\nLogin", font=controller.title_font)
        label.grid(row=1, columnspan=4, pady=5)
        #HOUSE LOGO
        image = Image.open('images\\logo.png')
        photo = ImageTk.PhotoImage(image)
        self.photolabel = tk.Label(self, image=photo, bg='#11AAFF')
        self.photolabel.image = photo 
        self.photolabel.grid(row=0, columnspan=4, pady=10, padx=200)
        
        #label and text box- username
        self.userNameL = tk.Label(self, font=controller.label_font, fg='#000000',bg='#74caf9', 
                                  text='Username: ').grid(row=2, column=0, pady=10, padx=100)
        self.username = tk.StringVar(value = '')
        self.currentUname = tk.Entry(self, textvariable = self.username,  width=22)
        self.currentUname.grid(row=2, column=0, sticky=tk.E)

        #label and text box- password
        self.passwordL = tk.Label(self, font=controller.label_font, fg='#000000', bg='#74caf9', 
                                  text='Password: ').grid(row=3, column=0, pady=10, padx=100)
        self.password = tk.StringVar(value = '')
        self.currentPword = tk.Entry(self, textvariable = self.password, width=22, show='*')
        self.currentPword.grid(row=3, column=0, sticky=tk.E)  

        #button to the main page
        loginB = tk.Button(self, text="Login",  bg="#0759a5", fg="#ffffff", width=20, font=controller.label_font,
                       command=lambda: self.verifyLogin())
        loginB.grid(row=4, columnspan=4, pady=10, padx=200)
        #enter button hit; goes to try to login
        #loginB.bind("<Return>", self.verifyLogin()) 
        
        #forgot button- red
        forgotB = tk.Button(self, text="Forgot password?",  bg="red", fg="#ffffff", width=20, font=controller.label_font,
                       command=lambda: controller.show_frame("Forgot"))
        forgotB.grid(row=6, columnspan=4, pady=10, padx=200)

    def verifyLogin(self):
        logincheck, role = script.database.checkLogin(str(self.username.get()),str(self.password.get()))
        #print(role)
        self.currentUname.delete(0,tk.END)
        self.currentPword.delete(0,tk.END)
        #verify the username and password
        if (logincheck == 1):
            #train_NN()
            autoLogout = threading.Thread(target=automatedChecker.logout_loop, args=(self.controller,), daemon=False)
            autoLogout.start()
            if role == "admin":
                Login.accessLevel = "admin"
                #print(Login.accessLevel)
                self.controller.show_frame("AdminMainPage")
            else:
                Login.accessLevel = "User"
                self.controller.show_frame("MainPage")