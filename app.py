import tkinter
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import pandas as pd
import math
import segment_tree as seg


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # output data
        # build tree
        self.input_arr = tk.StringVar()
        self.data_arr = []
        self.file_path = "a"
        self.max_tree_arr = []
        self.min_tree_arr = []
        self.sum_tree_arr = []
        self.idx_tree_arr = []

        # query tree
        self.min = tk.IntVar()
        self.max = tk.IntVar()
        self.sum = tk.IntVar()
        self.left_idx = tk.IntVar()
        self.right_idx = tk.IntVar()

        # update tree
        self.update_idx = tk.IntVar()
        self.update_value = tk.IntVar()

        # win configure
        self.title("Segment Tree")
        self.geometry("1000x700")

        self.attributes("-fullscreen", True)

        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=30)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1000)

        self.title_label = tk.Label(
            self,
            text="Segment tree",
            bg="green4",
            fg="white",
            highlightbackground="grey",
            highlightthickness=1,
        )
        self.title_label.config(font=("Segoe UI", 30))
        self.title_label.grid(row=0, column=0, sticky=tk.NSEW)

        self.body_frame = tk.LabelFrame(
            self,
            text="ToolBox",
            bg="grey95",
            highlightbackground="dark green",
            highlightthickness=1,
        )
        self.body_frame.grid(row=1, column=0, sticky=tk.NSEW)

        self.body_frame.columnconfigure(0, weight=1)
        self.body_frame.columnconfigure(1, weight=0)

        self.canvas = tk.Canvas(
            self, bg="grey99", highlightbackground="dark green", highlightthickness=2
        )
        self.canvas.grid(row=0, column=1, rowspan=3, sticky=tk.NSEW)

        self.style = Style()

        self.style.configure("TButton", font=("calibri", 12, "bold"), borderwidth=2)

        # Changes will be reflected
        # by the movement of mouse.
        self.style.map(
            "TButton",
            foreground=[("active", "!disabled", "green")],
            background=[("active", "black")],
        )

        ##input frame in body_frame
        self.input_frame = tk.Frame(self.body_frame)
        self.input_frame.grid(row=0, column=0, sticky=tk.NSEW, pady=(10, 10))
        self.input_frame.columnconfigure(0, weight=1)
        self.input_frame.columnconfigure(1, weight=5)
        self.input_frame.columnconfigure(2, weight=2)

        # Array entry
        self.array_label = tk.Label(self.input_frame, text="Array:")
        self.array_label.config(font=("calibri bold", 18))
        self.array_label.grid(row=0, column=0, sticky=tk.W, padx=15)

        self.array_entry = tk.Entry(self.input_frame, bd=2, textvariable=self.input_arr)
        self.array_entry.grid(row=0, column=1, sticky=tk.NSEW, padx=(0, 10))

        self.enter_button = Button(self.input_frame, text="Enter", command=self.get_arr)
        self.enter_button.grid(row=0, column=2, sticky=tk.W, pady=3)

        self.filename = tk.StringVar()
        self.filename.set("filename.csv")

        self.select_file_label = tk.Label(
            self.input_frame, textvariable=self.filename, font=("calibri", 15)
        )
        self.select_file_label.grid(row=1, column=0, columnspan=2)

        self.select_file_button = Button(
            self.input_frame, text="Select file", command=self.open_file_dialog
        )
        self.select_file_button.grid(row=1, column=2, sticky=tk.W, pady=3)

        self.build_button = Button(
            self.input_frame, text="Build", command=self.build_button
        )
        self.build_button.grid(row=2, column=2, sticky=tk.W, pady=3)

        # Query frame:
        self.query_frame = tk.Frame(self.body_frame)
        self.query_frame.grid(row=1, column=0, sticky=tk.NSEW, pady=(0, 10))

        self.query_frame.columnconfigure(0, weight=1000)
        self.query_frame.columnconfigure(1, weight=1)
        self.query_frame.columnconfigure(2, weight=2)
        self.query_frame.columnconfigure(3, weight=1)
        self.query_frame.columnconfigure(4, weight=1)

        self.query_label = tk.Label(self.query_frame, text="Query: ")
        self.query_label.config(font=("calibri bold", 18))
        self.query_label.grid(row=0, column=0, sticky=tk.W, padx=15)

        # Check type:
        self.select_query_label = tk.Label(self.query_frame, text="Type Query: ")
        self.select_query_label.config(font=("calibri", 15))
        self.select_query_label.grid(row=1, column=0, sticky=tk.E, padx=15)

        self.check_type_frame = tk.Frame(self.query_frame)
        self.check_type_frame.grid(row=1, column=1, sticky=tk.NSEW)

        self.min_checkbutton = tk.Checkbutton(
            self.check_type_frame,
            text="Min",
            font=("calibri", 15),
            variable=self.min,
            onvalue=1,
            offvalue=0,
            height=2,
            width=10,
        )
        self.min_checkbutton.pack(side="left")

        self.max_checkbutton = tk.Checkbutton(
            self.check_type_frame,
            text="Max",
            font=("calibri", 15),
            variable=self.max,
            onvalue=1,
            offvalue=0,
            height=2,
            width=10,
        )
        self.max_checkbutton.pack(side="left")

        self.sum_checkbutton = tk.Checkbutton(
            self.check_type_frame,
            text="Sum",
            font=("calibri", 15),
            variable=self.sum,
            onvalue=1,
            offvalue=0,
            height=2,
            width=10,
        )
        self.sum_checkbutton.pack(side="left")

        # self.sub_checkbutton = tk.Checkbutton(self.check_type_frame, text="Sub", font=("calibri", 15), variable=self.sub, onvalue=1, offvalue=0, height=2, width=10)
        # self.sub_checkbutton.pack(side="left")

        self.index_label = tk.Label(self.query_frame, text="Index:")
        self.index_label.config(font=("calibri", 15))
        self.index_label.grid(row=2, column=0, sticky=tk.E, padx=15)

        self.index_frame = tk.Frame(self.query_frame)
        self.index_frame.grid(row=2, column=1, sticky=tk.NSEW)

        self.left_idx_label = tk.Label(self.index_frame, text="L.idx: ")
        self.left_idx_label.config(font=("calibri", 15))
        self.left_idx_label.pack(side="left", padx=(35, 0))

        self.left_idx_entry = tk.Entry(
            self.index_frame, width=20, textvariable=self.left_idx, bd=2
        )
        self.left_idx_entry.pack(side="left", padx=(10, 0), fill="y")

        self.right_idx_label = tk.Label(self.index_frame, text="R.idx: ")
        self.right_idx_label.config(font=("calibri", 15))
        self.right_idx_label.pack(side="left", padx=(75, 0))

        self.right_idx_entry = tk.Entry(
            self.index_frame, width=20, textvariable=self.right_idx, bd=2
        )
        self.right_idx_entry.pack(side="left", fill="y", padx=(10, 0))

        self.get_button = Button(self.query_frame, text="Get", command=self.get_button)
        self.get_button.grid(row=3, column=1, sticky=tk.E, pady=10, padx=35)

        # Update_frame:
        self.update_frame = tk.Frame(self.body_frame)
        self.update_frame.grid(row=2, column=0, sticky=tk.NSEW)

        self.update_label = tk.Label(self.update_frame, text="Update: ")
        self.update_label.config(font=("calibri bold", 18))
        self.update_label.grid(row=0, column=0, sticky=tk.W, padx=15)

        self.index_label = tk.Label(
            self.update_frame, text="Index: ", font=("calibri", 15)
        )
        self.index_label.grid(row=1, column=1, padx=10)

        self.index_entry = tk.Entry(
            self.update_frame, bd=2, textvariable=self.update_idx
        )
        self.index_entry.grid(row=1, column=2, sticky=tk.NSEW)

        self.newvalue_label = tk.Label(
            self.update_frame, text="New Value: ", font=("calibri", 15)
        )
        self.newvalue_label.grid(row=1, column=3, padx=10)

        self.newvalue_entry = tk.Entry(
            self.update_frame, bd=2, textvariable=self.update_value
        )
        self.newvalue_entry.grid(row=1, column=4, sticky=tk.NSEW)

        self.update_button = Button(
            self.update_frame, text="Update", command=self.update_button
        )
        self.update_button.grid(row=2, column=4, sticky=tk.NSEW, pady=10)

        # Text widget
        self.text_frame = tk.Frame(self)
        self.text_frame.grid(row=2, column=0, sticky=tk.NSEW)

        self.text = Text(self.text_frame, height=25, width=70, font=("calibri", 12))

        # Create label
        self.label_text = Label(self.text_frame, text="Result")
        self.label_text.config(font=("calibri bold", 18))

        # Create an Exit button.
        self.exit_button = Button(self.text_frame, text="Exit", command=self.destroy)
        self.label_text.pack()
        self.text.pack()
        self.exit_button.pack()

    def insert_to_text(self, delete, str):
        if delete == 1:
            self.text.delete("1.0", "end")
        self.text.insert(tk.END, str)

    def get_arr(self):
        arr_str = "Array:   "
        self.data_arr = self.input_arr.get()
        self.data_arr = self.data_arr.split(",")
        for i in range(len(self.data_arr)):
            arr_str += f"{self.data_arr[i]}   "
            self.data_arr[i] = int(self.data_arr[i])

        arr_str += "\n"
        self.insert_to_text(1, arr_str)

    def open_file_dialog(self):
        arr_str = "Array:    "
        self.file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )
        self.text.delete("1.0", "end")
        data = pd.read_csv(self.file_path)
        self.data_arr = data["Array"].tolist()
        self.filename.set(self.file_path)

        for i in range(len(self.data_arr)):
            arr_str += f"{str(self.data_arr[i])}  "

        arr_str += "\n"
        self.insert_to_text(1, arr_str)

    def print_node(self, x_coord, y_coord, str):
        text = self.canvas.create_text(
            x_coord, y_coord, text=str, fill="dark green", font=("Helvetica 14 bold")
        )
        return self.canvas.coords(text)

    def print_edge(self, parent_coord, child_coord):
        self.canvas.create_line(
            parent_coord[0],
            parent_coord[1] + 50,
            child_coord[0],
            child_coord[1] - 50,
            width=3,
            fill="dark green",
        )

    def print_tree(self, tree):
        queue = []
        len_arr = len(tree)

        # set coordinate of tree
        tree_width = 630
        tree_height = 950

        # set distance of node:
        y_node_dis = tree_height / (math.log2(len_arr) // 1)
        x_node_dis = tree_width
        x_coord_root = 630
        y_coord_root = 55
        first_coord = x_coord_root

        # print root node
        node_str = f"""[{self.idx_tree_arr[0][0]} , {self.idx_tree_arr[0][1]})\nSum: {self.sum_tree_arr.container()[0]}\nMin: {self.min_tree_arr.container()[0]}\nMax: {self.max_tree_arr.container()[0]}"""
        parent_line = self.print_node(x_coord_root, y_coord_root, node_str)
        queue.append(parent_line)
        i = 1
        while i < len_arr:
            level = math.log2(i + 1) // 1

            # y_coord: set y coordinate of node
            y_cord = y_coord_root + level * y_node_dis

            # x_coord: set x coordinate of first node of level
            x_node_dis /= 2
            dis_node = x_node_dis * 2
            first_coord = first_coord - x_node_dis

            j = 0
            while i < len_arr and j < int(2**level):
                for z in range(2):
                    if tree[i] != None:
                        node_str = f"""[{self.idx_tree_arr[i][0]} , {self.idx_tree_arr[i][1]})\nSum: {self.sum_tree_arr.container()[i]}\nMin: {self.min_tree_arr.container()[i]}\nMax: {self.max_tree_arr.container()[i]}"""
                        child_coord = self.print_node(
                            first_coord + dis_node * j, y_cord, node_str
                        )
                        child_coord.append(i)
                        queue.append(child_coord)
                        parent_coord = queue[0]
                        self.print_edge(parent_coord, child_coord)
                    else:
                        queue.append(None)
                    i = i + 1
                    j = j + 1
                queue.pop(0)

    def build_button(self):
        self.canvas.delete("all")
        self.max_tree_arr = seg.build_max_tree(self.data_arr)
        self.min_tree_arr = seg.build_min_tree(self.data_arr)
        self.sum_tree_arr = seg.build_sum_tree(self.data_arr)
        self.idx_tree_arr = seg.tree_container_indexes_manager(len(self.data_arr))
        self.print_tree(self.idx_tree_arr)

    def get_button(self):
        query_str = "Query: \n"

        idx_pair = [(self.left_idx.get(), self.right_idx.get())]
        if self.min.get() == 1:
            query_str += f"Min: {self.min_tree_arr.query_min(idx_pair)}\n"
        if self.max.get() == 1:
            query_str += f"Max: {self.max_tree_arr.query_max(idx_pair)}\n"
        if self.sum.get() == 1:
            query_str += f"Sum: {self.sum_tree_arr.query_sum(idx_pair)}\n"

        self.insert_to_text(0, query_str)

    def update_button(self):
        self.data_arr[self.update_idx.get()] = self.update_value.get()

        arr_str = "New Array:   "
        for i in range(len(self.data_arr)):
            arr_str += f"{str(self.data_arr[i])}   "

        arr_str += "\n"
        self.insert_to_text(0, arr_str)

        value_n_idx = [(self.update_value.get(), self.update_idx.get())]

        self.min_tree_arr.update_min(value_n_idx)
        self.max_tree_arr.update_max(value_n_idx)
        self.sum_tree_arr.update_sum(value_n_idx)

        self.canvas.delete("all")
        self.print_tree(self.idx_tree_arr)
