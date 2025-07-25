import customtkinter
import tkinter
from datetime import datetime

customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("dark")

def button_click_event():
    dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Test")
    print("Number:", dialog.get_input())

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)

def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())
    ## update optionmenu values based on the selected type
    if radio_var.get() == 1:  # Income
        category_list = category_list_i
    else:  # Expense
        category_list = category_list_e
        
    optionmenu.configure(values=category_list, variable=customtkinter.StringVar(value=category_list[0]))

app = customtkinter.CTk()
app.geometry("1024x768")
app.title("Personal Finance Tracker")

category_list_i = ["Salary", "Investment", "Gift", "Other"]
category_list_e = ["Food", "Transport", "Entertainment", "Health", "Utilities", "Other"]

app.label = customtkinter.CTkLabel(app, text="Date")
app.label.grid(row=0, column=0, padx=10, pady=10)

app.date_entry = customtkinter.CTkEntry(app)
app.date_entry.grid(row=0, column=1, padx=10, pady=10)

## insert current date in YYYY-MM-DD format
app.date_entry.insert(0, datetime.today().strftime('%d-%m-%Y'))

app.label2 = customtkinter.CTkLabel(app, text="Type")
app.label2.grid(row=1, column=0, padx=10, pady=10)

radio_var = tkinter.IntVar(value=2)
radiobutton_1 = customtkinter.CTkRadioButton(app, text="Income", command=radiobutton_event, variable= radio_var, value=1)
radiobutton_2 = customtkinter.CTkRadioButton(app, text="Expense", command=radiobutton_event, variable= radio_var, value=2)

radiobutton_1.grid(row=1, column=1, padx=10, pady=10)
radiobutton_2.grid(row=1, column=2, padx=10, pady=10)

app.label3 = customtkinter.CTkLabel(app, text="Category")
app.label3.grid(row=2, column=0, padx=10, pady=10)

optionmenu_var = customtkinter.StringVar(value=category_list_e[0])  # Set default value to the first category
optionmenu = customtkinter.CTkOptionMenu(app, values=category_list_e, command=optionmenu_callback, variable=optionmenu_var)
optionmenu.grid(row=2, column=1, padx=10, pady=10)

app.label4 = customtkinter.CTkLabel(app, text="Amount")
app.label4.grid(row=3, column=0, padx=10, pady=10)

app.amount_entry = customtkinter.CTkEntry(app)
app.amount_entry.grid(row=3, column=1, padx=10, pady=10) 
## add validation to allow only digets and decimal points
app.amount_entry.configure(validate="key", validatecommand=(app.register(lambda s: s.replace('.', '', 1).isdigit()), '%P'))

#app.amount_entry.configure(validate="key", validatecommand=(app.register(lambda s: s.isdigit()), '%P')) 
  

app.label5 = customtkinter.CTkLabel(app, text="Description")
app.label5.grid(row=4, column=0, padx=10, pady=10)
app.description_entry = customtkinter.CTkEntry(app)
app.description_entry.grid(row=4, column=1, padx=10, pady=10)   

app.dialog = customtkinter.CTkButton(app, text="Dialog", command=button_click_event)
app.dialog.grid(row=5, column=0, padx=10, pady=10)

app.exit_button = customtkinter.CTkButton(app, text="Exit", command=app.destroy)
app.exit_button.configure(fg_color="darkred", hover_color="red")
app.exit_button.grid(row=5, column=1, padx=10, pady=10)


app.mainloop()