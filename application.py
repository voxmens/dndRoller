#!/usr/bin/env python2

import pygtk
pygtk.require('2.0')
import gtk
from diceRoller import dice

class Die:
	def callback(self, widget, callback_data=None):
		if self.__variable:
			self._die.setSides(int(self._Sides.get_text()))
		tempResult = 0
		for i in range(int(self._Number.get_text())):
			tempResult += self._die.roll()
		if self._RadioAdd.get_active():
			self._Result.set_text(str(tempResult + int(self._Modifier.get_text())))
		elif self._RadioSub.get_active():
			self._Result.set_text(str(tempResult - int(self._Modifier.get_text())))


	def __init__(self, sides=2, image='', showImage=True, variable=False):
		self.__variable = variable
		self.__showImage = showImage
		if self.__variable:
			self._Sides = gtk.Entry(max=3)
			self._Sides.set_width_chars(3)
			self._Sides.set_text('1')
		elif self.__showImage:
			self._Image = gtk.Image()
			self._Image.set_from_file(image)
		# Initialize the die
		self._die = dice.Dice(sides)
		# Setup the number box
		self._Number = gtk.Entry(max=3)
		self._Number.set_width_chars(3)
		self._Number.set_alignment(1)
		# Set the number text
		self._Number.set_text('1')
		# Set the input label
		if self.__variable:
			self._NumberLabel = gtk.Label('dx')
		else:
			self._NumberLabel = gtk.Label('d' + str(sides))
		self._NumberLabel.set_alignment(0, 0.5)
		# Radio buttons
		self._RadioAdd = gtk.RadioButton(None, "+")
		self._RadioSub = gtk.RadioButton(self._RadioAdd, "-")
		self._RadioBox = gtk.HButtonBox()
		self._RadioBox.set_homogeneous(True)
		self._RadioBox.set_layout(gtk.BUTTONBOX_END)
		# Button box
		self._RadioBox.pack_start(self._RadioAdd, False, True, 0)
		self._RadioBox.pack_start(self._RadioSub, False, True, 0)
		# Modifier
		self._Modifier = gtk.Entry(max=3)
		self._Modifier.set_width_chars(3)
		self._Modifier.set_text('0')
		self._Modifier.set_alignment(1)
		# Roll button
		self._Roll = gtk.Button(label="Roll")
		self._Roll.connect("clicked", self.callback)

		# Result box
		self._Result = gtk.Entry(max=0)
		self._Result.set_width_chars(10)
		self._Result.set_alignment(1)
		self.NumberPosition = self._Number
		self.NumberLabelPosition = self._NumberLabel
		self.AddSubPosition = self._RadioBox
		self.ModifierPosition = self._Modifier
		self.RollPosition = self._Roll
		self.ResultPosition = self._Result
		if self.__variable:
			self.ImagePosition = self._Sides
		else:
			self.ImagePosition = self._Image
		self.rowStuff = [self.ImagePosition, self.NumberPosition, self.NumberLabelPosition,
						 self.AddSubPosition, self.ModifierPosition, self.RollPosition,
						 self.ResultPosition]

	def show(self):
		if self.__variable:
			self._Sides.show()
		self._Number.show()
		self._NumberLabel.show()
		self._RadioAdd.show()
		self._RadioSub.show()
		self._RadioBox.show()
		self._Modifier.show()
		self._Roll.show()
		self._Result.show()

	def reset(self):
		if self._variable:
			self._Sides.set_text('1')
		self._Number.set_text('1')
		self._Modifier.set_text('0')
		self._Result.set_text('')
		self._RadioAdd.set_active(True)

class DnDRoller:
	def delete_event(self, widget, event, data=None):
		gtk.main_quit()
		return False

	def tableAttach(self, attachments, top=0, bottom=1, start=0, end=1, fillsRow=False):
		if fillsRow:
			self.mainTable.attach(attachments[0], left_attach=0, right_attach=self.mainTableCols,
								  top_attach=top, bottom_attach=bottom, xoptions=gtk.FILL,
								  yoptions=gtk.FILL, xpadding=0, ypadding=0)
		for attachment in attachments:
			self.mainTable.attach(attachment, left_attach=start, right_attach=end, top_attach=top,
							 	  bottom_attach=bottom, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=0, ypadding=0)
			start += 1
			end += 1

	def __init__(self):
		# Initialize the sets
		d4 = Die(sides=4, image='d4a.jpg', variable=False)
		d6 = Die(sides=6, image='d6a.jpg', variable=False)
		d8 = Die(sides=8, image='d8a.jpg', variable=False)
		d10 = Die(sides=10, image='d10a.jpg', variable=False)
		d12 = Die(sides=12, image='d12a.jpg', variable=False)
		d20 = Die(sides=20, image='d20a.jpg', variable=False)
		d100 = Die(sides=100, image='d100a.jpg', variable=False)
		dx = Die(sides=2, showImage=False, variable=True)
		# Create the window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("RPG Dice Roller")

		# Connect the delete_event to the window
		self.window.connect("delete_event", self.delete_event)
		self.window.set_border_width(10)

		# Create a vertical box to pack the horizontal boxes
		self.mainTableCols = 8
		self.mainTableRows = 10
		self.mainTable = gtk.Table(rows=self.mainTableRows, columns=self.mainTableCols, homogeneous=False)
		
		# Initialize the top row labels
		dieLabel = gtk.Label("Die")
		numberLabel = gtk.Label("Number")
		blankLabel = gtk.Label("")
		modifierlabel = gtk.Label("Modifier")
		resultsLabel = gtk.Label("Results")
		separator = gtk.HSeparator()
		quitButton = gtk.Button("Quit")
		quitButton.connect("clicked", lambda w: gtk.main_quit())
		# Pack the labels into the horizontal box
		self.tableAttach([dieLabel, numberLabel, blankLabel, blankLabel,
						  modifierlabel, blankLabel, resultsLabel], 0, 1)
		self.tableAttach([separator], 1, 2, True)
		self.tableAttach([quitButton], self.mainTableRows-1, self.mainTableRows,
						 self.mainTableCols-1, self.mainTableCols)
		# Show the labels
		dieLabel.show()
		numberLabel.show()
		blankLabel.show()
		modifierlabel.show()
		resultsLabel.show()
		separator.show()
		quitButton.show()

		# Setup the d4 row
		self.tableAttach(d4.rowStuff, 2, 3)

		# Setup the d6 row
		self.tableAttach(d6.rowStuff, 3, 4)
		
		#Setup the d8 row
		self.tableAttach(d8.rowStuff, 4, 5)
		
		# Setup the d10 row
		self.tableAttach(d10.rowStuff, 5, 6)
		
		# Setup the d12 row
		self.tableAttach(d12.rowStuff, 6, 7)
		
		# Setup the d20 row
		self.tableAttach(d20.rowStuff, 7, 8)
		
		# # Setup the d100 row
		self.tableAttach(d100.rowStuff, 8, 9)

		# # Setup the dx row
		self.tableAttach(dx.rowStuff, 9, 10)

		# Show all the elements
		d4.show()
		d6.show()
		d8.show()
		d10.show()
		d12.show()
		d20.show()
		d100.show()
		dx.show()
		self.window.add(self.mainTable)
		self.mainTable.show()
		self.window.show()

def main():
	DnDRoller()
	gtk.main()
	return 0

if __name__ == '__main__':
	main()