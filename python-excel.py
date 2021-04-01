from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import csv
import os
try:
	import matplotlib.pyplot as plt
except Exception as e:
	messagebox.showerror("Error", "you need to install matplotlib first")
	exit()
	





class tabButton:

		tabArray = []

		def __init__(self, fileCSV):
			global tabs
			self.name = fileCSV.name
			self.CSV = fileCSV
			self.buttonFrame = Frame(tabs)
			self.openButton = Button(self.buttonFrame, text=self.name, command= self.CSV.makeTable)
			self.closeButton = Button(self.buttonFrame, text="X", command=self.delete)
			self.openButton.pack(side=LEFT)
			self.closeButton.pack(side=RIGHT)
			tabButton.tabArray += [self.buttonFrame]
			tabButton.refresh()

		def delete(self):
			self.CSV.delete()
			tabButton.tabArray.remove(self.buttonFrame)
			self.openButton.pack_forget()
			self.closeButton.pack_forget()
			self.buttonFrame.pack_forget()
			tabButton.refresh()
			self = None	

		@staticmethod
		def refresh():
			global tabs

			i = 0
			for item in tabButton.tabArray:
				item.grid(row=0, column=i)
				i += 1
			# tabsCanvas.pack()


class fileCsv:

	def __init__(self, getAddress):
		
		self.panel = None
		self.isSaved = True
		self.address = getAddress
		self.name = functions.getName(self.address)

		# error file ham esm
		if self.name in allFiles:
			raise NameError('A file with same name is already open')

		# error file ba esme najoor
		for c in " ()":
			if c in self.name:
				raise NameError("filename contains \'"+c+"\'")

		self.f = open(self.address, encoding="utf8")

		# b soorate csv khoonde mishe va tuye ye objecte csv zakhire mishe
		self.csvFile = csv.reader(self.f, delimiter=",")

		# yek araye az satr ha sakhte mishe
		self.array = []
		for row in self.csvFile:
			tmp = []
			for item in row:
				tmp += [item]
			self.array += [tmp[:]]

		# ye objecte tabButton sakhte mishe k oon buttone zire jadval ro misaze
		self.tabB = tabButton(self)

		#  khode jadval ro mikeshe
		self.makeTable()

		


	def __str__(self):
		s = ""
		for row in self.array:
			s += ",".join(row)
			s += "\n"
		return s

	def delete(self):
		global root, currentTable
		self.array = []
		self.f.close()
		self.panel = None
		currentTable = Frame(tableCanv)
		del allFiles[self.name]


		tableCanv.delete("all")
		tableCanv.create_window(0,0,window=currentTable, anchor='nw')
		root.title("my app")
		root.update()
		tableCanv.config(scrollregion=tableCanv.bbox("all"))




	def makeChangeArray(self, x, y):
		def func(event):
			# print(event)
			self.isSaved = False
			self.updateTitle()
			if (event.state==8 or event.state==9) and not (event.keysym in ["BackSpace"]):
				self.array[x][y] = (event.widget.get()+event.char)
			elif event.keysym=="BackSpace":
				if event.widget.get()!="":
					self.array[x][y] = event.widget.get()[:-1]
			else:
				self.array[x][y] = event.widget.get()
		return func

	def deleteRow(self, row):
		def func():
			self.array.remove(self.array[row])
			self.makeTable()
		return func

	def addRow(self, row):
		def func():
			if len(self.array)>0:
				self.array = self.array[:row] + [["" for i in self.array[0]]] + self.array[row:]
			else:
				self.array.add([""])
			self.makeTable()
		return func

	def deleteCol(self, col):
		def func():
			# print("deleteCol ", col)
			for i in range(len(self.array)):
				# print("i ", i)
				self.array[i] = self.array[i][:col]+self.array[i][col+1:]
			if len(self.array)>0:
				if len(self.array[0])==0:
					self.array = []

			self.makeTable()
		return func

	def addCol(self, col):
		def func():
			for i in range(len(self.array)):
				self.array[i] = self.array[i][:col] + [""] + self.array[i][col:]
			self.makeTable()
		return func

	def getCol(self, title):
		retArray = []
		if len(self.array)>1:
			res = -1
			for i in range(len(self.array[0])):
				if self.array[0][i]==title:
					res = i
					break
			if res==-1:
				return []
			for i in range(1, len(self.array)):
				retArray += [self.array[i][res]]
		return retArray




	def updateTitle(self):
		global root
		if self.isSaved:
			root.title(self.name)
		else:
			root.title(self.name+"*")


	def makeTable(self):
		global table, currentTable, root, tableCanv

		self.panel = Frame(tableCanv)

		if len(self.array)==0:
			tmpFrame = Frame(self.panel)
			def addR():
				self.array += [[""]]
				self.makeTable()
			Button(tmpFrame, text="add row", command=addR).pack()
			tmpFrame.grid(row=0, column=0)
		else:
			for i in range(len(self.array[0])):
				tmpFrame = Frame(self.panel)
				Button(tmpFrame, text="+ bfr", command=self.addCol(i)).pack(side=LEFT)
				Button(tmpFrame, text="+ aft", command=self.addCol(i+1)).pack(side=LEFT)
				Button(tmpFrame, text="del", command=self.deleteCol(i)).pack(side=LEFT)
				tmpFrame.grid(row=0, column=i+1)

		for i in range(len(self.array)):

			tmpFrame = Frame(self.panel)
			Button(tmpFrame, text="+ bfr", command=self.addRow(i)).pack(side=LEFT)
			Button(tmpFrame, text="+ aft", command=self.addRow(i+1)).pack(side=LEFT)
			Button(tmpFrame, text="del", command=self.deleteRow(i)).pack(side=LEFT)
			tmpFrame.grid(row=i+1, column=0)

			for j in range(len(self.array[i])):
				tmp = Entry(self.panel)
				tmp.insert(END, self.array[i][j])
				tmp.grid(row=i+1, column=j+1)
				tmp.bind(sequence="<KeyPress>", func=self.makeChangeArray(i,j) )

		
		if currentTable!=None:
			currentTable = None
		currentTable = self.panel

		root.bind(sequence="<Control-s>", func=self.saveFile)


		tableCanv.delete("all")
		tableCanv.create_window(0,0,window=currentTable, anchor='nw')

		root.update()
		tableCanv.config(scrollregion=tableCanv.bbox("all"))

		self.updateTitle()


	def saveFile(self, event):

		if self.isSaved:
			return
		# file baz mishe baraye "write"
		output = open(self.address, "w", encoding="utf8")

		# ye objecte "csv writer" sakhte mishe baraye oon file
		writer = csv.writer(output,delimiter=",", lineterminator='\n')

		# oon writeri k sakhtim ye araye az satr ha migire va oonjoori k mikhaym zakhire mikone (joziatesh ro khodesh handle mikone)
		writer.writerows(self.array)
		output.close()

		self.isSaved = True
		self.updateTitle()

		pass


class functions:

	@staticmethod
	def getFileAddress():
		while True:
			filename =  filedialog.askopenfilename(initialdir = ".",title = "Select csv file",filetypes = (("csv files","*.csv"),))
			if filename==None or filename=="":
				return ""
			if len(filename)>4 and filename[-4:]==".csv":
				return filename

	@staticmethod
	def openCsvFile():
		name = functions.getFileAddress()
		if name!="":
			try:
				tmp = fileCsv(name)
				allFiles[tmp.name] = tmp
			except Exception as e:
				messagebox.showerror("Error", "some error occured during opening file\nhere's some more information: \n\n"+str(e))
			
			# add to tabs
	@staticmethod
	def getName(address):
		return os.path.splitext(os.path.basename(address))[0]

	@staticmethod
	def run(event=None):
		try:
			cmdStr = commandLine.get()
			cmd = cmdStr.split(" ")
			op = cmd[0]
			if op=="plot":
				first = cmd[1].split("(")
				first[1] = first[1][:-1]
				second = cmd[2].split("(")
				second[1] = second[1][:-1]
				xlabel = cmd[3][1:-1]
				ylabel = cmd[4][1:-1]
				title = cmd[5][1:-1]
				x = allFiles[first[0]].getCol(first[1])
				y = allFiles[second[0]].getCol(second[1])
				
				functions.plot(x,y,xlabel,ylabel,title)


			elif op=="hist":
				first = cmd[1].split("(")
				first[1] = first[1][:-1]
				title = cmd[2][1:-1]

				y = allFiles[first[0]].getCol(first[1])
				functions.hist(y, title)
			else:

				raise NameError("\'"+op+"\' operation not defined")

		except Exception as e:
			messagebox.showerror("Error", "Wrong input\nhere's some more info:\n"+str(e))
			raise
		

	@staticmethod
	def plot(xx, yy, xlabel, ylabel, title):

		if plt != None:
			plt.close('all')

		x = []
		y = []
		try:
			x = [float(i) for i in xx]
			y = [float(i) for i in yy]
		except Exception as e:
			messagebox.showerror("error!", "Column includes non number elements")
			return


		plt.plot(x,y,"ro")
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.title(title)
		plt.show()

	@staticmethod
	def hist(xx, title):

		if plt != None:
			plt.close('all')

		x = []
		try:
			x = [float(i) for i in xx]
		except Exception as e:
			messagebox.showerror("error!", "Column includes non number elements")
			return


		mn = min(x)
		mx = max(x)
		d = (mx - mn)/10.0
		if d>1:
			d = round(d)

		y = []
		i = mn-d
		while i<=mx+d:
			y += [i]
			i += d


		print("x, y: ",x,y)
		plt.hist(x, histtype='bar', rwidth=0.8)
		plt.title(title)
		plt.show()



allFiles = {}

# help(plt.plot)

# GUI

root = Tk()

root.title("my app")

main = Frame(root, bg="white", padx=10, pady=10)
main.pack(fill=BOTH, side=TOP, expand=TRUE)

table = Frame(main, bg="gray")
table.pack(fill=BOTH, side=TOP, expand=TRUE)

#####

vscrollbar = Scrollbar(table, orient=VERTICAL)
hscrollbar = Scrollbar(table, orient=HORIZONTAL)


tableCanv = Canvas(table, bg="white", yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)

vscrollbar.config(command=tableCanv.yview)
vscrollbar.pack(side=RIGHT, fill=Y)

hscrollbar.config(command=tableCanv.xview)
hscrollbar.pack(side=BOTTOM, fill=X)

currentTable = Frame(tableCanv)

tableCanv.pack(fill=BOTH, expand=True)
tableCanv.create_window(0,0,window=currentTable, anchor='nw')


root.update()
tableCanv.config(scrollregion=tableCanv.bbox("all"))

#####

tabs = Frame(main, padx=10)
tabs.pack(fill=X)

footer = Frame(root, padx=10, pady=10)
footer.pack(side=BOTTOM, fill=X)

runBar = Frame(footer, padx=10)


commandLine = Entry(runBar)
runButton = Button(runBar, text="Run", command=functions.run)
runButton.pack(side=RIGHT)
commandLine.pack(fill=X)

inputButton = Button(footer, text="Open File", command=functions.openCsvFile)
inputButton.pack(side=LEFT)

runBar.pack(fill=X)
runBar.bind(sequence="<Return>", func=functions.run )

root.mainloop()
