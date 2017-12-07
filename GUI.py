from tkinter import *
from AlchemyGlobal import items
from Alchemization import alchemize



class AlchemyGUI:
    method = "AND"
    item_a = "Choose\nan\nItem"
    item_b = "Choose\nan\nItem"
    item_a_item = None
    item_b_item = None

    method_button = None

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        left_list = Frame(frame)
        left_list.pack(side=LEFT, padx=5, pady=5, fill=Y, expand=1)

        left_list_title = Label(left_list, justify=CENTER, text="SELECT ITEM A", fg="#67db74", font=("Hobo", 14))
        left_list_title.pack(side=TOP)

        self.left_item_list = Listbox(left_list, width=15, borderwidth=0, fg="#67db74", font=("Hobo", 14), selectbackground="#67db74", exportselection=0)
        self.left_item_list.pack(side=TOP, fill=Y, expand=1)

        alchemy_frame = Frame(frame)
        alchemy_frame.pack(side=LEFT, pady=5)

        right_list = Frame(frame)
        right_list.pack(side=LEFT, padx=5, pady=5, fill=Y, expand=1)

        right_list_title = Label(right_list, justify=CENTER, text="SELECT ITEM B", fg="#67db74", font=("Hobo", 14))
        right_list_title.pack(side=TOP)

        self.right_item_list = Listbox(right_list, width=15, borderwidth=0, fg="#67db74", font=("Hobo", 14), selectbackground="#67db74", exportselection=0)
        self.right_item_list.pack(side=TOP, fill=Y, expand=1)

        print("Adding items to GUI item list...")
        for item in items:
            print("Adding {}".format(item.name))
            self.left_item_list.insert(END, item.name.upper())
            self.right_item_list.insert(END, item.name.upper())

        # bg="#d6d6d6"

        # Alchemy controls
        self.swap_button = Button(alchemy_frame, text="<- SWAP ->", justify=CENTER, width=10, height=1, fg="#67db74", font=("Hobo", 20), borderwidth=0, command=self.swap)
        self.swap_button.pack(side=TOP)

        controls_frame = Frame(alchemy_frame)
        controls_frame.pack(side=TOP)

        self.item_a_button = Button(
            controls_frame, text=self.item_a, justify=CENTER, width=10, height=6, fg="#67db74", font=("Hobo", 14), bg="white", borderwidth=0
        )
        self.item_a_button.pack(side=LEFT, padx=25)
        self.method_button = Button(
            controls_frame, text="&&", justify=CENTER, width=3, height=1, fg="#67db74", font=("Hobo", 44), bg="white", borderwidth=0, command=self.toggle_method
        )
        self.method_button.pack(side=LEFT, padx=5)
        self.item_b_button = Button(
            controls_frame, text=self.item_b, justify=CENTER, width=10, height=6, fg="#67db74", font=("Hobo", 14), bg="white", borderwidth=0
        )
        self.item_b_button.pack(side=LEFT, padx=25)

        self.alchemize_button = Button(
            alchemy_frame, text="COMBINE", justify=CENTER, width=10, height=2, fg="#67db74", font=("Hobo", 24), bd=0, command=self.get_alchemy
        )
        self.alchemize_button.pack()


        #Results field
        self.result = StringVar()
        self.result_build = Label(alchemy_frame, textvariable=self.result, fg="#67db74", bg="white", width=80, height=30, font=("Courier New Bold", 10), bd=0, justify=LEFT)
        self.result_build.pack(pady=5)
        self.result.set("")

        self.abilities = StringVar()
        self.result_abilities = Label(alchemy_frame, textvariable=self.abilities, fg="#67db74", bg="white", width=80, height=10, font=("Courier New Bold", 10), bd=0, justify=LEFT, wraplength=600)
        self.result_abilities.pack()
        self.abilities.set("")

        self.poll()


    def get_alchemy(self):
        name_a, name_b = self.parse_selected()
        construct, ability_set = alchemize(name_a, name_b)
        self.result.set(construct)
        self.abilities.set(ability_set)


    def swap(self):
        select_a = self.left_item_list.curselection()
        select_b = self.right_item_list.curselection()

        if select_a is not ():
            self.left_item_list.selection_clear(select_a)
        if select_b is not ():
            self.right_item_list.selection_clear(select_b)

        if select_b is not ():
            self.left_item_list.select_set(select_b)
        if select_a is not ():
            self.right_item_list.select_set(select_a)

        self.selection_changed()

    def poll(self):
        now_a, now_b = self.get_selected()
        if now_a != self.item_a or now_b != self.item_b:
            name_a, name_b = self.parse_selected()
            self.selection_changed()
            self.item_a = name_a
            self.item_b = name_b
        root.after(250, self.poll)

    def selection_changed(self):
        now_a, now_b = self.parse_selected()
        self.item_a_button.config(text=now_a.upper())
        self.item_b_button.config(text=now_b.upper())

    def get_selected(self):
        return self.left_item_list.curselection(), self.right_item_list.curselection()

    def parse_selected(self):
        select_a, select_b = self.get_selected()
        if select_a is ():
            name_a = "Choose\nan\nItem"
        else:
            name_a = self.left_item_list.get(select_a)
        if select_b is ():
            name_b = "Choose\nan\nItem"
        else:
            name_b = self.right_item_list.get(select_b)
        return name_a, name_b

    def toggle_method(self):
        try:
            if self.method == "AND":
                self.method_button.config(text="||")
                self.method = "OR"
            else:
                self.method_button.config(text="&&")
                self.method = "AND"
        except AttributeError:
            print("Error!  {}{}".format(type(self.method_button),self.method))
            return

class TESTGUI:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
        )
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print("Hi there, everyone!")


def begin_interface():
    gui = AlchemyGUI(root)
    root.title = "Alchemiter"
    root.mainloop()

root = Tk()
