import tkinter as tk
import time
from ..utils.drag_mixin import DragMixin
from ..components.control_panel import ControlPanel

class ClockWidget(DragMixin):
    def __init__(self, master):
        self.label = tk.Label(
            master,
            font=('Arial', 24),
            bg='black',
            fg='white',
            padx=10,
            pady=5
        )
        self.label.pack()

        # 初始化拖拽功能
        super().__init__(self.label)
        
        # 控制面板
        self.control_panel = None
        
        # 绑定事件
        self.label.bind('<Button-1>', self.on_click)
        self.label.bind('<Button-3>', self.quit_app)
        self.label.bind('<ButtonRelease-1>', self.on_release)
        
        # 开始更新时钟
        self.update_clock()

    def update_clock(self):
        """更新时钟显示"""
        current_time = time.strftime('%H:%M:%S')
        self.label.config(text=current_time)
        self.label.after(1000, self.update_clock)

    def on_click(self, event):
        """处理左键点击事件"""
        # 记录点击开始的位置
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        self._click_time = time.time()
        self.start_drag(event)

    def on_release(self, event):
        """处理鼠标释放事件"""
        if not hasattr(self, '_is_dragging') or not self._is_dragging:
            # 如果没有拖动，则显示控制面板
            self.show_control_panel(event)
        
        # 重置拖动状态
        self._is_dragging = False
        if hasattr(self, '_drag_data'):
            del self._drag_data

    def show_control_panel(self, event):
        """显示控制面板"""
        if self.control_panel is None or not tk.Toplevel.winfo_exists(self.control_panel.window):
            self.control_panel = ControlPanel(self.label.master)

    def quit_app(self, event):
        """退出应用"""
        try:
            if self.control_panel and tk.Toplevel.winfo_exists(self.control_panel.window):
                self.control_panel.window.destroy()
            self.label.master.quit()
        except:
            pass 