#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Cédric Guyaz"
__date__ = "03 aout 2016"

"""
**********PROJET PENDU**********
WordLetter.py : Les classes contenant le mot à trouver
			 et les constituants du mot à trouver (Word, Letter)
GamePendu.py : La mécanique interne du jeu (GamePendu)
GraphicInterfacePendu.py : L'interface graphique (GraphicInterfacePendu)
Instructions.txt : Les instructions du jeu (en lecture seulement)
WordsList.txt : La liste de mot d'où l'ordinateur choisit un mot (en lecture seulement)
History.txt : L'historique des parties jouées (lecture et écriture)
BackgroundGame.png : le fond d'écran de l'interface graphique
"""

from tkinter import *
from PIL import ImageTk
import GamePendu
import sys


class GraphicInterfacePendu:

	def __init__(self, root):

		self.root = root
		self.width_root = 1000
		self.height_root = 650
		self.root.geometry("{}x{}+183+20".format(self.width_root, self.height_root))
		self.root.maxsize(1000, 650)
		self.root.title("Python Pendu")
		self.widgets = []
		self.game_won = False
		self.game_lost = False


		self.canvas_background = Canvas(width = self.width_root, height = self.height_root)
		self.image_background = PhotoImage(file = "BackgroundGame.png")
		self.canvas_background.pack(expand = YES, fill = BOTH)
		self.canvas_background.create_image(0, 0, image = self.image_background, anchor = "nw")
		self.label_author = self.canvas_background.create_text((self.width_root, self.height_root), 
			text = "Par C. Guyaz ", fill = "black", anchor = SE)

		self.frame_buttons_menu = Frame(self.root, height = self.height_root*0.32, width = self.width_root*0.2, 
			borderwidth = 1)
		self.button_one_player = Button(self.frame_buttons_menu, text = "Un joueur", 
			command = self.command_button_game_1_player)
		self.button_two_players = Button(self.frame_buttons_menu, text = "Deux joueurs", 
			command = self.command_button_game_2_players)
		self.button_history = Button(self.frame_buttons_menu, text = "Historique des parties", 
			command = self.command_button_history)
		self.button_quit = Button(self.frame_buttons_menu, text = "Quitter", command = sys.exit)
		self.buttons = [self.button_one_player, self.button_two_players, self.button_history, self.button_quit]		
		for element in self.buttons:
			element.config(relief = RIDGE, height = 2, bg = "#3096AC", font=("Arial",12,"bold"), borderwidth = 0.5)

		self.frame_stats_game_menu = Frame(self.root, height = self.height_root*0.14, width = self.width_root*0.3, 
			borderwidth = 2, bg = "#C33446", highlightbackground = "black", highlightthickness = 1)		
		self.label_tries = Label(self.frame_stats_game_menu, bg = "#C33446", fg = "#F3F3F3", 
			font = ("Arial", 12, "bold"), text = "Nombre d'essais : 0" )
		self.label_errors = Label(self.frame_stats_game_menu, bg = "#C33446", fg = "#F3F3F3", 
			font = ("Arial", 12, "bold"), text = "Nombre d'erreurs : 0")
		self.label_letters_tried = Label(self.frame_stats_game_menu, bg = "#C33446", fg = "#F3F3F3", 
			font = ("Arial", 12, "bold"), text = "Lettres tentées : Aucune")			

		self.frame_word_input = Frame(self.root, height = self.height_root*0.2, width = self.width_root*0.35, 
			borderwidth = 1, bg = "#C33446", highlightbackground = "black", highlightthickness = 1)	
		self.label_word = Label(self.frame_word_input, bg = "#C33446", fg = "#F3F3F3", 
			font = ("Arial", 30, "bold"), text = "Mot")
		self.label_entry_precisions = Label(self.frame_word_input, bg = "#C33446", 
			font = ("Arial", 9), text = "Entrez une lettre :" )
		self.button_confirm = Button(self.frame_word_input, text = "Confirmer", command = self.command_button_confirm, 
			font = ("Arial", 9), relief = FLAT, bg = "#C33446")
		self.entry_game = Entry(self.frame_word_input, font = ("Arial", 9), relief = GROOVE)

		self.frame_back_instruction = Frame(self.root)
		self.button_back = Button(self.frame_back_instruction, text = "Retour", font = ("Arial", 9), 
			relief = FLAT, bg = "#EDA16D")
		self.button_instructions = Button(self.frame_back_instruction, text = "Instructions", 
			font = ("Arial", 9), relief = FLAT, bg = "#EDA16D")
		self.button_back.pack(side = LEFT)

		self.frame_instructions = Frame(self.root, width = 0.7*self.width_root, height = 0.7*self.height_root)
		self.text_instructions = Text(self.frame_instructions, bg = "#BAECA3", fg = "black", font = ("Arial", 15))

		self.text_history = Text(self.root, bg = "#BAECA3", fg = "black", font = ("Arial", 15))

		self.principal_menu()


	def principal_menu(self):

		self.remove_widgets()
		self.root.unbind("<Return>")
		self.root.bind("<Escape>", lambda _: self.command_button_back(self.principal_menu))

		self.title = self.canvas_background.create_text((0.45*self.width_root, 0.25*self.height_root), 
			text = "Python Pendu!", font =("Arial",35,"bold"), fill = "#C33446" )
		self.frame_buttons_menu.place(relx = 0.86, rely = 0.6, anchor = CENTER)
		self.add_active_widgets(self.frame_buttons_menu)
		for element in self.buttons:
			element.pack(side = TOP, fill = X, expand = 1)


	def game_menu(self):

		self.remove_widgets()
		self.root.bind("<Return>", self.command_button_confirm)
		self.root.bind("<Escape>", lambda _: self.command_button_back(self.principal_menu))
		self.entry_game.focus_set()		


		self.frame_stats_game_menu.place(relx = 0.07, rely = 0.05)
		self.frame_stats_game_menu.pack_propagate(0)
		self.add_active_widgets(self.frame_stats_game_menu)
		self.label_tries.pack(side = TOP)
		self.label_errors.pack(side = TOP)
		self.label_letters_tried.pack(side = TOP)
	
		self.frame_word_input.place(anchor = CENTER, relx = 0.5, rely = 0.5)
		self.frame_word_input.pack_propagate(0)
		self.add_active_widgets(self.frame_word_input)
		self.label_word.pack(side = TOP, expand = 1, fill = BOTH)
		self.entry_game.pack(side = TOP)
		self.label_entry_precisions.pack(side = TOP)
		self.button_confirm.pack()

		self.frame_back_instruction.place(relx = 0.01, rely = 0.95)
		self.add_active_widgets(self.frame_back_instruction)
		self.button_instructions.pack(side = LEFT)
		self.button_back.config(command = lambda: self.command_button_back(self.principal_menu))


	def command_button_game_1_player(self):

		try:
			self.game.__del__()
		except Exception:
			pass

		self.entry_game.config(state = NORMAL)
		self.button_confirm.config(state = NORMAL)
		self.label_entry_precisions.config(text = "Entrez une lettre :")
		self.button_instructions.config(command = lambda: self.command_button_instructions(True))		
		self.game_menu()
		self.game = GamePendu.GamePendu(1)
		self.label_word.config(text = self.game.get_key_word())
		self.choose_word = False


	def command_button_game_2_players(self):

		try:
			self.game.__del__()
		except Exception:
			pass

		self.entry_game.config(state = NORMAL)
		self.button_confirm.config(state = NORMAL)
		self.button_instructions.config(command = lambda: self.command_button_instructions(False))
		self.label_entry_precisions.config(text = "Joueur 1, entrez un mot :")
		self.label_word.config(text = "Python Pendu")
		self.game_menu()
		self.choose_word = True


	def command_button_confirm(self, event = None):

		self.data_entry = self.entry_game.get()
		self.entry_game.delete(0, END)

		try:
			self.game_won, self.game_lost = self.game.game_status()
		except AttributeError:
			pass

		if self.choose_word == True:

			if self.data_entry.isalpha() == True and len(self.data_entry) <= 12:
				self.game = GamePendu.GamePendu(2, self.data_entry)
				(self.game_won, self.game_lost) = self.game.game_status()
				self.label_entry_precisions.config(text = "Entrez une lettre :")
				self.label_word.config(text = self.game.get_key_word())
				self.choose_word = False
			else:
				self.label_entry_precisions.config(text = "Entrez un mot valide s'il vous plait :")

		elif (self.game.try_letter(self.data_entry) == False and
			self.game_won == False and
			self.game_lost == False):

			self.label_entry_precisions.config(text = "Entrez une lettre valide s'il vous plait :")

		elif (self.game_won == False and self.game_lost == False):

			self.game.try_letter(self.data_entry)
			self.label_entry_precisions.config(text = "Entrez une lettre :")
			self.label_word.config(text = self.game.get_key_word())
			(self.tries, self.errors, self.every_letters_tried) = self.game.get_game_stats()
			self.label_tries.config(text = "Nombre d'essais : {}".format(self.tries))
			self.label_errors.config(text = "Nombres d'erreurs : {}".format(self.errors))
			self.label_letters_tried.config(text = "Lettres tentées : {}".format(self.every_letters_tried))

			(self.game_won, self.game_lost) = self.game.game_status()
			if self.game_won == True:
				self.label_entry_precisions.config(text = "Vous avez gagné!")
				self.entry_game.config(state = DISABLED)
				self.button_confirm.config(state = DISABLED, disabledforeground = "black")
				self.game.write_history()

			elif self.game_lost == True:
				self.label_entry_precisions.config(text = "Vous avez perdu!")
				self.label_word.config(text = self.game.reveal_word())
				self.entry_game.config(state = DISABLED)
				self.button_confirm.config(state = DISABLED, disabledforeground = "black")
				self.game.write_history()


	def command_button_back(self, window_to_build):

		self.remove_widgets()
		if window_to_build != self.game_menu:
			self.button_instructions.pack_forget()
		window_to_build()


	def command_button_history(self):

		self.remove_widgets()
		self.text_history.config(state = NORMAL)
		self.text_history.delete('1.0', END)
		self.text_history.insert(END, "Historique des parties jouées:\n\n")


		self.readable_history = []
		self.history_file = open("History.txt", "r")
		self.history_lines = self.history_file.readlines()
		if len(self.history_lines) >= 20:
			for element in self.history_lines[-20:]:
				self.readable_history.append(element)
		else:
			for element in self.history_lines:
				self.readable_history.append(element)
		self.history_file.close()

		self.text_history.place(relx = 0.5, rely = 0.5, anchor = CENTER)
		self.add_active_widgets(self.text_history)
		i = 0
		for line in self.readable_history:
			self.text_history.insert(END, self.readable_history[i])
			i += 1
		self.text_history.config(state = DISABLED)
		self.frame_back_instruction.place(relx = 0.01, rely = 0.95)
		self.add_active_widgets(self.frame_back_instruction)
		self.button_back.pack(side = LEFT)
		self.button_back.config(command = lambda: self.command_button_back(self.principal_menu))


	def command_button_instructions(self, mode):

		self.mode = mode
		self.command_button_back(self.remove_widgets)
		self.root.bind("<Escape>", lambda _: self.command_button_back(self.game_menu))
		self.button_back.config(command = lambda: self.command_button_back(self.game_menu))


		self.frame_instructions.place(relx = 0.5, rely = 0.5, anchor = CENTER)
		self.add_active_widgets(self.frame_instructions)
		self.text_instructions.pack(side = TOP)
		self.file_instruction = open("Instructions.txt", "r")
		self.lines_instruction = self.file_instruction.readlines()
		self.skip_first_part = True
		if self.mode == True: #solo
			for lines in self.lines_instruction:
				if "Bon jeu" not in lines:
					self.text_instructions.insert(END, lines)
				else:
					self.text_instructions.insert(END, lines)
					break

		elif self.mode == False: #duo
			for lines in self.lines_instruction:
				if self.skip_first_part == False:
					self.text_instructions.insert(END, lines)

				if "Bon jeu" in lines:
					self.skip_first_part = False

		self.text_instructions.config(state = DISABLED)
		self.file_instruction.close()
		self.frame_back_instruction.place(relx = 0.01, rely = 0.95)
		self.add_active_widgets(self.frame_back_instruction)


	def active_widgets(self):

		return self.widgets


	def add_active_widgets(self, widget):

		self.widgets.append(widget)


	def remove_widgets(self):

		if self.widgets == []:
			return None
		else:
			for element in self.widgets:
				self.widgets.remove(element)
				element.place_forget()
				self.canvas_background.itemconfigure(self.title, state = HIDDEN)





if __name__ == "__main__":
	
	root = Tk()
	app = GraphicInterfacePendu(root)
	root.mainloop()