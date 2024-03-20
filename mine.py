from tkinter import * 
from tkinter import messagebox 
import tkinter.filedialog as tkf
  
messagebox.showinfo("showinfo", "Information") 
  
messagebox.showwarning("showwarning", "Warning") 
  
messagebox.showerror("showerror", "Error") 
  
c_1 = messagebox.askquestion("askquestion", "Are you sure?") 
print(c_1)

c_2 = messagebox.askokcancel("askokcancel", "Want to continue?") 
print(c_2)

c_3 = messagebox.askyesno("askyesno", "Find the value?") 
print(c_3)

c_4 = messagebox.askretrycancel("askretrycancel", "Try again?")   
print(c_4)

#tkf.askopenfilename(title='seleccione un archivo')
