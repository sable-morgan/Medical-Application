# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 13:37:30 2017

@author: Nick
"""
import mysql.connector as SQL
import numpy as np
import config
import hashlib as hs
import tkinter.messagebox
class HouseDB(object): 
    def __init__(self): #constructs class by connecting the database using a config file
        try:    
            
            self.cnx = SQL.connect(**config.config)
            print("Connection to database successful")
            self.c = self.cnx.cursor(buffered=True)
            
        except:
            print("Connection to database unsuccessful")
    def __del__(self): #constructs class by connecting the database using a config file
        self.c.close()
        self.cnx.close()
    def readDB(self): #Takes entire data set for training purposes
        self.c.execute('SELECT questionnaire.*,labresults.*,diagnosis.sickness from questionnaire, labresults, diagnosis WHERE questionnaire.pid = labresults.pid AND questionnaire.pid = diagnosis.pid')
        # fetchall() returns a nested tuple (one tuple for each table row)
        results = self.c.fetchall()
        print(len(results[0]))

        cols = zip( *results ) # return a list of each column
                      # ( the * unpacks the 1st level of the tuple )
        outlist = []

        for col in cols:

            arr = np.asarray( col )

            outlist.append( arr )
        outlist = np.asarray( outlist )
        outlist = outlist.T
        outlist = np.delete(outlist, [71], axis=1)
        outlist = outlist.tolist()
        return outlist
    def writeDB(self, qArray, lArray, dArray): #input a row into the database
        qList = ','.join(map(str, qArray))
        print(len(qArray))
        self.c.execute('INSERT INTO questionnaire VALUES ('+qList+')')
        lList = ','.join(map(str, lArray))
        self.c.execute('INSERT INTO labresults VALUES ('+lList+')')
        dList = ','.join(map(str, dArray))
        self.c.execute('INSERT INTO diagnosis VALUES ('+dList+')')
        self.cnx.commit()

        
    def searchDB(self, pid): #searches the database for a specific pid, made for profile function
        self.c.execute("select column_name from information_schema.columns where table_name='questionnaire'")
        colresults = self.c.fetchall()
        print(len(colresults))
        self.c.execute("SELECT questionnaire.*,labresults.*,diagnosis.sickness FROM questionnaire,labresults,diagnosis WHERE questionnaire.pid=labresults.pid AND questionnaire.pid=diagnosis.pid AND questionnaire.pid="+ pid)
        results = self.c.fetchall()
        print(len(results))
        cols = zip( *results ) # return a list of each column
                      # ( the * creates a tuple from the columns )
        outlist = []

        for col in cols:

            arr = np.asarray( col )

            type = arr.dtype

            outlist.append( arr )
 
        outlist = np.asarray( outlist )
        
        outlist = outlist.T
        outlist = np.delete(outlist, [71], axis=1)
        return outlist[0]
    def getCols(self): #searches the database for a specific pid, made for profile function
        self.c.execute("select column_name from information_schema.columns where table_name='questionnaire'")
        results = self.c.fetchall()
        print(len(results))
        cols = zip( *results ) # return a list of each column
                      # ( the * creates a tuple from the columns )
        outlist = []

        for col in cols:

            arr = np.asarray( col )

            type = arr.dtype

            outlist.append( arr )
 
        outlist = np.asarray( outlist )
        
        self.c.execute("select column_name from information_schema.columns where table_name='labresults'")
        labresults = self.c.fetchall()
        print(len(labresults))
        cols = zip( *labresults ) # return a list of each column
                      # ( the * creates a tuple from the columns )
        lablist = []

        for col in cols:

            arr = np.asarray( col )

            type = arr.dtype

            lablist.append( arr )
 
        lablist = np.asarray( lablist )
        

        self.c.execute("select column_name from information_schema.columns where table_name='diagnosis'")
        results = self.c.fetchall()
        print(len(results))
        cols = zip( *results ) # return a list of each column
                      # ( the * creates a tuple from the columns )
        diaglist = []

        for col in cols:

            arr = np.asarray( col )

            type = arr.dtype

            diaglist.append( arr )
 
        diaglist = np.asarray( diaglist )
        

        
        outlist = np.concatenate((outlist, lablist), axis=1)
        outlist = np.concatenate((outlist, diaglist), axis=1)
        outlist = np.delete(outlist, [71])
        outlist = np.delete(outlist, [89])
        return outlist
    def checkLogin(self, user, password): #checks login information with the database's set login info
        string ="SELECT * FROM login WHERE username='{}'".format(user)
        self.c.execute(string)
        results = self.c.fetchone()
        outlist = []
        arr = np.asarray( results )
        outlist.append( arr )
        #print(outlist)
        #print(user)
        if(results == None):
            tkinter.messagebox.showinfo('Error', 'No user by that name found.')
            return 0
        
        m = hs.sha256(str(password).encode('utf-32')).hexdigest()
        for i in range(0,50000):
            m = hs.sha256(str(m).encode('utf-32')).hexdigest()
            
        #print(m)
        if(outlist[0][0] == user):
            if(m == outlist[0][1]):
                print ("login successful")
                return 1, outlist[0][4]
            else:
                print("password incorrect")
                tkinter.messagebox.showinfo('Error', 'Password is incorrect. Try again.')
                return 0
        else:
            print("No user by that name found")
            tkinter.messagebox.showinfo('Error', 'No user by that name found.')

            return 0
    def writeUser(self, user, password, sec_question, sec_answer, access): #writes a new user to the database after hashing
        m = hs.sha256(str(password).encode('utf-32')).hexdigest()
        s = hs.sha256(str(sec_answer).encode('utf-32')).hexdigest()
        for i in range(0,50000):
            m = hs.sha256(str(m).encode('utf-32')).hexdigest()
            s = hs.sha256(str(s).encode('utf-32')).hexdigest()
        #print(m)
        #print(s)
        string = "INSERT INTO login VALUES('{}','{}','{}','{}','{}')".format(user,m,sec_question,s,access)
        print (string)
        self.c.execute(string)
        self.cnx.commit()
    def checkForUser(self): 
        self.c.execute("SELECT * from login")
        # fetchall() returns a nested tuple (one tuple for each table row)
        results = self.c.fetchall()
        users = len(results)
        return users
    def deleteUser(self, user): 
        string ="SELECT * FROM login WHERE username='{}'".format(user)
        self.c.execute(string)
        # fetchall() returns a nested tuple (one tuple for each table row)
        results = self.c.fetchall()
        if (len(results) != 0):
            string ="DELETE FROM login WHERE username='{}'".format(user)
            self.c.execute(string)
            self.cnx.commit()
    
    def resetPass(self, user,newPass,secAns):
        string ="SELECT * FROM login WHERE username='{}'".format(user)
        self.c.execute(string)
        results = self.c.fetchone()
        outlist = []
        arr = np.asarray( results )
        outlist.append( arr )
        m = hs.sha256(str(newPass).encode('utf-32')).hexdigest()
        s = hs.sha256(str(secAns).encode('utf-32')).hexdigest()
        for i in range(0,50000):
            m = hs.sha256(str(m).encode('utf-32')).hexdigest()
            s = hs.sha256(str(s).encode('utf-32')).hexdigest()
        if(s==outlist[0][3]):
            string ="UPDATE login SET password='{}' WHERE username='{}'".format(m, user)
            self.c.execute(string)
            self.cnx.commit()
        else:
            print("Security answer not correct")
            
    def getQuestionnaire(self): #searches the database for a specific pid, made for profile function
        self.c.execute("select column_name from information_schema.columns where table_name='questionnaire'")
        results = self.c.fetchall()
        print(len(results))
        cols = zip( *results ) # return a list of each column
                      # ( the * creates a tuple from the columns )
        outlist = []

        for col in cols:

            arr = np.asarray( col )

            type = arr.dtype

            outlist.append( arr )
 
        outlist = np.asarray( outlist )
        outlist = np.delete(outlist, [5])
        outlist = np.delete(outlist, [0])
        return outlist
######### Testing the functions
if __name__=='__main__':      
    testing = HouseDB()
    print(testing.checkLogin("just", "test2"))
    #cols = testing.readDB()
    #print(cols)
    #testing.writeUser("just", "test", "What class is this application for?", "4996", "User")
    #testing.deleteUser("nick")
    #print(data)
    #print(testing.checkForUser)
#data = np.asarray( data )
#data = data.T
#print(data)
#data = ['401', '32', '0', '32', '32', 1.0, '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '60', '80', '1.025', '0', '0', '0', '0', '0', '0', '81', '15', '0.5', '141', '3.6', '15', '46', '10500', '5.3', '0', '1']
#data = np.array(data)
#string = 'INSERT INTO questionnaire VALUES({})'.format(data)
#testing.writeDB(data)
#testing.checkLogin("hospital", "hospital123")
#data = np.array(data)
#print(data)
#data = data.tolist()
#print(data[0])
######### end of testing