from tkinter import Tk, Label, Button, Entry, Checkbutton, ttk, StringVar, IntVar
#TODO
# change geometry when summary gets big
# merge changes
# clean code

class ClimbingGUI:
    def __init__(self, master):
        self. master = master
        master.title("Climbing grade tracker")
        master.geometry("400x300")

        # creating tabs
        self.tabParent = ttk.Notebook(master)
        self.tabParent.bind('<<NotebookTabChanged>>', self.checkIndexOfTab)
        self.tabInput = ttk.Frame(self.tabParent, width=400)
        self.tabOutput = ttk.Frame(self.tabParent, width=400)

        self.tabParent.add(self.tabInput, text="Input")
        self.tabParent.add(self.tabOutput, text="Summary")

        self.tabParent.grid(row=0, column=0)

        # creating input layout
        self.labelPrompt = Label(self.tabInput, text="What did you climb today?")
        self.labelPrompt.grid(row=0, column=0)

        for i in range(3, 10):
            self.gradeButton = Button(self.tabInput, text=f"Grade {i}", command= lambda i=i: self.createGradeButtons(i))
            self.gradeButton.grid(row=i-2, column=0, sticky="w", pady=5)

        self.gradeButtonsFrame = ttk.Frame(self.tabInput)


    def checkIndexOfTab(self, *args):
        index = self.tabParent.index(self.tabParent.select())
        if index == 1:
            self.addLabelsforRoutesClimbed()

    def addLabelsforRoutesClimbed(self):
        for widget in self.tabOutput.winfo_children():
            widget.destroy()


        file = open("climbingGrades.txt", "r")
        file = open("climbingGrades.txt", "r")
        lines = file.readlines()

        routeDict = {}
        if len(lines) != 0:
            for line in lines:
                splitLine = line.split()
                key = splitLine[0]
                value = splitLine[1]

                routeDict[key] = int(value)

        self.gradeLabelHeader = Label(self.tabOutput, text="Grade")
        self.gradeLabelHeader.grid(row=0, column=0)

        self.numberOfGradesHeader = Label(self.tabOutput, text="Number")
        self.numberOfGradesHeader.grid(row=0, column=1)

        for index, grade in enumerate(sorted(routeDict)):
            self.gradeLabel = Label(self.tabOutput, text=f"{grade}")
            self.gradeLabel.grid(row=index+1, column=0, sticky="w")

            self.numberOfGradesLabel = Label(self.tabOutput, text=f"{routeDict[grade]}")
            self.numberOfGradesLabel.grid(row=index+1, column=1, sticky="w")

    def createGradeButtons(self, grade):
        for widget in self.gradeButtonsFrame.winfo_children():
            widget.destroy()

        self.gradeButtonsFrame.grid(row=1, column=1, rowspan=7)

        self.gradeDict = {
            3: ["3"],
            4: ["4a", "4b", "4c"],
            5: ["5a", "5b", "5c"],
            6: ["6a", "6a+", "6b", "6b+", "6c", "6c+"],
            7: ["7a", "7a+", "7b", "7b+", "7c", "7c+"],
            8: ["8a", "8a+", "8b", "8b+", "8c", "8c+"],
            9: ["9a", "9a+", "9b", "9b+", "9c"]
        }
        self.labelPromptNumber = Label(self.gradeButtonsFrame, text="How many?")
        self.labelPromptNumber.grid(row=0, column=1)


        self.varGradeNumber = IntVar()

        self.varGradeList = []
        self.varGradeNumberList = []
        for index, grades in enumerate(self.gradeDict[grade]):
            varGrade = StringVar()
            varGrade.set("0")
            self.gradeLabel = Checkbutton(self.gradeButtonsFrame, text=f"{grades}", variable=varGrade, onvalue=grades, offvalue="0")
            self.gradeLabel.grid(row=index+1, column=0, sticky="w")

            varGradeNumber = IntVar()
            self.gradeEntry = Entry(self.gradeButtonsFrame, textvariable=varGradeNumber)
            self.gradeEntry.grid(row=index+1, column=1, sticky="w")

            self.varGradeList.append(varGrade)
            self.varGradeNumberList.append(varGradeNumber)

        self.commitButton = Button(self.gradeButtonsFrame, text="Register", command=self.commitChanges)
        self.commitButton.grid(column=1)


    def commitChanges(self):
        file = open("climbingGrades.txt", "r")
        lines = file.readlines()

        routeDict = {}
        if len(lines) != 0:
            for line in lines:
                splitLine = line.split()
                key = splitLine[0]
                value = splitLine[1]

                routeDict[key] = int(value)

        for i in range(len(self.varGradeList)):
            if self.varGradeList[i].get() != "0":
                if self.varGradeList[i].get() not in routeDict:
                    routeDict[self.varGradeList[i].get()] = self.varGradeNumberList[i].get()
                else:
                    routeDict[self.varGradeList[i].get()] += int(self.varGradeNumberList[i].get())

                self.varGradeList[i].set("0")
                self.varGradeNumberList[i].set(0)

        file.close()

        file = open("climbingGrades.txt", "w")
        for key in routeDict:
            file.writelines(f"{key} {routeDict[key]}\n")

        file.close()






root = Tk()
climbGUI = ClimbingGUI(root)
root.mainloop()