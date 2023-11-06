import tkinter as tk
import customtkinter as ctk 

def ripple_effect(event):
    x, y = event.x, event.y  # Get the click coordinates
    ripple = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline='', width=2, fill='blue', stipple='gray12')
    
    def expand_ripple():
        canvas.move(ripple, -1, -1)  # Move the ripple to slightly overlap the original position
        canvas.scale(ripple, x, y, canvas.coords(ripple)[2] + 10, canvas.coords(ripple)[3] + 10)  # Expand the ripple
        
        if canvas.coords(ripple)[2] < 50:  # If ripple size is less than 50, continue expanding
            canvas.after(10, expand_ripple)
        else:
            canvas.delete(ripple)  # Remove the ripple when it's large enough

    expand_ripple()

root = ctk.CTk()
root.title("Ripple Effect")

canvas = ctk.CTkCanvas(root, width=400, height=400)
canvas.pack()

button = ctk.CTkButton(root, text="Click Me")
button.bind("<Button>", lambda e:ripple_effect)
button.pack()

root.mainloop()