import customtkinter as ctk 
from AppOpener import open as op
from customtkinter import CTkImage
from tkinter import filedialog as fd
from tkinter import Canvas
from toolTip import *
from PIL import ImageTk
from PIL import Image
from PIL import *
from settings import *

class ImageImport(ctk.CTkFrame):
  def __init__(self, parent, importFunc):
    super().__init__(master = parent, fg_color = "#1f191c")
    self.importFunc = importFunc

    self.openCamBtn = ctk.CTkButton(
      master = self, 
      text = 'Take a Picture', 
      command = lambda : op('camera'), 
      hover_color ="#d10d65", 
      fg_color = "#ff2285", 
      font = ('Merriweather', 15),
    )
    self.openCamBtn.place(x = 350, y = 286)

    self.button = ctk.CTkButton(
      master = self, 
      text = 'Open Image', 
      command = self.openDiag, 
      hover_color ="#d10d65", 
      fg_color = "#ff2285", 
      font = ('Merriweather', 15),
    )
    self.button.place(x = 510, y = 286)
    
    # tooltip 
    Tooltip(self.button, text = 'Press To Open The Image (Ctrl+n)')
    
  def openDiag(self):
    try:
      path = fd.askopenfile().name # type:ignore
      self.importFunc(path)
    except Exception as e:
      print(e)
    
class ImageOutput(ctk.CTkCanvas):
  def __init__(self, parent, resizeImage):
    super().__init__(
      master = parent, 
      background = BACKGROUND, 
      bd = 0, 
      highlightthickness = 0, 
      relief = 'ridge', 
      
      )
    self.bind('<Configure>', resizeImage)
    self.grid(row = 0, column = 1, sticky = 'nsew', padx = 10, pady = 10)
    
class CloseOutput(ctk.CTkButton):
  def __init__(self, parent, command):
    super().__init__(
      master = parent, 
      text = 'X', 
      text_color = WHITE, 
      fg_color = '#423e41', 
      # bg_color = '#2c2910', 
      width = 40, 
      height = 40, # make it as square
      corner_radius = 13, 
      hover_color = CLOSE_RED, 
      command = command
     )
    self.place(relx = 0.99, rely = 0.03, anchor = 'ne')
