from tkinter import ttk
from tkinter import * 
import time 
from PIL import Image,ImageTk


class App(Tk):
    def __init__(self,pomodoro_value=25,long_break=30,short_break=15):
        
        super().__init__()
        self.title("Pomodoro Timer")
        self.geometry("350x330")
        self.resizable(False,False)
        
        self.F1 = Frame(self)
        self.F1.grid(row=0,column=0)
        self.F1.columnconfigure(0,weight=1)
    
        self.pomodoro_value = pomodoro_value
        self.long_break_value = long_break
        self.short_break_value = short_break
        
        self.frames = {}
        
        for F in (TimerFrameTitle,SettingsPage):
            
            frame = F(self.F1,self)
            self.frames[F] = frame
            
        self.change_f = self.change_frame()
                
        
    def change_frame(self,setting_flag = False):
        
        if(setting_flag):
            fr = self.frames[SettingsPage]
            fr.grid(row=0,column=0)
            fr.tkraise()
        else:
            fr = self.frames[TimerFrameTitle]
            fr.grid(row=0,column=0)
            fr.tkraise()
            

class TimerFrameTitle(ttk.Frame):
    def __init__(self,container,controller):
        super().__init__(container,padding=(50,35))
        self.control = controller
        self.frame1 = Frame(self,width=350,height=40,bg="red",padx=10,pady=10)
    
        self.pomodoro_label = Label(self.frame1,text="Pomodoro",
                                    foreground="white",
                                    background="red",
                                    font=("Helvetica",20)
                                    )
        self.pomodoro_label.pack(side=LEFT)
        
        self.settings_button = Button(self.frame1,text="Settings",padx=5,pady=5,
                                      font=("Helvetica",10),
                                      command=self.settings_page)
        self.settings_button.pack(side=RIGHT)
        
        self.frame1.pack(side="top",fill="both",expand=True)
        
        InternalTimer(self,controller)
        
    def settings_page(self):        
        self.control.change_frame(setting_flag = True)
    
class InternalTimer():
    
    def __init__(self,container,controller):
        
        self.frame2 = Frame(container,bg="pink",width=350,height=180)
        
        self.po_value = controller.pomodoro_value
        self.long_value = controller.long_break_value
        self.short_value = controller.short_break_value
        if(self.po_value <10):
            self.time = StringVar(value=f"0{self.po_value}:00")
        else:    
            self.time = StringVar(value=f"{self.po_value}:00")
        
        self.timer_label = Label(self.frame2,textvariable=self.time,
                                 font=("Helvetica",40),
                                 foreground="black",
                                 background="pink",
                                 padx=50,pady=50)
        
        self.timer_label.pack()
        self.frame2.pack(side="top",fill="both")
        ControlButton(container,self)
        
class ControlButton():
    def __init__(self,cont,controller) -> None:
        
        self.frame3 = Frame(cont,bg="black")
        self.frame3.pack(fill="both",expand=True)
        self.control = controller
        
        self.stop_timer_flag = StringVar(value="False") 
        self.start_button = Button(self.frame3,text="Start",
                                   command=self.start_timer)
        self.start_button.pack(side=LEFT,padx=5,pady=5,fill='x',
                               expand=True)
        
        self.stop_button = Button(self.frame3,text="Stop",
                                  command=self.stop_timer,
                                  state="disabled")
        self.stop_button.pack(side=LEFT,padx=5,pady=5,fill='x',expand=True)
        
        self.restart_button = Button(self.frame3,text="Restart",
                                     command=self.restart_timer)
        self.restart_button.pack(side=LEFT,padx=5,pady=5,fill='x',expand=True)
        self.pomodoro_counter = 0
        
    def start_timer(self):
        self.stop_timer_flag.set("False")
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "normal"
        self.control.frame2.update()
        def change_time(time_sec):
            while time_sec>=0:
                mins,sec = divmod(time_sec,60)
                timeformat = '{:02d}:{:02d}'.format(mins, sec)
                
                self.control.time.set(timeformat)
                self.control.frame2.update()
                time.sleep(1)
                time_sec -= 1
                
                if((self.stop_timer_flag.get()) == "True" or self.pomodoro_counter>3):
                    break
                
            if((self.stop_timer_flag.get() == "False")):
                
                if(self.pomodoro_counter<3):
                    self.pomodoro_counter += 1 
                    self.short_break()
                
                elif(self.pomodoro_counter==3):
                    self.long_break()
                    self.message_info()
                
        tim = (self.control.time.get())
        watch = tim.split(":")
        total_min_sec = int(watch[0])*60
        total_sec = total_min_sec + int(watch[1])
        change_time(total_sec)
        
    
    def stop_timer(self):
        self.stop_timer_flag.set("True")
        self.start_button["state"] = "active"
        self.stop_button["state"] = "disabled"
        
    def short_break(self):
        
        self.break_win = Toplevel(self.frame3)
        self.break_win.geometry("300x200")
        self.break_win.grab_set()
        self.break_cont = Frame(self.break_win)
        self.break_cont.pack(side="top",fill='y',expand=True)
        self.break_label = Label(self.break_cont,
                                 text="Short break",
                                 font=("Helvetica",30),
                                 foreground="blue")
        self.break_label.pack()
        self.break_time = (self.control.short_value)
        self.bb_time = StringVar(value= f"Your short break ends-in: {self.break_time}:00")
        self.break_time_label = Label(self.break_cont,
                                      textvariable=self.bb_time,
                                      font=("Helvetica",10),foreground="red")
        self.break_time_label.pack()
        self.time_decrement()
    

    def time_decrement(self):
        
        tim = (self.break_time)
        time_sec = int(tim)*60
        
        while time_sec>=0:
                mins,sec = divmod(time_sec,60)
                timeformat = '{:02d}:{:02d}'.format(mins, sec)
                time_string = f"Your short break ends-in: {timeformat}"
                self.bb_time.set(time_string)
                self.break_cont.update()
                time.sleep(1)
                time_sec -= 1
        self.break_win.destroy()  
        if(self.control.po_value <10):
            self.control.time.set(f"0{self.control.po_value}:00")
        else:    
            self.control.time.set(f"{self.control.po_value}:00")
        self.control.frame2.update()
        self.stop_timer_flag.set("True")               
        self.start_timer()
        
    def long_break(self):
        
        self.lbreak_win = Toplevel(self.frame3)
        self.lbreak_win.geometry("300x200")
        self.lbreak_win.grab_set()
        self.lbreak_cont = Frame(self.lbreak_win)
        self.lbreak_cont.pack(side="top",fill='y',expand=True)
        self.lbreak_label = Label(self.lbreak_cont,
                                 text="Long break",
                                 font=("Helvetica",30),
                                 foreground="blue")
        self.lbreak_label.pack()
        self.lbreak_time = (self.control.long_value)
        self.lbb_time = StringVar(value= f"Your long break ends-in: {self.lbreak_time}:00")
        self.lbreak_time_label = Label(self.lbreak_cont,
                                      textvariable=self.lbb_time,
                                      font=("Helvetica",10),foreground="red")
        self.lbreak_time_label.pack()
        self.time_de()
        
    def time_de(self):
        
        ltim = (self.lbreak_time)
        ltime_sec = int(ltim)*60
        
        while ltime_sec>=0:
                mins,sec = divmod(ltime_sec,60)
                timeformat = '{:02d}:{:02d}'.format(mins, sec)
                time_string = f"Your long break ends-in: {timeformat}"
                self.lbb_time.set(time_string)
                self.lbreak_cont.update()
                time.sleep(1)
                ltime_sec -= 1
        self.lbreak_win.destroy()  
        if(self.control.po_value <10):
            self.control.time.set(f"0{self.control.po_value}:00")
        else:    
            self.control.time.set(f"{self.control.po_value}:00")
        self.control.frame2.update()
        
        self.stop_timer_flag.set("True")  
        
    def message_info(self):
                     
        self.message_win = Toplevel(self.frame3)
        self.message_win.geometry("300x200")
        self.message_win.grab_set()
        self.message_label = Label(self.message_win,
                                   text="Pomodoro completed",
                                   font=("Helvetica",10),
                                   foreground="red")
        self.message_label.pack(padx=50,pady=50)
        self.message_win.update()
        time.sleep(3)
        self.restart_timer()
        self.pomodoro_counter = 1
        self.message_win.destroy()
    
    
    
    def restart_timer(self):
        if(self.control.po_value <10):
            self.control.time.set(f"0{self.control.po_value}:00")
        else:    
            self.control.time.set(f"{self.control.po_value}:00")
        self.start_button["state"] = "normal"
        self.stop_button["state"] = "disabled"
        self.control.frame2.update()
        self.stop_timer_flag.set("True")

        
class SettingsPage(ttk.Frame):
    def __init__(self,cont,controller) -> None:
        super().__init__(cont,padding=(20,35))
        self.control = controller
        
        self.frame4 = Frame(self,bg="blue")
        self.frame4.pack(fill="both",expand=True)
        
        self.pomodoro_label = Label(self.frame4,text="Pomodoro:",
                                    padx=35,pady=15,
                                    foreground="white",
                                    background="blue",
                                    font=("Helvetica",15))
        self.pomodoro_label.grid(row=0,column=0,sticky="W")
        
        self.pomodoro_label_min = Label(self.frame4,text="min",
                                    foreground="white",
                                    background="blue",
                                    font=("Helvetica",10))
        self.pomodoro_label_min.grid(row=0,column=3,sticky="W")
        
        self.pomodoro_value = StringVar(value=controller.pomodoro_value)
        self.pomodoro_spin_box = Spinbox(self.frame4,from_=0,to=60,
                                         textvariable=self.pomodoro_value,
                                         font=("Helvetica",15),
                                         width=5,wrap=True)
        self.pomodoro_spin_box.grid(row=0,column=1)
        
        self.long_time_break = Label(self.frame4,text="Long time break:",
                                    padx=35,pady=5,
                                    foreground="white",
                                    background="blue",
                                    font=("Helvetica",15))
        self.long_time_break.grid(row=1,column=0,sticky="W")
        
        self.long_time_break_min = Label(self.frame4,text="min",                        
                                    foreground="white",
                                    background="blue",
                                    font=("Helvetica",10))
        self.long_time_break_min.grid(row=1,column=3,sticky="W")
        
        self.long_time_break_value = StringVar(value=controller.long_break_value)
        self.long_time_break_spin_box = Spinbox(self.frame4,from_=0,to=60,
                                         textvariable=self.long_time_break_value,
                                         font=("Helvetica",15),
                                         width=5,wrap=True)
        self.long_time_break_spin_box.grid(row=1,column=1)
        
        self.short_time_break = Label(self.frame4,text="Short time break:",
                                    padx=35,pady=15,
                                    foreground="white",
                                    background="blue",
                                    font=("Helvetica",15))
        self.short_time_break.grid(row=2,column=0,sticky="W")
        
        self.short_time_break_min = Label(self.frame4,text="min",
                                    foreground="white",
                                    background="blue",
                                    font=("Helvetica",10))
        self.short_time_break_min.grid(row=2,column=3,sticky="W")
        
        self.short_time_break_value = StringVar(value=controller.short_break_value)
        self.short_time_break_spin_box = Spinbox(self.frame4,from_=0,to=30,
                                         textvariable=self.short_time_break_value,
                                         font=("Helvetica",15),
                                         width=5,wrap=True)
                                         
        self.short_time_break_spin_box.grid(row=2,column=1)
        
        self.back_button = Button(self.frame4,text="Back ",font=("Helvetica",15),
                                  command=self.time_page)
        self.back_button.grid(row=4,column=1)
        self.change_button = Button(self.frame4,text="Change",font=("Helvetica",15),
                                    command=self.change_pomo)
        self.change_button.grid(row=4,column=0)

    def time_page(self):
        self.control.change_frame()

    def change_pomo(self):
        self.control.destroy()
        self.control.__init__(
            pomodoro_value=int(self.pomodoro_value.get()),
            long_break=int(self.long_time_break_value.get()),
            short_break=int(self.short_time_break_value.get())
        )
        
if __name__ == "__main__":
    app = App()
    app.mainloop()