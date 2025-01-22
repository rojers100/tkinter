import tkinter as tk
from tkinter import ttk
from .components.clock_widget import ClockWidget
from .components.control_panel import ControlPanel

class TimeManager:
    def __init__(self):
        # 主窗口设置
        self.root = tk.Tk()
        self.root.title("时间管理助手")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)

        # 初始化时钟组件
        self.clock = ClockWidget(self.root)
        
        # 初始化控制面板
        self.control_panel = None

        # 设置初始位置
        self._set_initial_position()

        # 添加程序关闭处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _set_initial_position(self):
        """设置窗口初始位置"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - self.root.winfo_reqwidth() - 50
        y = screen_height - self.root.winfo_reqheight() - 50
        self.root.geometry(f'+{x}+{y}')

    def on_closing(self):
        """处理程序关闭"""
        try:
            # 关闭所有子窗口
            if self.control_panel and tk.Toplevel.winfo_exists(self.control_panel.window):
                self.control_panel.window.destroy()
            # 关闭主窗口
            self.root.quit()
        except:
            pass

    def run(self):
        """运行程序"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing() 