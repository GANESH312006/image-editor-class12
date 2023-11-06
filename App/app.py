try:
  import customtkinter as ctk 
  from imageWidgets import * 
  import tkinter as tk
  from tkinter import filedialog as fd
  import webbrowser as wb
  from panels import *
  import os 
  from menu import Menu
  from menu import *
  from PIL import Image
  from PIL import ImageTk
  from PIL import ImageOps
  from PIL import ImageEnhance
  from PIL import ImageFilter
except ModuleNotFoundError:
  print('Install The Required Python Packages!')
except NameError:
  print('Please install the required Python Packages!')

class App(ctk.CTk):
  def __init__(self):
    super().__init__(fg_color = '#1f191c')
    self._set_appearance_mode('dark')
    self.geometry('1000x600')
    self.title('Image Editor')
    self.resizable(False, False)
    self._windows_set_titlebar_color('light')
    
    # geometry 
    self.rowconfigure(index = 0, weight = 1)
    self.columnconfigure(index = 0, weight = 2, uniform = 'b')
    self.columnconfigure(index = 1, weight = 6, uniform = 'b')
    
    # canvas data
    self.imageWidth = self.imageHeight = self.canvasWidth = self.canvasHeight = 0
    
    # widgets
    self.imageImport = ImageImport(self, self.importImage)
    self.imageImport.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew')
    
    # self.toplevelWindow = Toplevel(self)
    
    # methods
    self.initParam()
    
    # menuBar
    self.menu = MenuBar(self, importFunc = self.importImage, exportFunc = None)
    self.configure(menu = self.menu)

    # event bindings
    try:
      self.bind('<Escape>', func = lambda e : (self.destroy()))
      self.bind('<Control-o>', func = lambda e : self.menu.openDiag())
      self.bind('<Control-n>', func = lambda e : self.menu.openDiag())
      self.bind('<Control-s>', func = lambda e : self.exportImage())
      self.bind('<Control-r>', func = lambda e : self.menu.openWeb(url = self.menu.requirementsVar))
      self.bind('<Control-u>', func = lambda e : self.menu.openWeb(url = self.menu.userManuelVar))
      self.bind('<Alt-k>', func = lambda e : self.menu.openWeb(url = self.menu.keyBoardShortcutsVar))
    except Exception as e:
      print(e)

    # run
    self.mainloop()    
    
  def initParam(self):
    self.posVars = {
      'rotate': ctk.DoubleVar(value = ROTATE_DEFAULT),
      'zoom': ctk.DoubleVar(value = ZOOM_DEFAULT),
      'flip': ctk.StringVar(value = FLIP_OPTIONS[0])
    }
    
    self.colorVars = {
      'brightness': ctk.DoubleVar(value = BRIGHTNESS_DEFAULT), 
      'grayscale': ctk.BooleanVar(value = GRAYSCALE_DEFAULT),
      'invert': ctk.BooleanVar(value = INVERT_DEFAULT),
      'vibrance': ctk.DoubleVar(value = VIBRANCE_DEFAULT),
    }
    
    self.fxVars = {
      'blur': ctk.DoubleVar(value = BLUR_DEFAULT),
      'contrast': ctk.IntVar(value = CONTRAST_DEFAULT), 
      'effect': ctk.StringVar(value = EFFECT_OPTIONS[0])
    }

    for var in list(self.posVars.values()) + list(self.colorVars.values()) + list(self.fxVars.values()): # To get the values from the dict, to iterate thru all the three dict, we use list as list are ezy to combine
      var.trace('w', self.manipulateImg)
    
  def manipulateImg(self, *args):
    self.image = self.original
    self.imageStack = [self.image.copy]
    
    # rotate
    if self.posVars['rotate'].get()!=ROTATE_DEFAULT:
      self.image = self.image.rotate(self.posVars['rotate'].get())
    
    # zoom
    if self.posVars['zoom'].get()!= ZOOM_DEFAULT:
      self.image = ImageOps.crop(image = self.image, border = self.posVars['zoom'].get()) # type:ignore
    
    # flip
    if self.posVars['flip'].get()!=FLIP_OPTIONS[0]:
      if (self.posVars['flip'].get() == 'X'):
        self.image = ImageOps.mirror(self.image) # filp iamge in horizontal axis
        
      if (self.posVars['flip'].get() == 'Y'):
        self.image = ImageOps.flip(self.image)
        
      if (self.posVars['flip'].get() == 'Both'):
        self.image = ImageOps.mirror(self.image) 
        self.image = ImageOps.flip(self.image)
    
    #brightness and vibrance
    if self.colorVars['brightness'].get() != BRIGHTNESS_DEFAULT:
      brightness_enhancer = ImageEnhance.Brightness(self.image)
      self.image = brightness_enhancer.enhance(self.colorVars['brightness'].get())
      
    if self.colorVars['vibrance'].get() != VIBRANCE_DEFAULT:  
      vibrance_enhancer = ImageEnhance.Color(self.image)
      self.image = vibrance_enhancer.enhance(self.colorVars['vibrance'].get())
    

    #grayscale and invert of the colors
    if self.colorVars['grayscale'].get():
      self.image=ImageOps.grayscale(self.image)
    if self.colorVars['invert'].get():
      self.image=ImageOps.invert(self.image)

    #blur and contrast
    if self.fxVars['blur'].get() != BLUR_DEFAULT:
      self.image=self.image.filter(ImageFilter.GaussianBlur(self.fxVars['blur'].get()))
      
    if self.fxVars['contrast'].get() != CONTRAST_DEFAULT:  
      self.image=self.image.filter(ImageFilter.UnsharpMask(self.fxVars['contrast'].get()))
      
    match self.fxVars['effect'].get(): # Match cases for effects
      case 'Emboss':self.image = self.image.filter(ImageFilter.EMBOSS)
      case 'Find edges':self.image = self.image.filter(ImageFilter.FIND_EDGES)
      case 'Contour':self.image = self.image.filter(ImageFilter.CONTOUR)
      case 'Edge enhance':self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    
    self.placeImg()
    
  def importImage(self, path:str):
    self.original = Image.open(path)
    self.image = self.original
    self.imageRatio = self.image.size[0] / self.image.size[1] # Returns Tuple
    
    self.imageTk = ImageTk.PhotoImage(self.image, master = self)
    
    self.imageImport.grid_forget()
    self.imageOutput = ImageOutput(self, self.resizeImage)
    self.closeBtn = CloseOutput(self, command = self.closeEdit)
    
    self.menu = Menu(self, self.posVars, self.colorVars, self.fxVars, self.exportImg)
    
  def resizeImage(self, event): 
    # current canvas ratio
    canvasRatio = event.width / event.height
    
    # update canvas attrb
    self.canvasHeight = event.height
    self.canvasWidth = event.width
        
    # resize
    if (canvasRatio > self.imageRatio): # Canvas wider than image
      self.imageHeight = int(event.height)
      self.imageWidth = int(self.imageHeight * self.imageRatio)
    else: # canvas taller than image
      self.imageWidth = int(event.width)
      self.imageHeight = int(self.imageWidth / self.imageRatio)
    self.placeImg()
          
  def placeImg(self):
    self.imageOutput.delete('all')
    resizedImage = self.image.resize((self.imageWidth, self.imageHeight))
    self.imageTk = ImageTk.PhotoImage(resizedImage, master = self) 
    self.imageOutput.create_image(self.canvasWidth / 2 , self.canvasHeight/2, image = self.imageTk)

  def closeEdit(self):
    self.imageOutput.grid_forget()
    self.closeBtn.place_forget()
    self.menu.grid_forget()
    self.imageImport = ImageImport(self, self.importImage)
    self.imageImport.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew')

  def exportImg(self, name, file, path):
    try:
      # Check if the path and name variables are empty.
      if not name:
        print('Enter name of the file!')
        return
      if (not path):
        print('Enter path of the file!')
        return
      
      # Create the export string.
      exportStr = f'{path}/{name}.{file}'

      # Save the image.
      self.image.save(exportStr)

      # Check if the file was saved successfully.
      if os.path.exists(exportStr):
        print(f'The file is saved to {exportStr}')
      else:
        print(f'The file is not saved to {exportStr}')

    except FileNotFoundError as e:
      print(e)
    except Exception:
      pass
     
  def exportImage(self):
    formats = [
      ('PNG files', '*.png'), 
      ('JPEG files', '*.jpg')
    ]
    file_path = fd.asksaveasfilename(
      defaultextension = '.png', 
      filetypes = formats
    )

    if file_path:
      parts = file_path.split('/')
      filename = parts[-1]
      path = '/'.join(parts[:-1])
      format = file_path.split('.')[-1]
      self.export_image(format, filename, path)

  def export_image(self, format, filename, path):
    try:
      export_str = f'{path}/{filename}.{format}'
      self.image.save(export_str)
      print(f'Image exported to {export_str}')
    except Exception as e:
      print(e)
    
class MenuBar(tk.Menu):
  def __init__(self,parent, importFunc, exportFunc):
    super().__init__(parent)
    self.app = parent
    self.createFileMenu()
    self.createHelpmenu()
        
    # init attributes
    self.importFunc = importFunc
    self.exportFunc = exportFunc

  def openWeb(self,url):
    wb.open(url)

  def createFileMenu(self):
    fileMenu = tk.Menu(master = self, tearoff = False)
    fileMenu = tk.Menu(master = self, tearoff = False)
    fileMenu.add_command(label = 'New (ctrl - n)', command = lambda : self.openDiag())  
    fileMenu.add_command(label = 'Open' '(ctrl - o)', command = lambda:self.openDiag())
    fileMenu.add_command(label = 'New Window', command = lambda : self.openNewWindow())
    fileMenu.add_command(label = 'Export (ctrl - s)', command = lambda : self.exportImage())
    fileMenu.add_separator() # To add a separator for the exit menu
    fileMenu.add_command(label = 'Exit', command = lambda:self.app.quit())
    self.add_cascade(menu = fileMenu, label = 'File')

  def createHelpmenu(self):
    # init Var
    github_url = 'https://github.com/GANESH312006/'
    self.keyBoardShortcutsVar = github_url + 'KeyboardShortcuts/blob/main/KeyBoardShortcuts.txt'
    self.requirementsVar = github_url + 'KeyboardShortcuts/blob/main/requirements.txt'
    self.userManuelVar = 'https://github.com/GANESH312006/KeyboardShortcuts/blob/main/CsProjUserManuel.txt'
    
    # helpMenu
    helpMenu = tk.Menu(master = self, tearoff = False)
    helpMenu.add_command(label = 'UserManuel (ctrl-u)', command = lambda:self.openWeb('https://github.com/Shad18/KeyboardShortcuts/blob/main/User%20Manual'))
    helpMenu.add_command(
      label = 'Keyboard Shortcuts (alt-k)',
      command = lambda : self.openWeb(self.keyBoardShortcutsVar)
      )
    helpMenu.add_command(
      label = 'Requirements (ctrl-r)', 
      command = lambda : self.openWeb(self.requirementsVar)
    )
    self.add_cascade(menu = helpMenu, label = 'Help')

  def openDiag(self):
    try:
      path = fd.askopenfile().name
      self.importFunc(path)
    except Exception as e:
      pass
  
  def openNewWindow(self):
    try:
      appMain = App()
    except Exception:
      pass
  
  def exportImage(self):
    formats = [
      ('PNG files', '*.png'), 
      ('JPEG files', '*.jpg')
      ]
    file_path = fd.asksaveasfilename(
      defaultextension = '.png', 
      filetypes = formats
    )

    if file_path:
      parts = file_path.split('/')
      filename = parts[-1]
      path = '/'.join(parts[:-1])
      format = file_path.split('.')[-1]
      self.export_image(format, filename, path)

  def export_image(self, format, filename, path):
    try:
      export_str = f'{path}/{filename}.{format}'
      self.app.image.save(export_str)
      print(f'Image exported to {export_str}')
    except Exception as e:
      print(e)

  def resize(self):
    self.app.image.resize()
    self.app.placeImg()

if (__name__ == '__main__'):
  try:
    appMain = App()
  except Exception as e:
    print(e)
