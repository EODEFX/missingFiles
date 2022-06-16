# The missingFiles function will only work on file sequences that are structured as
# fileName.####.ext with the hashes being the frame numbers. The frame numbers can be
# padded to any length.

# The first argument is the exact directory path you want to check, the second argument
# is how many frames the sequence is supposed to be, and the third argument is the first
# frame of the sequence. The last argument is optional and allows you to specify a specific
# file name to search for, i.e. you have more than one set of passes in one folder.

# Change to the directory you want to check, the 'r' before the string will read it as Literal and
# allow for special characters, such as back slash '\'.

#path=r'C:\Users\ry101290\desktop\compositing\shots\shot62\env'
#missingFiles(path,216,460,"shot62_env_colorAOVs")

#path=r'C:\Users\ry101290\desktop\compositing\shots\shot62\data'
#missingFiles(path,216,460,'shot62_data') # Our Ambient Occlusion pass in the beauty output
#missingFiles(path,216,460,'shot62_data_data')
#missingFiles(path,216,460,'shot62_data_matteIDs')
#missingFiles(path,216,460,'shot62_data_world')

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

#main Tkinter window call
main = Tk()
main.title('Check Missing Frames')
main.geometry('700x500-0-25')
#main.resizable(FALSE,FALSE)

strFile = StringVar()
strFirst = StringVar()
strLast = StringVar()

def missingFiles():
	import os
	frameNum = int(strLast.get()) - int(strFirst.get()) + 1
	filePath = strFile.get()
	frameFirst = int(strFirst.get())
	fileSplit = filePath.split('/')
	fileName = fileSplit[len(fileSplit)-1]
	fileSplit = fileSplit[0:(len(fileSplit)-1)]
	filePath = '/'.join(fileSplit)
	fileLt = os.listdir(filePath) #File List, including directories
	fullLt = [] #Full List
	partLt = [] #Partial List
	#print(fileName)
	
	for i in range(frameNum): #set for how many frames you're supposed to have
		fullLt.append(i + frameFirst) #set for your first frame
	#print(fullLt)

	for file in fileLt:
		if len(file.split('.')) > 1: #ignores directories
			#print(file.split('.')[0])
			#print(fileName)
			if file.split('.')[0] == fileName.split('.')[0]: #check the file name
				#print(file.split('.')[1])
				partLt.append(int(file.split('.')[1])) #only take the frame number, and take it as an integer

	missLt = [x for x in fullLt if x not in partLt] #Missing List
	#print(fullLt)
	#print(partLt)
	#print(missLt)
	conLt = [] #Shortened List

	def group(L): #separates consecutive and non-consecutive numbers
		first = last = L[0]
		for n in L[1:]:
			if n - 1 == last: # Part of the group, bump the end
				last = n
			else: # Not part of the group, yield current group and start a new
				if first != last:
					yield str(first)+"-"+str(last) # Yield the last group
				else:
					yield str(last)
				first = last = n
		if first != last:	
			yield str(first)+"-"+str(last) # Yield the last group
		else:
			yield str(last)

	txtList.insert(END, '\n' + filePath + '/' + fileName + '\n')
	if len(missLt) > 0:
		txtList.insert(END, ','.join(map(str,list(group(missLt)))) + '\n')
	else:
		txtList.insert(END, 'None Missing')
	txtList.insert(END, 'Total missing = ' + str(len(missLt)) + '\n')
	print("Ran Missing Files")

frameMain = ttk.Frame(main)
frameMain.grid(sticky="NEWS")

def findFileDialog():
	strReturn = filedialog.askopenfilename()
	if strReturn != "":
		strFile.set(strReturn)
	
def checkFirst(varName,i,oper):
	testFirst = strFirst.get()
	if (testFirst.isdigit() == FALSE and testFirst != ""):
		testFirst = testFirst[slice(len(testFirst)-1)]
		strFirst.set(testFirst)
strFirst.trace("w",checkFirst)
	
def checkLast(varName,i,oper):
	testLast = strLast.get()
	if (testLast.isdigit() == FALSE and testLast != ""):
		testLast = testLast[slice(len(testLast)-1)]
		strLast.set(testLast)
strLast.trace("w",checkLast)

def callMissingFiles():
	frameNum = int(strLast.get()) - int(strFirst.get()) + 1
	missingFiles(strFile.get(),frameNum,int(strFirst.get()))

Label(frameMain, text="File").grid(row=0,sticky=E)
entFile = Entry(frameMain,textvariable=strFile).grid(row=0,column=1,columnspan=3,sticky="EW")

butFile = ttk.Button(frameMain,text="Find File",command=findFileDialog).grid(row=1,column=1,sticky="W")

Label(frameMain, text="First Frame").grid(row=2)
entFirst = Entry(frameMain,textvariable=strFirst).grid(row=2,column=1)
Label(frameMain, text="Last Frame").grid(row=2,column=2)
entLast = Entry(frameMain,textvariable=strLast).grid(row=2,column=3)

butCheck = ttk.Button(frameMain,text="Check Frames",command=missingFiles).grid(row=3,column=1,sticky="W")

txtList = Text(frameMain)
txtList.grid(row=4,columnspan=4,sticky="NEW")
txtScrl = ttk.Scrollbar(frameMain, orient=VERTICAL, command=txtList.yview)
txtScrl.grid(column=4,row=4,sticky='NS')
txtList['yscrollcommand'] = txtScrl.set
frameMain.rowconfigure(4, weight=1)

main.mainloop()
