import os
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mbox

# from collections import OrderedDict

VERSION = 'v0.0.1'

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

    # Solve the problem of page scaling
    matplotlib.use('TkAgg')
except Exception as e:
    print(e)
    print('Failed to import modules')


# make sure just one instance
def singleton(cls):
    """
    To be used like
    @singleton
    instances = {}
    :param cls:
    :return:
    """
    _instance_dict = {}

    def inner(*args, **kwargs):
        if cls not in _instance_dict:
            _instance_dict[cls] = cls(*args, **kwargs)
        return _instance_dict.get(cls)

    return inner


def ctype2dict(struct):
    """
    Convert ctypes StructType object to python dictionary
    _dict = {}
    :param struct:
    :return:
    """
    result = {}
    for field, _ in struct._fields_:
        value = getattr(struct, field)
        # if the type is not a primitive, and it evaluates to False ...
        if (type(value) not in [int, float, bool]) and not bool(value):
            # it's a null pointer
            value = None
        elif hasattr(value, "_length_") and hasattr(value, "_type_"):
            # Probably an array
            value = list(value)
            for i in range(len(value)):
                if hasattr(value[i], "_fields_"):
                    value[i] = ctype2dict(value[i])
        elif hasattr(value, "_fields_"):
            # Probably another struct
            value = ctype2dict(value)
        result[field] = value
    return result


SINGLE = 1
MULTI = 2


@singleton
class DebugGUI:
    def __init__(self, master):
        self.queue = []
        self.mode = SINGLE
        self.monitor = OFF
        self.root = master
        self.cbox = None
        self.name_cbox = None
        self.index_cbox = None
        self.props_list = None
        self.checkbox = None
        self.canvas = Canvas()
        self.figure = None
        self.sub_fig = None
        self.sub_figs = []
        self.sub_window = None
        self.lines = []
        self.parameters = {"FG": ("FGInfoIni",), "BG": (
            "BGInfoIni",), "CUS": ("CUSInfoIni",), "OBJ": ("OBJInfoIni",), "Goody": ("GoodyInfoIni",)}
        self.default_props = ("xstart", "ystart", "xscale", "yscale", "rotAngle", "shearH", "shearV", "alphaNor")
        self.goodie_props = ("gap", "index", "scale", "initNum", "x", "y", "height", "width", "show")
        self.goodie_keys = []

        self.setup_ui()

    def setup_ui(self):
        # set window title
        self.root.title(f"Debug Window {VERSION}")
        # set window size
        self.root.geometry("500x500+10+10")
        # disable resize
        self.root.resizable(width=False, height=False)
        # set window bg color
        self.root.configure(background="#fff")
        # set window focus
        self.root.focus_force()
        # set label text and position
        ttk.Label(self.root, background="#ffffff", text="Select parameter name for debug:",
                  font=("Helvetica", 10, "bold"), anchor="w", justify="left").grid(column=0, row=3, padx=10, pady=25)

        val = StringVar()
        values = self.parameters.keys()
        cbox = ttk.Combobox(
            master=self.root,
            height=10,
            width=24,
            state='normal',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('Helvetica', 12),  # 字体
            textvariable=val,  # 通过StringVar设置可改变的值
            values=tuple(values),  # 设置下拉框的选项
        )
        cbox.grid(column=1, row=3)
        cbox.bind("<<ComboboxSelected>>", self.on_cbox_changed)
        self.cbox = cbox

        ttk.Label(self.root, background="#ffffff", text="Select parameter for debug:",
                  font=("Helvetica", 10, "bold"), anchor="w", justify="left").grid(column=0, row=6, padx=10, pady=25)
        value = StringVar()
        name_cbox = ttk.Combobox(
            master=self.root,
            height=10,
            width=24,
            state='normal',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('Helvetica', 12),  # 字体
            textvariable=value,  # 通过StringVar设置可改变的值
        )
        name_cbox.grid(column=1, row=6)
        name_cbox.bind("<<ComboboxSelected>>", self.on_name_cbox_changed)
        self.name_cbox = name_cbox

        ttk.Label(self.root, background="#ffffff", text="Select index of parameters:",
                  font=("Helvetica", 10, "bold"), anchor="w", justify="left").grid(column=0, row=9, padx=10, pady=25)
        index_value = StringVar()
        index_cbox = ttk.Combobox(
            master=self.root,
            height=10,
            width=24,
            state='normal',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('Helvetica', 12),  # 字体
            textvariable=index_value,  # 通过StringVar设置可改变的值
        )
        index_cbox.grid(column=1, row=9)
        index_cbox.bind("<<ComboboxSelected>>", self.reset)
        self.index_cbox = index_cbox

        ttk.Label(self.root, background="#ffffff", text="Select prop of parameter:",
                  font=("Helvetica", 10, "bold"), anchor="w", justify="left").grid(column=0, row=12, padx=10, pady=25)

        props = StringVar(value=self.default_props)
        props_list = Listbox(
            master=self.root,
            width=24,
            height=10,
            selectmode="multiple",
            cursor="arrow",
            font=('Helvetica', 12),
            listvariable=props
        )
        props_list.grid(column=1, row=12)
        props_list.bind('<<ListboxSelect>>', self.on_props_list_changed)
        self.props_list = props_list

        check_val = IntVar(value=SINGLE)
        checkbox = Checkbutton(master=self.root, background="#ffffff", text="Set multiple charts", variable=check_val,
                               onvalue=MULTI,
                               offvalue=SINGLE, font=("Helvetica", 10, "bold"), justify="left")
        checkbox.grid(column=0, row=14)
        self.checkbox = checkbox
        self.mode = check_val

        btn = Button(bg="#007fff", foreground="#fff", text="Confirm", command=self.confirm_handler,
                     font=("Helvetica", 14, "bold"))
        btn.grid(column=1, row=15, padx=30, pady=20)

    def setup_figure(self):
        name = self.name_cbox.get()
        props = self.props_list.curselection()
        rows = self.get_current_props()

        f = plt.figure(num=1, figsize=(12, 8), dpi=100,
                       edgecolor='green', frameon=True)

        sub_fig = plt.subplot(1, 1, 1)

        sub_fig.set_title(label=f'Debug {name} - {",".join([rows[i] for i in props])}', color='black', loc='center')
        sub_fig.set_xlabel('time')
        sub_fig.set_ylabel('props')

        f.tight_layout()

        self.lines = [0] * (max(props) + 1)
        # create lines from props
        for i in props:
            p = rows[i]
            line, = sub_fig.plot([], [], label=p)
            self.lines[i] = line

        self.sub_fig = sub_fig
        self.figure = f

    def setup_figures(self):
        idx = 1
        name = self.name_cbox.get()
        props = self.props_list.curselection()
        rows = self.get_current_props()
        sub_figs = [0] * (max(props) + 1)

        f = plt.figure(num=2, figsize=(12, 8), dpi=100,
                       edgecolor='green', frameon=True)
        self.lines = [0] * (max(props) + 1)

        for i in props:
            p = rows[i]
            sub_fig = plt.subplot(len(props), 1, idx)
            idx += 1
            sub_fig.set_title(label=f'Debug {name} - {p}', color='black', loc='center')
            sub_fig.set_xlabel('time')
            sub_fig.set_ylabel(p)
            sub_figs[i] = sub_fig
            # create lines from props
            line, = sub_fig.plot([], [], label=p)
            self.lines[i] = line

        f.tight_layout()

        self.sub_figs = sub_figs
        self.figure = f

    def on_cbox_changed(self, _):
        if self.cbox is not None:
            v = self.cbox.get()
            self.name_cbox["values"] = self.parameters[v]
            self.reset()

    def on_name_cbox_changed(self, _):
        if self.name_cbox is not None:
            v = self.name_cbox.get()
            n = 8 if "InfoIni" in v else 3
            if v != "GoodyInfoIni":
                self.index_cbox["values"] = [i for i in range(1, n + 1)]
            else:
                self.index_cbox["values"] = list(filter(lambda x: x, self.goodie_keys))

            self.props_list.delete(0, END)
            for row in self.get_current_props():
                self.props_list.insert(END, row)

            self.reset()

    def on_props_list_changed(self, _):
        # limit the number of props
        if len(self.props_list.curselection()) > 2:
            self.props_list.selection_clear(0, END)
        self.reset()

    def get_current_props(self):
        v = self.name_cbox.get()
        if v == "GoodyInfoIni":
            return self.goodie_props
        else:
            return self.default_props

    def confirm_handler(self):
        param = self.cbox.get()
        name = self.name_cbox.get()
        index = self.index_cbox.get()
        props = self.props_list.curselection()
        mode = self.mode.get()

        if param and name and index and len(props) > 0:
            if mode == SINGLE:
                self.setup_figure()
            elif mode == MULTI:
                self.setup_figures()

            self.create_matplotlib(f'Monitor {self.name_cbox.get()} - Index: {self.index_cbox.get()}')
        else:
            mbox.showwarning("Tip", "Please select valid parameters!")

    def create_matplotlib(self, title):
        # create sub window
        sub_window = Toplevel(self.root)
        sub_window.title(title)
        sub_window.geometry("1200x600+10+510")
        # force focus
        sub_window.focus_force()
        sub_window.protocol("WM_DELETE_WINDOW", self.reset)

        self.canvas = FigureCanvasTkAgg(self.figure, sub_window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP)
        toolbar = NavigationToolbar2Tk(self.canvas, sub_window)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.sub_window = sub_window

    def pack_payload(self, payload):
        if win is None:
            return

        name = self.name_cbox.get()
        index = self.index_cbox.get()

        if name:
            if len(self.goodie_keys) == 0:
                data = payload[name]
                val = ctype2dict(data) if hasattr(data, "_fields_") else data
                if "GoodyInfo" in val:
                    goody_info = val["GoodyInfo"]
                    self.goodie_keys = list(
                        map(lambda x: bytes.decode(x["goodyString"]) if x["goodyString"] is not None else x[
                            "goodyString"], goody_info))
                    self.index_cbox["values"] = list(filter(lambda x: x, self.goodie_keys))

            if index:
                try:
                    data = payload[name]
                    val = ctype2dict(data) if hasattr(data, "_fields_") else data

                    if name != "GoodyInfoIni":
                        index = int(index)
                    else:
                        if index in self.goodie_keys:
                            index = self.goodie_keys.index(index) + 1

                    timestamp = payload["timestamp"]

                    if "verified" in val and name != "GoodyInfoIni":
                        if val["verified"][index - 1] == 0:
                            return

                    filed_name = name.replace("Ini", "")
                    filed = val[filed_name][index - 1]
                    source = {"item": filed, "timestamp": timestamp}
                    # set queue max size is 50
                    if len(self.queue) > 50:
                        self.queue.pop(0)
                    self.queue.append(source)
                    self.update_graph()
                except Exception as err:
                    print(repr(err))

    # update chart from queue data
    def update_graph(self):
        mode = self.mode.get()
        props = self.props_list.curselection()

        if len(props) == 0 or self.sub_window is None:
            return

        for i in props:
            rows = self.get_current_props()
            p = rows[i]
            if len(self.lines) > 0 and self.lines[i]:
                ln = self.lines[i]
                ln.set_xdata(list(map(lambda x: x["timestamp"], self.queue)))
                ln.set_ydata(list(map(lambda x: x["item"][p], self.queue)))

        if self.sub_fig is not None or len(self.sub_figs) != 0:
            if mode == SINGLE:
                self.sub_fig.relim()
                self.sub_fig.autoscale_view()
                plt.legend()
            else:
                for i in props:
                    self.sub_figs[i].relim()
                    self.sub_figs[i].autoscale_view()
                    self.sub_figs[i].legend()

        # Remove duplicate redundant legends
        # handles, labels = plt.gca().get_legend_handles_labels()
        # by_label = OrderedDict(zip(labels, handles))
        # plt.legend(by_label.values(), by_label.keys())

        self.canvas.draw()

    def quit(self):
        self.root.quit()
        self.root.destroy()

    def reset(self, *args):
        self.queue.clear()
        self.lines.clear()
        if self.sub_window:
            self.sub_window.destroy()
            self.sub_window.update()
            self.sub_window = None
        self.root.update()
        plt.close()


@singleton
class Monitor:
    def __init__(self, master):
        self.queue = []
        self.mode = SINGLE
        self.root = master
        self.canvas = Canvas()
        self.figure = None
        self.sub_fig = None
        self.lines = {}
        self.stage = 1
        self.currentIdx = 0

        self.setup()

    def setup(self):
        # set window title
        self.root.title(f"Monitor Window {VERSION}")
        # set window size
        self.root.geometry("800x400+10+10")
        # set window bg color
        self.root.configure(background="#fff")

        btn = Button(bg="#007fff", foreground="#fff", text="Snapshot", command=self.snapshot,
                     font=("Helvetica", 14, "bold"))
        btn.pack(side=TOP, anchor="w", padx=10, pady=10)

        f = plt.figure(num=3, figsize=(12, 8), dpi=100,
                       edgecolor='green', frameon=True)
        sub_fig = plt.subplot(1, 1, 1)
        sub_fig.set_title(label=f'Monitor variables', color='black', loc='center')
        sub_fig.set_xlabel('time')
        sub_fig.set_ylabel("variables")

        f.tight_layout()

        self.canvas = FigureCanvasTkAgg(f, self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP)
        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.figure = f
        self.sub_fig = sub_fig

    def snapshot(self):
        folder = os.path.dirname(os.path.abspath(__file__)).split("\\")
        snapshots_folder = os.path.join("C:\\integem\\pythonLogs\\", folder[-1])
        print(snapshots_folder)
        if not os.path.isdir(snapshots_folder):
            os.mkdir(snapshots_folder)
        filename = f'{snapshots_folder}\\timeIndex - {self.currentIdx}.png'
        plt.savefig(filename)

    def matches(self, time_index):
        return next((item for item in self.queue if item["timestamp"] == time_index), None)

    def monitor_variables(self, stage, time_index, variables):
        if win is None:
            return

        if stage != self.stage:
            self.lines = {}
            self.queue = []

        # set queue max size is 50
        if len(self.queue) > 30:
            self.queue.pop(0)

        keys = variables.keys()

        for k in keys:
            # create lines from props
            if k not in self.lines:
                line, = self.sub_fig.plot([], [], '.--', label=k)
                self.lines[k] = line

        if self.currentIdx != time_index and len(self.queue) > 0:
            for k in self.lines.keys():
                ln = self.lines[k]
                q = list(filter(lambda x: k in x['items'], self.queue))
                ln.set_xdata(list(map(lambda x: x["timestamp"], q)))
                ln.set_ydata(list(map(lambda x: x["items"][k], q)))

            self.sub_fig.relim()
            self.sub_fig.autoscale_view()
            self.sub_fig.legend()

            self.canvas.draw()

        match = self.matches(time_index)

        if match is None:
            self.queue.append({
                "items": variables,
                "timestamp": time_index
            })
        else:
            match['items'].update(variables)

        self.currentIdx = time_index
        self.stage = stage

    def quit(self):
        self.root.quit()
        self.root.destroy()


def read_debug_flag():
    """
    Read debug flag from config file
    :return: debug flag
    """
    try:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "debugConfig.txt")) as f:
            for line in f:
                if line.startswith("Debug="):
                    return int(line.split("=")[1].strip())
            return 0
    except Exception as e:
        print(repr(e))
        return 0


win = None
FLAG = read_debug_flag()
DEBUG_PLOT_FLAG = 2
DEBUG_PLOT_INTERFACE_FLAG = 3


def debug_plot_start():
    global win
    root = Tk()

    win = Monitor(root)
    root.mainloop()


def debug_plot_interface_start():
    global win
    root = Tk()

    win = DebugGUI(root)
    root.mainloop()


def run():
    if FLAG == DEBUG_PLOT_FLAG:
        debug_plot_start()
    elif FLAG == DEBUG_PLOT_INTERFACE_FLAG:
        debug_plot_interface_start()
