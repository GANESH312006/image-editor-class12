import customtkinter as ctk 
from customtkinter import CTkImage
from toolTip import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from settings import *

class Panel(ctk.CTkFrame):
  def __init__(self, parent):
    super().__init__(master = parent, fg_color = "#1f1c1c", corner_radius  = 1)
    self.pack(fill = 'x', pady = 4, ipady = 8)

class SliderPanel(Panel):
  def __init__(self, parent, text, dataVar, minVal, maxVal):
    super().__init__(parent = parent,) # parent in lhs is the parent in parameter of the Panel class 
    
    # geometry 
    self.rowconfigure(index = (0, 1), weight = 1)
    self.columnconfigure(index = (0, 1), weight = 1)
    
    self.dataVar=dataVar
    self.dataVar.trace('w',self.updateText)
    
    ctk.CTkLabel(self, text = text, bg_color = 'transparent').grid(row = 0, column = 0, sticky = 'w', padx = 7)
    self.numLabel = ctk.CTkLabel(self, text = dataVar.get())
    self.numLabel.grid(row = 0, column = 1, sticky = 'e', padx = 7)
    
    ctk.CTkSlider(
      self, 
      fg_color = "#d83782", 
      hover = True,
      variable = self.dataVar,
      from_ = minVal, 
      to = maxVal, 
      progress_color = '#f72585', 
      button_color = '#a977e7', 
      button_hover_color = '#6b5685',
      height = 16
      ).grid(row = 1, column = 0, columnspan = 2, sticky = 'ew', padx = 5, pady = 5)
    
    
  def updateText(self, *args):
    self.numLabel.configure(text = f'{round(self.dataVar.get(), 2)}')
    
class FileNamePanel(Panel):
  def __init__(self, parent, nameStr, fileStr):
    super().__init__(parent = parent)
    
    self.fileStr = fileStr
    self.nameStr = nameStr # weird otter -> weird_otter
    self.nameStr.trace('w', self.updateText)
    
    self.entry = ctk.CTkEntry(self, textvariable = self.nameStr,).pack(fill = 'x', padx = 20, pady = 20)
    frame = ctk.CTkFrame(self, fg_color = 'transparent')
    
    jpgCheck = ctk.CTkCheckBox(
      frame, 
      text = 'jpg', 
      variable = self.fileStr, 
      onvalue = 'jpg', 
      offvalue = 'png', 
      command = lambda:self.click('jpg'), 
      hover = True,
      fg_color = '#ff2285', 
      checkmark_color = '#f7f7f7', 
      hover_color = '#3b3639'
      )
    jpgCheck.pack(side = 'left', fill = 'x', expand = True)
    
    pngCheck = ctk.CTkCheckBox(
      frame, 
      text = 'png', 
      variable = self.fileStr, 
      onvalue = 'png', 
      offvalue = 'jpg', 
      command = lambda:self.click('png'),
      hover = True, 
      fg_color = '#ff2285', 
      checkmark_color = '#f7f7f7', 
      hover_color = '#3b3639', 
      )
    pngCheck.pack(side = 'left', fill = 'x', expand = True)
    
    frame.pack(expand = True, fill = 'x', padx = 20)
    
    self.output = ctk.CTkLabel(self, text = '')
    self.output.pack()
  
  def updateText(self, *args):
    if (self.nameStr.get()):
      text = self.nameStr.get().replace(' ', '_') + '.' + self.fileStr.get()  # has white space, like weird otter, first arg is the char we wanna replace, in this use case it is the white space, and second arg is the char we wanna replace with, in this case it is the underscore
      self.output.configure(text = text)
      
  def click(self, value):
    self.fileStr.set(value)
    self.updateText()
  
class SegmentPanel(Panel):
  def __init__(self, parent, text, dataVar, options):
    super().__init__(parent = parent)
    ctk.CTkLabel(self, text = text).pack()
    ctk.CTkSegmentedButton(
        self, 
        variable = dataVar, 
        values = options, 
        selected_color = '#332525', 
        selected_hover_color = '#221a1a', 
        unselected_hover_color = '#5a5a5a',
        dynamic_resizing = True
      ).pack(expand = True, fill = 'both', padx = 4, pady = 4)

class Switchpanel(Panel):
  def __init__(self,parent,*args):
    super().__init__(parent=parent)
    for var, text in args:
      switch = ctk.CTkSwitch(
        self, 
        text = text, 
        variable = var, 
        button_color = PURPLE, 
        fg_color = SLIDER_BG, 
        progress_color = '#42474b', 
        border_color = '#332525', 
        button_hover_color = '#6b5685'
        )
      switch.pack(side='left', expand=True, fill="both", padx=5,pady=5)

class Dropdownpanel(ctk.CTkOptionMenu):
  def __init__(self, parent, data_var, options):
    super().__init__(
      master = parent, 
      values = options,
      fg_color = DROPDOWN_MAIN_COLOR,
      button_hover_color = DROPDOWN_HOVER_COLOR,
      dropdown_fg_color = 'white',
      dropdown_hover_color = '#0078D7',
      button_color = '#3a2a2a',
      hover = True,
      corner_radius = 8, 
      variable = data_var, 
      dropdown_text_color = 'black', 
    )
    self.pack(fill = 'x',pady = 8, padx = 6)

class Revertbtn(ctk.CTkButton):
  def __init__(self,parent,*args):
    # images 
    self.ctkImage = ctk.CTkImage(
      light_image = Image.open('Images\\back (1).png'), 
      dark_image = Image.open('Images\\backward.png')
    )
    super().__init__(
      master=parent,
      text='Revert',
      command=self.revert, 
      hover_color ="#d10d65", 
      fg_color = "#ff2285", 
      image = self.ctkImage
    )
    
    # tooltip 
    Tooltip(self, text = 'Press To Revert The Changes')
    
    self.pack(side = 'bottom',pady = 10)
    self.args = args
  
  def revert(self):
    for var, value in self.args:
      var.set(value)

class FilePathPanel(Panel):
  def __init__(self, parent, pathStr):
    super().__init__(parent = parent)
    self.pathStr = pathStr
    
    # ctk Image
    self.imageBtn = ctk.CTkImage(
      light_image = Image.open('Images\\case-file.png'), 
      dark_image = Image.open('Images\\case-file.png')
    )
    
    self.openExplorer = ctk.CTkButton( 
      self, 
      text = 'Open Explorer', 
      command = self.openFileDiag, 
      hover_color = '#d10d65', 
      fg_color = '#ff2285',
      image = self.imageBtn, 
      )
    self.openExplorer.pack(pady = 5)
    
    # tooltip 
    Tooltip(self.openExplorer, text = 'Press To Open The File Explorer')
    
    # entry
    entry = ctk.CTkEntry(self, textvariable = self.pathStr)
    entry.pack(expand = True, fill = 'both', padx = 5, pady = 5)
    
  
  def openFileDiag(self):
    self.pathStr.set(filedialog.askdirectory())

class SaveBtn(ctk.CTkButton):
  def __init__(self, parent, exportImg, nameStr, fileStr, pathStr):
    
    # ctk Image
    self.imageBtn = ctk.CTkImage(
      light_image = Image.open('Images\\diskette.png'), 
      dark_image = Image.open('Images\\diskette.png')
    )
    
    super().__init__(
      master = parent, 
      text = 'Save', 
      command = self.save, 
      hover = True, 
      hover_color = '#d10d65', 
      fg_color = '#ff2285', 
      image =  self.imageBtn
      )
    
    # tooltip 
    Tooltip(self, text = 'Press To Save The Image (Ctrl+s)')
    

    self.exportImage = exportImg
    self.nameStr = nameStr
    self.fileStr = fileStr
    self.pathStr = pathStr
    
    # run
    self.pack(side = 'bottom', pady = 10)
  
  def save(self):
    self.exportImage(
    self.nameStr.get(),
    self.fileStr.get(),
    self.pathStr.get()
    )
