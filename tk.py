import tkinter as tk
# tkinter 是 Python 标准库的一部分，用于创建图形用户界面（GUI）。
# ttk 是对这些控件的改进，使用系统的本地主题来显示更现代的外观，同时增加了更多功能。
# from tkinter import ttk
# 表示仅从 tkinter 模块中导入 ttk 子模块，而不是导入整个 tkinter。
# 导入后，ttk 里的控件可以直接使用，例如：ttk.Label()、ttk.Button() 等。
from tkinter import ttk
import time
from datetime import datetime
import json
from tkinter import messagebox


class TimeManager:
    # 在Python中，__init__是一个类的特殊方法，被称为
    # 构造函数。它的主要作用是在创建类的实例时对实例对象进行初始化。
    def __init__(self):
        # 主窗口设置
        self.root = tk.Tk()
        self.root.title("时间管理助手")
        self.root.attributes('-topmost', True) # 设置窗口的属性，-topmost 选项会将窗口置顶。
        self.root.overrideredirect(True)  # 无边框窗口

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 时钟标签
        # Label 控件是用来显示文本或图像的，通常用于显示信息、状态、标题
        self.time_label = tk.Label(
            self.root,
            font=('Arial', 24), # 标签的字体样式
            bg='black', # 标签的背景颜色
            fg='white', # 标签中文字的颜色
            padx=10, # 标签内容与其左右边缘之间的水平内边距
            pady=5 # 标签内容与上下边缘之间的垂直内边距
        )
        self.time_label.pack() # 将 time_label 控件添加到父容器

        # 控制面板窗口
        self.control_panel = None

        # 数据存储
        self.todos = []
        self.schedules = []
        self.alarms = []
        self.countdown = None

        # 绑定鼠标事件
        self.time_label.bind('<Button-1>', self.show_control_panel)  # 左键点击显示控制面板
        self.time_label.bind('<Button-3>', self.quit_app)  # 右键点击退出应用
        self.time_label.bind('<B1-Motion>', self.drag_window)  # 左键拖动窗口
        self.time_label.bind('<ButtonPress-1>', self.start_drag)  # 开始拖动

        # 更新时钟
        self.update_clock()

        # 初始位置（右下角）
        x = screen_width - self.root.winfo_reqwidth() - 50
        y = screen_height - self.root.winfo_reqheight() - 50
        # 设置窗口的位置和大小。
        # 该方法接受一个字符串作为参数，字符串可以包含窗口的尺寸（宽x高）和位置（x, y）。
        # 格式为 f'+{x}+{y}'，即只设置窗口的位置信息（不改变大小）。
        # +{x}+{y}：将窗口的位置设置为屏幕右下角偏移 50像素的地方，其中x和y是计算得到的屏幕坐标。
        self.root.geometry(f'+{x}+{y}')

    def update_clock(self):
        """更新时钟显示"""
        current_time = time.strftime('%H:%M:%S')
        # 更新 time_label 标签的配置
        # text=current_time：将 time_label 的文本内容设置为刚才获取到的当前时间。
        self.time_label.config(text=current_time)
        # .root.after 是tkinter 中用于创建定时器的方法
        # self.update_clock：这是我们定义的方法。表示 1 秒钟后再次调用 update_clock 方法，从而实现每秒更新一次时间。
        self.root.after(1000, self.update_clock)

    def show_control_panel(self, event):
        """显示控制面板"""
        # winfo_exists 方法检查该窗口是否仍然存在
        if self.control_panel is None or not tk.Toplevel.winfo_exists(self.control_panel):
            # tk.Toplevel(self.root)：Toplevel 是 tkinter 中的一个类，用来创建新的顶级窗口（即子窗口）。与 Tk 窗口不同，Toplevel 窗口是从父窗口（在这里是 self.root）派生出来的。
            # self.root：指定 Toplevel 窗口的父窗口。这里，self.root 是主窗口，Toplevel 窗口会在主窗口之上弹出。
            self.control_panel = tk.Toplevel(self.root)
            self.control_panel.title("控制面板")

            # 创建选项卡
            # Notebook 控件允许你在同一个窗口中展示多个“页面”或“标签页”，每个标签页内可以包含不同的控件和内容。
            notebook = ttk.Notebook(self.control_panel)

            # 待办事项标签页
            todo_frame = ttk.Frame(notebook)
            self.create_todo_tab(todo_frame)
            notebook.add(todo_frame, text="待办事项")

            # 日程安排标签页
            schedule_frame = ttk.Frame(notebook)
            self.create_schedule_tab(schedule_frame)
            notebook.add(schedule_frame, text="日程安排")

            # 倒计时标签页
            countdown_frame = ttk.Frame(notebook)
            self.create_countdown_tab(countdown_frame)
            notebook.add(countdown_frame, text="倒计时")

            # 闹钟标签页
            alarm_frame = ttk.Frame(notebook)
            self.create_alarm_tab(alarm_frame)
            notebook.add(alarm_frame, text="闹钟")

            notebook.pack(expand=True, fill='both')

    def create_todo_tab(self, parent):
        """创建待办事项标签页"""
        # 添加待办输入框
        entry_frame = ttk.Frame(parent)
        entry_frame.pack(fill='x', padx=5, pady=5)

        self.todo_entry = ttk.Entry(entry_frame)
        self.todo_entry.pack(side='left', expand=True, fill='x')

        add_btn = ttk.Button(entry_frame, text="添加", command=self.add_todo)
        add_btn.pack(side='right')

        # 待办列表
        self.todo_listbox = tk.Listbox(parent)
        self.todo_listbox.pack(fill='both', expand=True, padx=5, pady=5)

    def create_schedule_tab(self, parent):
        """创建日程安排标签页"""
        # 时间选择
        time_frame = ttk.Frame(parent)
        time_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(time_frame, text="时间:").pack(side='left')
        self.schedule_time = ttk.Entry(time_frame)
        self.schedule_time.pack(side='left')

        # 事项输入
        event_frame = ttk.Frame(parent)
        event_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(event_frame, text="事项:").pack(side='left')
        self.schedule_entry = ttk.Entry(event_frame)
        self.schedule_entry.pack(side='left', expand=True, fill='x')

        add_btn = ttk.Button(event_frame, text="添加", command=self.add_schedule)
        add_btn.pack(side='right')

        # 日程列表
        self.schedule_listbox = tk.Listbox(parent)
        self.schedule_listbox.pack(fill='both', expand=True, padx=5, pady=5)

    def create_countdown_tab(self, parent):
        """创建倒计时标签页"""
        # 时间设置
        frame = ttk.Frame(parent)
        frame.pack(padx=5, pady=5)

        ttk.Label(frame, text="分钟:").pack(side='left')
        self.countdown_entry = ttk.Entry(frame, width=10)
        self.countdown_entry.pack(side='left')

        ttk.Button(frame, text="开始", command=self.start_countdown).pack(side='left', padx=5)
        ttk.Button(frame, text="停止", command=self.stop_countdown).pack(side='left')

        # 倒计时显示
        self.countdown_label = ttk.Label(parent, text="未开始", font=('Arial', 20))
        self.countdown_label.pack(pady=20)

    def create_alarm_tab(self, parent):
        """创建闹钟标签页"""
        # 时间设置
        frame = ttk.Frame(parent)
        frame.pack(padx=5, pady=5)

        ttk.Label(frame, text="时间(HH:MM):").pack(side='left')
        self.alarm_entry = ttk.Entry(frame, width=10)
        self.alarm_entry.pack(side='left')

        ttk.Button(frame, text="添加", command=self.add_alarm).pack(side='left', padx=5)

        # 闹钟列表
        self.alarm_listbox = tk.Listbox(parent)
        self.alarm_listbox.pack(fill='both', expand=True, padx=5, pady=5)

    def add_todo(self):
        """添加待办事项"""
        todo = self.todo_entry.get()
        if todo:
            self.todos.append(todo)
            self.todo_listbox.insert(tk.END, todo)
            self.todo_entry.delete(0, tk.END)

    def add_schedule(self):
        """添加日程"""
        time_str = self.schedule_time.get()
        event = self.schedule_entry.get()
        if time_str and event:
            schedule = f"{time_str} - {event}"
            self.schedules.append(schedule)
            self.schedule_listbox.insert(tk.END, schedule)
            self.schedule_time.delete(0, tk.END)
            self.schedule_entry.delete(0, tk.END)

    def start_countdown(self):
        """开始倒计时"""
        try:
            minutes = int(self.countdown_entry.get())
            self.countdown = minutes * 60
            self.update_countdown()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的分钟数")

    def update_countdown(self):
        """更新倒计时"""
        if self.countdown is not None and self.countdown > 0:
            minutes = self.countdown // 60
            seconds = self.countdown % 60
            self.countdown_label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.countdown -= 1
            self.root.after(1000, self.update_countdown)
        elif self.countdown == 0:
            messagebox.showinfo("提示", "倒计时结束！")
            self.countdown = None
            self.countdown_label.config(text="未开始")

    def stop_countdown(self):
        """停止倒计时"""
        self.countdown = None
        self.countdown_label.config(text="未开始")

    def add_alarm(self):
        """添加闹钟"""
        alarm_time = self.alarm_entry.get()
        try:
            datetime.strptime(alarm_time, '%H:%M')
            self.alarms.append(alarm_time)
            self.alarm_listbox.insert(tk.END, alarm_time)
            self.alarm_entry.delete(0, tk.END)
            self.check_alarms()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的时间格式(HH:MM)")

    def check_alarms(self):
        """检查闹钟"""
        current_time = time.strftime('%H:%M')
        for alarm in self.aalarms:
            if alarm == current_time:
                messagebox.showinfo("闹钟", f"时间到了！现在是 {alarm}")
        self.root.after(1000, self.check_alarms)

    def start_drag(self, event):
        """开始拖动时记录鼠标位置"""
        self._drag_data = {'x': event.x, 'y': event.y}

    def drag_window(self, event):
        """处理窗口拖动"""
        if hasattr(self, '_drag_data'):
            # 计算新位置
            deltax = event.x - self._drag_data['x']
            deltay = event.y - self._drag_data['y']
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f'+{x}+{y}')

    def quit_app(self, event):
        """退出应用程序"""
        self.root.quit()

    def run(self):
        """运行程序"""
        self.root.mainloop()


if __name__ == "__main__":
    app = TimeManager()
    app.run()
