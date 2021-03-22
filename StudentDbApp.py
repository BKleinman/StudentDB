import sqlite3
import csv
import re

conn = sqlite3.connect('./studentDB.sqlite')  # establish connection
mycursor = conn.cursor()


def importData(filePath):  # a
    with open(filePath, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        count = 0
        for row in csv_reader:
            if row[0] == "FirstName":
                continue
            else:
                mycursor.execute(
                    'INSERT INTO Student(FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);',
                    (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],))
                conn.commit()
        mycursor.execute('Update Student set isDeleted = 0;')
    return


def printAll():  # b
    mycursor.execute('select * from Student where isDeleted = 0;')
    db = mycursor.fetchall()
    print(db)
    return


# c
def addStudent(fn, ln, gpa, major, advisor, address, city, state, zip, phone):
    mycursor.execute(
        'Insert into Student(FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
        (fn, ln, gpa, major, advisor, address, city, state, zip, phone, 0,))
    conn.commit()
    return


def updateMajor(ID, fieldValue):  # d had to split up the updates because the field can't have quotes around it
    mycursor.execute('Update Student set Major = ? where StudentId = ?', (fieldValue, ID,))
    conn.commit()
    return

def updateAdvisor(ID, fieldValue):  # d
    mycursor.execute('Update Student set FacultyAdvisor = ? where StudentId = ?', (fieldValue, ID,))
    conn.commit()
    return

def updatePhone(ID, fieldValue):  # d
    mycursor.execute('Update Student set MobilePhoneNumber = ? where StudentId = ?', (fieldValue, ID,))
    conn.commit()
    return


def softDelete(ID):  # e
    mycursor.execute('Update Student set isDeleted = 1 where StudentId = ?', (ID,))
    conn.commit()
    return


# f
def searchMajor(fieldValue):
    mycursor.execute('Select * from Student where Major = ? and isDeleted = 0;', (fieldValue,))
    db = mycursor.fetchall()
    print(db)
    return


def searchCity(fieldValue):
    mycursor.execute('Select * from Student where City = ? and isDeleted = 0;', (fieldValue,))
    db = mycursor.fetchall()
    print(db)
    return


def searchState(fieldValue):
    mycursor.execute('Select * from Student where State = ? and isDeleted = 0;', (fieldValue,))
    db = mycursor.fetchall()
    print(db)
    return


def searchAdvisor(fieldValue):
    mycursor.execute('Select * from Student where FacultyAdvisor = ? and isDeleted = 0;', (fieldValue,))
    db = mycursor.fetchall()
    print(db)
    return


def promptUser():
    print("1: Display all students")
    print("2: Add a new student")
    print("3: Update student")
    print("4: Delete student from database")
    print("5: Search/Display students by Major, GPA, City, State, and Advisor")
    temp = input("Enter the number of which option you would like to execute. (Type 'exit' to quit)")
    return temp


def main():
    passGo = True
    mycursor.execute('Delete from Student;')
    conn.commit()
    importData("/Users/brandonkleinman/Desktop/Datasets/students.csv")
    while passGo:
        choice = promptUser()
        if choice.lower() == "exit":
            passGo = False
            break
        if choice == "1":
            printAll()
        if choice == "2":
            fName = input("What is the student's first name?")
            lName = input("What is the student's last name?")
            invalid = True
            while invalid:
                try:
                    gpa = float(input("What is the students's gpa?"))
                except ValueError:
                    print("Invalid input; enter a valid gpa.")
                try:
                    if isinstance(gpa, float):
                        invalid = False
                        break
                except:
                    continue
            major = input("What is the student's major?")
            advisor = input("Who is the student's faculty advisor?")
            address = input("What is the student's address?")
            city = input("What city does the student live in?")
            state = input("What state does the student live in?")
            notValid = True
            while notValid:
                try:
                    zip = int(input("What is zip code does the student live in?"))
                except ValueError:
                    print("Invalid input; enter a valid zip code.")
                try:
                    if isinstance(zip, int):
                        notValid = False
                        break
                except:
                    continue
            pattern = r"\d{1} \(\d{3}\) \d{3}-\d{4}"
            while True:
                phone = input("Enter the student's phone number in the following format: 1 (408) 555-1234.")
                isphone = re.match(pattern, phone)
                if isphone:
                    break
                else:
                    print("Invalid input; enter a phone number matching the format presented.")
            addStudent(fName, lName, gpa, major, advisor, address, city, state, zip, isphone[0])
        if choice == "3":
            print("The following are the students to which you can apply updates.")
            printAll()
            mycursor.execute('select min(StudentID) from Student')
            minID = mycursor.fetchone()[0]
            mycursor.execute('select max(StudentID) from Student')
            maxID = mycursor.fetchone()[0]
            go = True
            while go:
                try:
                    id = int(input("Enter the ID of the student you would like to update:"))
                except:
                    print("Invalid input; enter a valid student ID.")
                try:
                    if id > maxID or id < minID:
                        print("Invalid input; enter a student ID that is in the database.")
                    else:
                        go = False
                        break
                except:
                    continue

            while True:
                field = input("Select which of the following you would like to update: "
                              "Major, Advisor, Phone Number.")
                if field.lower() == "major":
                    value = input("What would you like to update the student's major to?")
                    updateMajor(id, value)
                    break
                if field.lower() == "advisor":
                    value = input("Who would you like to update the student's advisor to?")
                    updateAdvisor(id, value)
                    break
                if field.lower() == "phone number":
                    pattern = r"\d{1} \(\d{3}\) \d{3}-\d{4}"
                    while True:
                        phone = input("Enter the student's phone number in the following format: 1 (408) 555-1234.")
                        isphone = re.match(pattern, phone)
                        if isphone:
                            break
                        else:
                            print("Invalid input; enter a phone number matching the format presented.")
                    updatePhone(id, isphone[0])
                    break
                else:
                    print("Invalid input. Enter a valid value.")
        if choice == "4":
            print("The following are the students which you can delete.")
            printAll()
            mycursor.execute('select min(StudentID) from Student')
            minID = mycursor.fetchone()[0]
            mycursor.execute('select max(StudentID) from Student')
            maxID = mycursor.fetchone()[0]
            go = True
            while go:
                try:
                    id = int(input("Enter the ID of the student you would like to delete:"))
                except:
                    print("Invalid input; enter a valid student ID.")
                try:
                    if id > maxID or id < minID:
                        print("Invalid input; enter a student ID that is in the database.")
                    else:
                        go = False
                        break
                except:
                    continue
            softDelete(id)
        if choice == "5":
            field = input("Which of the following fields would you like to search students by:"
                          "Major, GPA, City, State, or Advisor")
            if field.lower() == "major":
                value = input("What major would you like to search for?")
                print("These are the students with the major you entered:")
                searchMajor(value)
            if field.lower() == "city":
                value = input("What city would you like to search for?")
                print("These are the students who live in the city you entered:")
                searchCity(value)
            if field.lower() == "state":
                value = input("What state would you like to search for?")
                print("These are the students who live in the state you entered:")
                searchState(value)
            if field.lower() == "advisor":
                value = input("What advisor would you like to search for?")
                print("These are the students with the advisor you entered:")
                searchAdvisor(value)
            if field.lower() == "gpa":
                print("You will be able to search for students with GPA's less than, greater than, or equal to"
                      "the GPA you specify")
                invalid = True
                while invalid:
                    try:
                        gpa = float(input("What is the GPA you would like to query by?"))
                    except ValueError:
                        print("Invalid input; enter a valid gpa.")
                    try:
                        if isinstance(gpa, float):
                            invalid = False
                            break
                    except:
                        continue
                    finally:
                        break
                while True:
                    comp = input("Would you like to search for students with GPA's less than, equal to, or greater than"
                                 "the GPA you specified? Enter: less, equal, or greater.")
                    if comp.lower() == "less":
                        mycursor.execute('Select * from Student where GPA < ? and isDeleted = 0;', (gpa,))
                        db = mycursor.fetchall()
                        print(db)
                        break
                    if comp.lower() == "equal":
                        mycursor.execute('Select * from Student where GPA = ? and isDeleted = 0;', (gpa,))
                        db = mycursor.fetchall()
                        print(db)
                        break
                    if comp.lower() == "greater":
                        mycursor.execute('Select * from Student where GPA > ? and isDeleted = 0;', (gpa,))
                        db = mycursor.fetchall()
                        print(db)
                        break
                    else:
                        print("Invalid input; try again.")
    return


main()
