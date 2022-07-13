import tkinter as tk
from unicodedata import digit

#colors
LIGHT_GRAY="#F5F5F5"
LABEL_COLOR="#25265E"
WHITE="#FFFFFF"
ORANGE="#FFA500"
DEFAULT_FONT_STYLE = ("Arial", 20)
OFF_WHITE = "#F8FAFF"
SMALL_FONT_SIZE=("Arial",16)
LARGE_FONT_SIZE=("Arial",40,"bold")
DIGITS_FONT_STYLE=("Arial",24,"bold")
class Calculator:
    def __init__(self):
        self.window=tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0,0)
        self.window.title("Calculator")   

        self.display_frame=self.create_display_frame()
        self.buttons_frame=self.create_buttons_frame()

        self.total_expression=""
        self.current_expression=""

        self.total_label,self.current_label=self.create_display_labels()
        
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+","%":"%"}
        self.buttons_frame.rowconfigure(0,weight=1)
        for x in range(1,5):
            self.buttons_frame.rowconfigure(x,weight=1)
            self.buttons_frame.columnconfigure(x,weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_clear_button()
        self.create_equal_button()

        self.create_square_button()
        self.create_square_root_button()

        self.bind_keys()

    def add_to_expression(self,value):
        self.current_expression+=str(value)

        self.update_current_label()

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_current_label()

    def evaluate(self):
        self.total_expression+=self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Invalid"
        finally:
            self.update_current_label()
    
    def create_display_frame(self):
        frame=tk.Frame(self.window,height=221,bg=LIGHT_GRAY)
        frame.pack(expand=True,fill="both")
        return frame
    
    def create_buttons_frame(self):
        frame=tk.Frame(self.window)
        frame.pack(expand=True,fill="both")
        return frame

    def create_display_labels(self):
        total_label=tk.Label(self.display_frame,text=self.total_expression,anchor=tk.E,bg=LIGHT_GRAY,fg=ORANGE,padx=24,font=SMALL_FONT_SIZE)
        total_label.pack(expand=True,fill="both")

        current_label=tk.Label(self.display_frame,text=self.current_expression,anchor=tk.E,bg=LIGHT_GRAY,fg="#000000",padx=24,font=LARGE_FONT_SIZE)
        current_label.pack(expand=True,fill="both")

        return total_label,current_label
    def clear(self):
        self.total_expression=""
        self.current_expression=""
        self.update_current_label()
        self.update_total_label()

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_current_label()
    
    def square_root(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_current_label()
    
    
    
    def bind_keys(self):
        self.window.bind("<Return>", lambda x: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda x, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda x, operator=key: self.append_operator(operator))

    def create_digit_buttons(self):
        for digit,grid_value in self.digits.items():
            button=tk.Button(self.buttons_frame,text=str(digit),bg=WHITE,fg="#000000",font=DIGITS_FONT_STYLE,
                               borderwidth=0,command=lambda x=digit:self.add_to_expression(x))
            button.grid(row=grid_value[0],column=grid_value[1],sticky=tk.NSEW)

    def create_operator_buttons(self):
        i=0
        for operator,symbol in self.operations.items():
            button=tk.Button(self.buttons_frame,text=symbol,fg=ORANGE,bg=OFF_WHITE,font=DEFAULT_FONT_STYLE,borderwidth=0,command=lambda x=operator: self.append_operator(x))
            button.grid(row=i,column=4,sticky=tk.NSEW)
            i+=1
    
    def create_clear_button(self):
        button=tk.Button(self.buttons_frame,text='C',fg=ORANGE,bg=OFF_WHITE,font=DEFAULT_FONT_STYLE,borderwidth=0,command=self.clear)
        button.grid(row=0,column=1,sticky=tk.NSEW)

    def create_equal_button(self):
        button=tk.Button(self.buttons_frame,text='=',fg=WHITE,bg=ORANGE,font=DEFAULT_FONT_STYLE,borderwidth=0,command=self.evaluate)
        button.grid(row=4,column=3,columnspan=2,sticky=tk.NSEW)

    def create_square_button(self):
        button=tk.Button(self.buttons_frame,text='x\00b2',fg=ORANGE,bg=OFF_WHITE,font=DEFAULT_FONT_STYLE,borderwidth=0,command=self.square)
        button.grid(row=0,column=2,sticky=tk.NSEW)
    
    def create_square_root_button(self):
        button=tk.Button(self.buttons_frame,text='\u221a',fg=ORANGE,bg=OFF_WHITE,font=DEFAULT_FONT_STYLE,borderwidth=0,command=self.square_root)
        button.grid(row=0,column=3,sticky=tk.NSEW)
    
    

    def update_total_label(self):
        self.total_label.config(text=self.total_expression)

    def update_current_label(self):
        self.current_label.config(text=self.current_expression[:12])
    def run(self):
        self.window.mainloop()

calc=Calculator()
calc.run()
