import tkinter as tk
from tkinter import ttk
from .tabs.todo_tab import TodoTab
from .tabs.schedule_tab import ScheduleTab
from .tabs.countdown_tab import CountdownTab
from .tabs.alarm_tab import AlarmTab

class ControlPanel:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("控制面板")
        
        # 创建选项卡
        self.notebook = ttk.Notebook(self.window)
        
        # 添加各个功能标签页
        self.todo_tab = TodoTab(self.notebook)
        self.schedule_tab = ScheduleTab(self.notebook)
        self.countdown_tab = CountdownTab(self.notebook)
        self.alarm_tab = AlarmTab(self.notebook)
        
        # 将标签页添加到notebook
        self.notebook.add(self.todo_tab, text="待办事项")
        self.notebook.add(self.schedule_tab, text="日程安排")
        self.notebook.add(self.countdown_tab, text="倒计时")
        self.notebook.add(self.alarm_tab, text="闹钟")
        
        self.notebook.pack(expand=True, fill='both') 