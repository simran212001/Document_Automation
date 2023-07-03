import tkinter as tk
from tkinter import ttk

def add_value():
    new_value = entry.get()
    if new_value and new_value not in dropdown["values"]:
        dropdown["values"] = (*dropdown["values"], new_value)
        dropdown.set("")

root = tk.Tk()

# Create a StringVar to hold the selected values
selected_values = tk.StringVar()

# Create a Combobox (dropdown) with editable property set to True
dropdown = ttk.Combobox(root, textvariable=selected_values, state="readonly")
dropdown["values"] = ("Value 1", "Value 2", "Value 3")
dropdown.pack()

# Create an Entry widget to allow adding new values
entry = tk.Entry(root)
entry.pack()

# Create a button to add the new value to the dropdown
add_button = tk.Button(root, text="Add", command=add_value)
add_button.pack()

root.mainloop()
