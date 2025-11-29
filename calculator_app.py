## Additional calculator app project with Tkinter GUI ## 

from tkinter import *

# Create the main application window
root = Tk()
root.title("Calculator")

temp_calc = 0
previous_operator = ""

# Functions for button actions
def number_button_click(number):
    """
    Handle number button clicks in the calculator.

    Parameters:
    number (int): The digit pressed by the user.

    Returns:
    None
    """
    global previous_operator
    if previous_operator == "=" or calc_entry.get() == "Math Error":
        reset_calculation()
    # Clear the entry field and append the clicked number to the current number
    current_number = calc_entry.get()
    clear_entry()
    
    calc_entry.insert(0, str(current_number) + str(number))

def clear_entry():
    """
    Clear the calculator entry field.

    Parameters:
    None

    Returns:
    None
    """
    calc_entry.delete(0, END)
    
def reset_calculation():
    """
    Reset the calculator state, clearing the entry field and resetting temporary calculation values and operator history.

    Parameters:
    None

    Returns:
    None
    """
    global temp_calc
    global previous_operator
    clear_entry()

    temp_calc = 0
    previous_operator = ""

def get_current_entry():
    """
    Retrieve the current value from the calculator entry field. Handles 'Math Error' by resetting the calculator state.

    Parameters:
    None

    Returns:
    float or str: The numeric value in the entry field as a float, or an empty string if the field is empty or invalid.
    """
    if calc_entry.get() == "Math Error":
        reset_calculation()
        return ""

    if calc_entry.get() != "":
        print (calc_entry.get())
        return float(calc_entry.get())
    else:
        return ""

def toggle_negate():
    """
    Toggle the sign of the current number in the calculator entry field.

    If the number is positive, it becomes negative. If negative, 
    it becomes positive. Updates the temporary calculation if the previous operator was '='.

    Parameters:
    None

    Returns:
    None
    """
    global previous_operator
    global temp_calc
    current_number = calc_entry.get()
    
    if "-" not in current_number:
        clear_entry()
        negated_number = "-" + current_number
    else:
        clear_entry()
        negated_number = current_number.replace("-", "")

    clear_entry()
    calc_entry.insert(0, negated_number)

    if previous_operator == "=":
        temp_calc = float(calc_entry.get())

def add_decimal():
    """
    Add a decimal point to the current number in the calculator entry field.

    Ensures that only one decimal point is added and prevents modification if the last operator was '='.

    Parameters:
    None

    Returns:
    None
    """

    current_number = calc_entry.get()
    if "." not in current_number and previous_operator != "=":
        clear_entry()
        calc_entry.insert(0, str(current_number) + ".")

def operator_button_click(operator):
    """
    Handle operator button clicks (+, -, ×, ÷, =) in the calculator.
    Performs the appropriate arithmetic operation based on the previous operator and updates the temporary calculation. 
    Displays 'Math Error' if division by zero occurs.

    Parameters:
    operator (str): The operator pressed by the user ('+', '-', '×', '÷', '=').

    Returns:
    None
    """

    global previous_operator 
    global temp_calc
    
    current_number = get_current_entry()

    if current_number != "":
        clear_entry()
        
        # Initialise temp_calc if it's the first operation
        if previous_operator == "":
            temp_calc = current_number

        match previous_operator:
            case "+":
                temp_calc += current_number
            case "-":
                temp_calc -= current_number
            case "×":
                temp_calc *= current_number
            case "÷":
                if current_number != 0:
                    temp_calc /= current_number
                else:
                    clear_entry()
                    calc_entry.insert(0, "Math Error")
                    temp_calc = ""
            case ".":
                pass

    #print (temp_calc)
    #print (previous_operator)
    previous_operator = operator

    if operator == "=":
        calc_entry.insert(0, str(temp_calc))

# Create widgets
calc_entry = Entry(root, width=50, borderwidth=5)

button_1 = Button(root, text="1", padx=40, pady=20, command=lambda: number_button_click(1))
button_2 = Button(root, text="2", padx=40, pady=20, command=lambda: number_button_click(2))
button_3 = Button(root, text="3", padx=40, pady=20, command=lambda: number_button_click(3))
button_4 = Button(root, text="4", padx=40, pady=20, command=lambda: number_button_click(4))
button_5 = Button(root, text="5", padx=40, pady=20, command=lambda: number_button_click(5))
button_6 = Button(root, text="6", padx=40, pady=20, command=lambda: number_button_click(6))
button_7 = Button(root, text="7", padx=40, pady=20, command=lambda: number_button_click(7))
button_8 = Button(root, text="8", padx=40, pady=20, command=lambda: number_button_click(8))
button_9 = Button(root, text="9", padx=40, pady=20, command=lambda: number_button_click(9))
button_0 = Button(root, text="0", padx=40, pady=20, command=lambda: number_button_click(0))

button_add = Button(root, text="+", padx=40, pady=20, command=lambda: operator_button_click("+"))
button_subtract = Button(root, text="-", padx=42, pady=20 , command=lambda: operator_button_click("-"))
button_multiply = Button(root, text="×", padx=40, pady=20 , command=lambda: operator_button_click("×"))
button_divide = Button(root, text="÷", padx=40, pady=20, command=lambda: operator_button_click("÷"))
button_equal = Button(root, text="=", padx=90, pady=20, command=lambda: operator_button_click("="), bg = "blue", fg = "white")
button_clear = Button(root, text="Clear", padx=77, pady=20, command=reset_calculation)
button_negate = Button(root, text="+/-", padx=34, pady=20, command=toggle_negate)
button_decimal = Button(root, text=".", padx=42, pady=20, command=add_decimal)

# Place widgets using grid layout
calc_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

button_negate.grid(row=4, column=0)
button_0.grid(row=4, column=1)
button_decimal.grid(row=4, column=2)
button_add.grid(row=4, column=3)


button_1.grid(row=3, column=0)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=2)
button_subtract.grid(row=3, column=3)

button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)
button_multiply.grid(row=2, column=3)

button_7.grid(row=1, column=0)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=2)
button_divide.grid(row=1, column=3)


button_equal.grid(row=5, column=2, columnspan=2)
button_clear.grid(row=5, column=0, columnspan=2)

# Start the main event loop
root.mainloop()