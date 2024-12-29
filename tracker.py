import tkinter as tk 
import psycog2 
from datetime import datetime
from tkinter import ttk, messagebox, simpledialog, fieldialog 

class DutyTracker:
    def __init__ (self, Output):
        self.Output = Output
        self.Output.title("my little project ")
        self.Output.geometry('800x400')

        self.connect = psycog2.connect(
            dbname = 'mydb',
            user = 'postgres',
            password = '672345',
            host ='localhost',
            port = '5432',
        )

        self.cursor() =self.connect.cursor()

        self.create_tracker_table()

        self.categories = [
            'Food',"transport",'conti ','katanga'
        ]
        self.create_widget()

        self.load_expenses()

        def create_tracker_table(self):
            create_table_query = ''' 
            CREATE TABLE IF NOT EXISTS  tracker_expenses(
           ID serial , primary key ,
           DATE date not null ,
             AMOUNT decimal(10,2) not ull ,
             CATEGORY VARCHAR(100) not null
               DESCRIPTION  text
           L)
 '''
            
            self.cursor.execute (create_table_query)
            self.connect.commit()


            def create_widgets(self):
                #expense input frame 
                input_frame = ttk.LabelFrame(self.Output, text ='Create New expense')
                input_frame.pack(padx=12 pady=10 fill='x')

                ttk.Label(input_frame, text="Amount (cedis )".grid(row=0,coloumn=0 padx== 5 pady==5))
                self.amount_entry = ttk.Entry(input_frame,width=20)
                self.amount_entry.grid(row=0,coloumn=1,padx=5,pady=5)

                ttk.Label(input_frame, text='Category: ').grid(row =0,coloumn=2 , padx=2 ,pady=5)
                self.amount_entry = ttk.Entry(input_frame ,width =20)



                def load_expenses(self):
                    query = "select date , amount .category ,description from expense "
                    self.cursor.execute.fetchall()
                    for row in rows:
                        self.expense_tree.insert