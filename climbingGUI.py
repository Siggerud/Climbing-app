# this is an app that keeps track of all routes you've climbed and the corresponding number of times

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# TODO: teste
# legge til kommentarer


class ClimbingGUI:
    def __init__(self, master):
        self.routeDict = self.getRouteDict()
        self.gradeDict = self.getGradeDict()
        self.dates = self.getDateChanges()

        self. master = master
        master.title("Climbing grade tracker")
        master.geometry("400x400")

        # creating tabs
        self.tabParent = ttk.Notebook(master)
        self.tabParent.bind('<<NotebookTabChanged>>', self.checkIndexOfTab)
        self.tabInput = ttk.Frame(self.tabParent, width=400, height=400)
        self.tabOutput = ttk.Frame(self.tabParent, width=400, height=400)

        self.tabParent.add(self.tabInput, text="Input")
        self.tabParent.add(self.tabOutput, text="Summary")

        self.tabParent.grid(row=0, column=0)

        # creating input layout
        labelPrompt = Label(self.tabInput, text="What did you climb today?", font="Cambria")
        labelPrompt.grid(row=0, column=0)

        for i in range(3, 10):
            gradeButton = Button(self.tabInput, text=f"Grade {i}", bg="cyan", command= lambda i=i: self.createGradeButtons(i))
            gradeButton.grid(row=i-2, column=0, sticky="w", pady=5)

        self.gradeButtonsFrame = ttk.Frame(self.tabInput)


    # retrieves a dictionary containing all grades in french grade scale
    def getGradeDict(self):
        gradeDict = {
            3: ["3"],
            4: ["4a", "4b", "4c"],
            5: ["5a", "5b", "5c"],
            6: ["6a", "6a+", "6b", "6b+", "6c", "6c+"],
            7: ["7a", "7a+", "7b", "7b+", "7c", "7c+"],
            8: ["8a", "8a+", "8b", "8b+", "8c", "8c+"],
            9: ["9a", "9a+", "9b", "9b+", "9c"]
        }

        return gradeDict


    # retrieves a dictionary where key is the grade climbed and the value is corresponding number of times
    # climbed
    def getRouteDict(self):
        file = open("climbingGrades.txt", "r")
        lines = file.readlines()

        routeDict = {}
        if len(lines) != 0:
            for line in lines:
                splitLine = line.split()
                key = splitLine[0]
                value = splitLine[1]

                routeDict[key] = int(value)

        return routeDict

    # retrieves when you last made a change
    def getDateChanges(self):
        datesFile = open("dates.txt", "r")
        lines = datesFile.readlines()

        dates = {}
        if len(lines) > 0:
            for line in lines:
                splitLine = line.split()
                key = " ".join(splitLine[:2])
                value = " ".join(splitLine[2:])
                dates[key] = value

        datesFile.close()

        return dates


    # changes the txt file that keeps track of grades and numbers
    def changeTxtFile(self):
        file = open("climbingGrades.txt", "w")
        for key in self.routeDict:
            if self.routeDict[key] != 0:
                file.writelines(f"{key} {self.routeDict[key]}\n")

        file.close()


    # checks if user is on input or output tab. Adds labels if on output tab
    def checkIndexOfTab(self, *args):
        index = self.tabParent.index(self.tabParent.select())
        if index == 1:
            self.addLabelsforRoutesClimbed()

    # adds labels showing the grades climbed and corresponding number of times climbed
    def addLabelsforRoutesClimbed(self):
        for widget in self.tabOutput.winfo_children(): # destroy previous labels
            widget.destroy()

        self.summaryExplanation = Label(self.tabOutput, text="A summary of every climb registered.")
        self.summaryExplanation.grid(row=0, column=0, columnspan=5)

        self.gradeLabelHeader = Label(self.tabOutput, text="Grade")
        self.gradeLabelHeader.grid(row=1, column=0, sticky="w")

        self.numberOfGradesHeader = Label(self.tabOutput, text="Number")
        self.numberOfGradesHeader.grid(row=1, column=1, sticky="w")

        if len(self.routeDict) > 13:
            self.gradeLabelHeader2 = Label(self.tabOutput, text="Grade")
            self.gradeLabelHeader2.grid(row=1, column=2, sticky="w")

            self.numberOfGradesHeader2 = Label(self.tabOutput, text="Number")
            self.numberOfGradesHeader2.grid(row=1, column=3, sticky="w")

        columnGradeValue = 0
        columnNumberOfGradesValue = 1
        rowTracker = 2
        for index, grade in enumerate(sorted(self.routeDict)):
            if index > 12:
                columnGradeValue = 2
                columnNumberOfGradesValue = 3
                rowTracker = -11


            self.gradeLabel = Label(self.tabOutput, text=f"{grade}")
            self.gradeLabel.grid(row=index+rowTracker, column=columnGradeValue, sticky="w")

            self.numberOfGradesLabel = Label(self.tabOutput, text=f"{self.routeDict[grade]}")
            self.numberOfGradesLabel.grid(row=index+rowTracker, column=columnNumberOfGradesValue, sticky="w")

        if len(self.routeDict) < 14: # make second pair of columns if there are too many grades to fit in first pair
            col = 3
        else:
            col = 5

        editSummaryButton = Button(self.tabOutput, text="Edit summary", bg="orange", command=self.addEditPopup)
        editSummaryButton.grid(row=14, column=col)

        count = 0
        for key in self.dates:
            if self.dates[key] != "0":
                self.dateLabel = Label(self.tabOutput, text=f"{key} registered {self.dates[key]}")
                self.dateLabel.grid(row=15+count, columnspan=5, sticky="w")
                count += 1


    # popup menu for changing number of times a route has been climbed
    def addEditPopup(self):
        self.editSummary = Toplevel(self.tabOutput)
        self.editSummary.geometry("250x200")
        self.editSummary.title("Edit Summary")

        editPrompt1 = Label(self.editSummary, text="Enter the grade you want to edit")
        editPrompt1.grid(row=0, column=0, columnspan=2, rowspan=1)

        editPrompt2 = Label(self.editSummary,
                                text="and the correct number of climbs")
        editPrompt2.grid(row=1, column=0, columnspan=2)

        editFrame = Frame(self.editSummary)
        editFrame.grid(row=2, column=0, rowspan=2, columnspan=2)

        editGrade = Label(editFrame, text="Grade")
        editGrade.grid(row=0, column=0)

        editNumber = Label(editFrame, text="Number")
        editNumber.grid(row=0, column=1)

        self.editGradeVar = StringVar()
        self.editGradeVar.set("4a")
        editGradeEntry = Entry(editFrame, width=5, textvariable=self.editGradeVar)
        editGradeEntry.grid(row=1, column=0)

        self.editNumberEntryVar = IntVar()
        editNumberEntry = Entry(editFrame, width=5, textvariable=self.editNumberEntryVar)
        editNumberEntry.grid(row=1, column=1)

        changeSummaryButton = Button(self.editSummary, text="Register change", bg="spring green", command=self.changeSummary)
        changeSummaryButton.grid(row=4, column=1)


    # changes summary of grades and corresponding numbers from user input
    def changeSummary(self):
        gradeToBeChanged = self.editGradeVar.get()

        flag = 0
        for keys in self.gradeDict:
            if gradeToBeChanged in self.gradeDict[keys]:
                flag = 1

        if flag == 0:
            messagebox.showwarning(message=f"{gradeToBeChanged} is not a valid grade.")
            return
        try:
            newNumber = self.editNumberEntryVar.get()
        except TclError:
            messagebox.showwarning(message="Enter a number. No changes registered.")
            return

        self.registerDateChanges("Last edit")
        self.showSummaryChangesToUser(gradeToBeChanged, newNumber)
        self.routeDict[gradeToBeChanged] = newNumber
        self.changeTxtFile()
        self.routeDict = self.getRouteDict()
        self.addLabelsforRoutesClimbed()


    # show the changes that have been made in a messagebox
    def showSummaryChangesToUser(self, grade, newNumber):
        try:
            oldNumber = self.routeDict[grade]
        except KeyError:
            oldNumber = 0

        if oldNumber != newNumber:
            message = f"Number of times you've climbed\ngrade {grade} changed from {oldNumber} to {newNumber}."
        else:
            message = "No changes registered"
        messagebox.showinfo(message=message)


    # creates buttons for each number grade
    def createGradeButtons(self, grade):
        for widget in self.gradeButtonsFrame.winfo_children():
            widget.destroy()

        self.gradeButtonsFrame.grid(row=1, column=1, rowspan=7)

        labelPromptNumber = Label(self.gradeButtonsFrame, text="How many?")
        labelPromptNumber.grid(row=0, column=1)


        self.varGradeNumber = IntVar()

        self.varGradeList = []
        self.varGradeNumberList = []
        for index, grades in enumerate(self.gradeDict[grade]):
            varGrade = StringVar()
            varGrade.set("0")
            gradeLabel = Checkbutton(self.gradeButtonsFrame, text=f"{grades}", variable=varGrade, onvalue=grades, offvalue="0")
            gradeLabel.grid(row=index+1, column=0, sticky="w")

            varGradeNumber = IntVar()
            gradeEntry = Entry(self.gradeButtonsFrame, textvariable=varGradeNumber, width=8)
            gradeEntry.grid(row=index+1, column=1, sticky="w")

            self.varGradeList.append(varGrade)
            self.varGradeNumberList.append(varGradeNumber)

        commitButton = Button(self.gradeButtonsFrame, text="Register", bg="spring green", command=self.commitChanges)
        commitButton.grid(column=1)


    # registers any changes fron input tab to the txt file
    def commitChanges(self):

        routeDict = self.routeDict.copy()

        for i in range(len(self.varGradeList)):
            if self.varGradeList[i].get() != "0":
                try:
                    if self.varGradeList[i].get() not in self.routeDict:
                        routeDict[self.varGradeList[i].get()] = self.varGradeNumberList[i].get()
                    else:
                        routeDict[self.varGradeList[i].get()] += int(self.varGradeNumberList[i].get())
                except TclError:
                    messagebox.showwarning(message="Enter a number. No changes registered")
                    self.resetGradeAndNumberVariables()
                    return

        self.registerDateChanges("Last commit")
        self.showRegisteredChangesToUser()
        self.routeDict = routeDict
        self.changeTxtFile()
        self.routeDict = self.getRouteDict()
        self.resetGradeAndNumberVariables()


    # register time of date change
    def registerDateChanges(self, key):
        now = datetime.now()
        dateText = now.strftime("%d:%m%Y %H:%M:%S")
        self.dates[key] = dateText
        self.editDateTxt()


    # edits file holding date changes
    def editDateTxt(self):
        dateFile = open("dates.txt", "w")

        for key in self.dates:
            dateFile.write(f"{key} {self.dates[key]}\n")

        dateFile.close()



    # resets the grade and number variables
    def resetGradeAndNumberVariables(self):
        for i in range(len(self.varGradeList)):
            self.varGradeList[i].set("0")
            self.varGradeNumberList[i].set(0)


    # shows the registered changes from input menu in a message box
    def showRegisteredChangesToUser(self):
        self.registeredChangesPopup = Toplevel(self.tabInput)
        self.registeredChangesPopup.title("Change summary")

        count = 0
        for i in range(len(self.varGradeList)):
            textToShow = ""
            if self.varGradeList[i].get() != "0":
                grade = self.varGradeList[i].get()
                number = self.varGradeNumberList[i].get()
                if self.varGradeList[i].get() not in self.routeDict:
                    textToShow += f"You climbed your first grade {grade}!\n"
                textToShow += f"Registered {number} climb(s) of grade {grade}.\n"

                infoLabel = Label(self.registeredChangesPopup, text=textToShow)
                infoLabel.grid(column=0, columnspan=3, sticky="w")
                count += 1

        width = 50 + count*50
        self.registeredChangesPopup.geometry(f"300x{width}")

        goToSummaryButton = Button(self.registeredChangesPopup, text="Go to Summary", command=self.goToSummary, bg="cyan")
        goToSummaryButton.grid(column=1)


    # navigates to summary tab
    def goToSummary(self):
        self.tabParent.select(self.tabOutput)
        self.registeredChangesPopup.destroy()



root = Tk()
climbGUI = ClimbingGUI(root)
root.mainloop()





