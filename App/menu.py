import customtkinter as ctk 
from panels import *

class Menu(ctk.CTkTabview):
  def __init__(self, parent, posVars, colorVars, fxVars, exportImg):
    super().__init__(
      master = parent, 
      bg_color = '#1f1c1c', 
      fg_color = '#292929', 
      segmented_button_selected_color = '#332525', 
      segmented_button_selected_hover_color = '#221a1a', 
      segmented_button_unselected_color = '#616161',
      segmented_button_unselected_hover_color = '#575757'
    )
    self.grid(row = 0, column = 0, sticky = 'nsew', pady = 10, padx = 10)
    
    
    # tabs
    self.add('Position')
    self.add('Color')
    self.add('Effects')
    self.add('Export')
    
    # widgets
    PositionFrame(self.tab('Position'), posVars)
    ColorFrame(self.tab('Color'), colorVars)
    EffectFrame(self.tab('Effects'), fxVars)
    ExportFrame(self.tab('Export'), exportImg)

class PositionFrame(ctk.CTkFrame):
  def __init__(self, parent, posVars):
    super().__init__(master = parent, fg_color = '#1f1c1c')
    self.pack(expand = True, fill = 'both')
    
    SliderPanel(self, 'Rotation', posVars['rotate'], 0, 360) # to get the rotate property
    SliderPanel(self, 'Zoom', posVars['zoom'], 0, 200) # To get the zoom property
    SegmentPanel(self, text = 'Invert', dataVar = posVars['flip'], options = FLIP_OPTIONS)
    Revertbtn(
      self, 
      (posVars['rotate'], ROTATE_DEFAULT),
      (posVars['zoom'], ZOOM_DEFAULT),
      (posVars['flip'], FLIP_OPTIONS[0])
    )

class ColorFrame(ctk.CTkFrame):
  def __init__(self, parent, colorVars):
    super().__init__(master = parent, fg_color = '#1f1c1c')
    self.pack(expand = True, fill = 'both')
    
    Switchpanel(self,(colorVars['grayscale'],'B/W'), (colorVars['invert'],'Invert'))
    SliderPanel(self, 'Brightness', colorVars['brightness'], 0, 5)
    SliderPanel(self, 'Vibrance', colorVars['vibrance'], 0, 5)
    Revertbtn(
      self, 
      (colorVars['grayscale'],GRAYSCALE_DEFAULT),
      (colorVars['brightness'], BRIGHTNESS_DEFAULT),
      (colorVars['invert'], INVERT_DEFAULT),
      (colorVars['vibrance'], VIBRANCE_DEFAULT)
    )

class EffectFrame(ctk.CTkFrame):
  def __init__(self, parent, fxVars):
    super().__init__(master = parent, fg_color = '#1f1c1c')
    self.pack(expand = True, fill = 'both')
    
    Dropdownpanel(self,fxVars['effect'], EFFECT_OPTIONS)
    SliderPanel(self, 'Blur', fxVars['blur'], 0, 30)
    SliderPanel(self, 'Contrast', fxVars['contrast'], 0, 10)
    Revertbtn(
      self, 
      (fxVars['blur'],BLUR_DEFAULT),
      (fxVars['contrast'], CONTRAST_DEFAULT),
      (fxVars['effect'],EFFECT_OPTIONS[0])
    )
    
class ExportFrame(ctk.CTkFrame):
  def __init__(self, parent, exportImage):
    super().__init__(master = parent, fg_color = '#1f1c1c')
    self.pack(expand = True, fill = 'both')
    
    # data
    self.nameStr = ctk.StringVar()
    self.fileStr = ctk.StringVar(value = 'jpg')
    self.pathStr = ctk.StringVar()
    
    lol = FilePathPanel.__dict__
    
    # widgets
    FileNamePanel(self, self.nameStr, self.fileStr)
    FilePathPanel(self, self.pathStr)
    SaveBtn(self, exportImage, self.nameStr, self.fileStr, self.pathStr)
    
    self.saveLabel = ctk.CTkLabel(
      master = self, 
      text = 'Saved!',
      font = ('sans-serif', 16)
    )
    self.saveLabel.place(relx = 0.40, rely = 0.86)
