#Title: Guest Log Program
#Developer: Justice Torkornoo

import os
import sqlite3
from datetime import datetime
import csv
import time

global day
global month
global year

# Global variables are needed for entering the data into the database through the "commit" method

now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

pending = "PENDING" #This is used when searching for people that have not signed out yet

os.system('cls')

def commit():
    connect = sqlite3.connect('guestLog.db') #connects to the guestLog database file which is included in the repository
    c = connect.cursor()
    c.execute("INSERT INTO GuestLog (Date_In, Time_In, Resident_Name, Room_Number, Resident_Number, Guest_Name, Guest_Birthday, Age, Overnight, DA_Initials, Under18, Date_Out, Time_Out) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(date, real_time, residentFullName, room, residentPhoneNumber, guestFullName, guestBirth, str(over18), overnight, initials, under, pending, pending))
    connect.commit()
    connect.close()

def residentName():
    residentFName = input("Enter Resident's first name\n").lower()
    residentLName = input("\nEnter Resident's last name\n").lower()
    global residentFullName
    residentFullName = residentFName + " " + residentLName

def roomNumber():
    limit = 214
    global room
    room = input("\nEnter Resident's room number\n").lower()
    
    # The WITH statment runs through the CSV file with all the room numbers and verifies that the user was not given a room that does not exist
    with open('room_numbers.csv') as csvFile:
        database = csv.reader(csvFile)
        for row in database:
            if room == row[0]:
                pass
            else:
                limit = limit - 1
        if limit == 1:
            while limit == 1: 
                limit = 214     
                print("\nRoom " + room + " either does not exist or is not in use")
                room = input("Please re-enter the resident's room number\n\n").lower()
                with open('room_numbers.csv') as csvFile:
                    database = csv.reader(csvFile)
                    for row in database:
                        if room == row[0]:
                            pass
                        else:
                            limit = limit - 1   
                              
def residentPhone():
    global residentPhoneNumber
    residentPhoneNumber = input("\nEnter Resident's phone number\n")

    # The IF statment verifies that the user types in the correct format for the phone number
    if len(residentPhoneNumber) != 10:
        while len(residentPhoneNumber) != 10:
            residentPhoneNumber = input("\nThe phone number you entered is in the incorrect format. Please re-enter\n")
    residentPhoneNumber = residentPhoneNumber[0:3] + "-" + residentPhoneNumber[3:6] + "-" + residentPhoneNumber[6:]

def guestName():
    global guestFullName
    guestFName = input("\nEnter guest's first name\n").lower()
    guestLName = input("\nEnter guest's last name\n").lower()
    guestFullName = guestFName + " " + guestLName

def guestBirthDay():
    global guestBirth
    global guestBirthYear
    guestBirth = input("\nEnter guest's birth day (Format: MMDDYYYY)\n")

    # The IF statment verifies that the user typed in the correct format for the birth date and the second one verifies
    # that the user entered a year that makes sense
    if len(guestBirth) != 8:
        while len(guestBirth) != 8:
            print("\nIncorrect format")
            guestBirth = input("\nPlease enter the birthday with the correct format 'MMDDYYYY'\n")

    if int(guestBirth[4:]) >= year:
        while int(guestBirth[4:]) >= year:
            guestBirth = input("\nPlease re-enter the birthdate, the year is incorrect\n")
    guestBirthYear = int(guestBirth[4:])
    guestBirth = guestBirth[0:2] + "/" + guestBirth[2:4] + "/" + guestBirth[4:]
    print(guestBirth)

def da(): # da == Desk Assistant
    global initials
    initials = input("\nEnter your initials\n").upper()

def confirmation():
    print("\nDate        Time In     Resident's Name       Room#     Resident's Phone        Guest's Name         Birth Date     Age    Overnight   DA Initials     Under 18")
    print("{:10}  {:7}     {:20}  {:4}      {:12}            {:20} {:10}     {:3}    {:3}         {:2}              {:3}".format(date, real_time, residentFullName, room, residentPhoneNumber, guestFullName, guestBirth, str(over18), overnight, initials, under))
    confirm = input("\nIs the above information correct?\n").upper()

    if confirm == "YES":
        commit()
        print()
        os.system('cls')
        print(guestFullName, "has been signed in")
        time.sleep(2)
    if confirm == "NO":
        repair()

def repair():
    answer = input("\nWhat info needs to be changed?\n1. Resident's Name\n2. Resident's Room Number\n3. Resident's Phone Number\n4. Guest Name\n5. Guest Birth Date\n6. DA Initials\n").lower()
    if answer == "1":
        print()
        residentName()
        confirmation()
    if answer == "2":
        print()
        roomNumber()
        confirmation()
    if answer == "3":
        print()
        residentPhone()
        confirmation()
    if answer == "4":
        print()
        guestName()
        confirmation()
    if answer == "5":
        print()
        guestBirthDay()
        ageCalUNDER()
        confirmation()
    if answer == "6":
        print()
        da()
        confirmation()

def ageCalUNDER():
    global overnight
    global over18
    global under
    over18 = year - guestBirthYear
    if over18 <= 17:
        print("\nWARNING " + guestFullName, "is under 18")
        under = "YES" # Enters into database that the guest is under 18
        overnight = "NO" # Enters into the database that the guest can not stay overnight due to the fact they are underage
    else:
        under = "NO"
        overnight = input("\nIs " + guestFullName + " staying overnight?\n").upper()

def signInTimeDate():
    global hour
    global minute
    global real_time
    global date
    if hour == 0:
        hour = 12
    if hour in range(13, 24):
        dart = "PM"
        hour = hour - 12
    else:
        dart = "AM"
    if minute in range(0, 10):
        add_the_zero = 0
    else:
        add_the_zero = ""

    real_time = str(hour) + ":" + str(add_the_zero) + str(minute) +  str(dart)
    date = str(month) + "/" + str(day) + "/" + str(year)

def option1(): # Signing people in
    os.system('cls')
    residentName()
    roomNumber()
    residentPhone()
    guestName()
    guestBirthDay()
    ageCalUNDER()
    signInTimeDate()
    da()
    confirmation()
    
def option2(): # Signing people out
    resident = ""
    guest = ""

    os.system('cls')
    while guest == "":
        guest = input("Enter guest's name\n")
        answer = input("\nIs this correct?\n").upper()
        while answer == "NO":
            guest = input("Enter guest's name\n")
            answer = input("\nIs this correct?\n").upper()

    while resident == "":
        resident = input("\nEnter resident's name\n")
        answer = input("\nIs this correct?\n").upper()
        while answer == "NO":
            resident = input("\nEnter resident's name\n")
            answer = input("\nIs this correct?\n").upper()
    
    connect = sqlite3.connect('guestLog.db')
    c = connect.cursor()
    c.execute("SELECT * FROM GuestLog WHERE Guest_Name LIKE '" + guest + "%' AND Resident_Name LIKE '" + resident + "%' AND Date_Out = 'PENDING' ORDER BY Date_In")
    result = c.fetchall()

    signInTimeDate()
    print()

    datein = ""

    print("Date In      Time In     Resident's Name       Room#     Resident's Phone        Guest's Name         Birth Date     Age    Overnight   DA Initials     Under 18     Date Out     Time Out")

    for i in result:
        datein = i[0]
        print("{:10}   {:7}     {:20}  {:4}      {:12}            {:20} {:8}     {:3}    {:3}         {:2}              {:3}          {:8}     {:7}".format(datein, i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12]))
    
    if datein == "":
        print()
        print(guest + " either never signed in with " + resident + ", or " + guest + " was already signed out")
    
    else:
        signOut = input("\nConfirm sign out of " + i[5] + " (yes/no)\n").upper()

        if signOut == "YES":
            connect = sqlite3.connect('guestLog.db')
            c = connect.cursor()
            c.execute("SELECT * FROM GuestLog WHERE Guest_Name LIKE '" + guest + "%' AND Resident_Name LIKE '" + resident + "%'")
            c.execute("UPDATE GuestLog SET Date_Out = '" + date + "', Time_Out = '" + real_time + "' WHERE Guest_Name LIKE '" + guest + "%' AND Resident_Name LIKE '" + resident + "%' AND Date_Out = 'PENDING' AND Time_Out = 'PENDING'")
            connect.commit()
            connect.close()

            print("\n" + i[5] + " has been signed out")
            time.sleep(2)

        if signOut == "NO":
            print("\nOperation cancelled")

while True:
    os.system('cls')
    answer = input("Enter the number of the option you would like to use\n1. Sign someone in\n2. Sign someone out\n")

    if answer == "1":
        option1()

    if answer == "2":
        option2()

    if answer == "exit":
        break