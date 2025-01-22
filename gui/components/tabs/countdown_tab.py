from tkinter import ttk, messagebox
from .base_tab import BaseTab

class CountdownTab(BaseTab):
    def __init__(self, notebook):
        self.countdown = None
        super().__init__(notebook)

    def create_widgets(self):
        """创建倒计时标签页的控件"""
        # 时间设置框架
        time_frame = ttk.Frame(self)
        time_frame.pack(padx=5, pady=5)

        # 小时选择
        ttk.Label(time_frame, text="时:").pack(side='left')
        self.hours_spinbox = ttk.Spinbox(
            time_frame, 
            from_=0, 
            to=23, 
            width=3,
            format="%02.0f"
        )
        self.hours_spinbox.pack(side='left', padx=(0,10))
        self.hours_spinbox.set("00")

        # 分钟选择
        ttk.Label(time_frame, text="分:").pack(side='left')
        self.minutes_spinbox = ttk.Spinbox(
            time_frame, 
            from_=0, 
            to=59, 
            width=3,
            format="%02.0f"
        )
        self.minutes_spinbox.pack(side='left', padx=(0,10))
        self.minutes_spinbox.set("00")

        # 秒钟选择
        ttk.Label(time_frame, text="秒:").pack(side='left')
        self.seconds_spinbox = ttk.Spinbox(
            time_frame, 
            from_=0, 
            to=59, 
            width=3,
            format="%02.0f"
        )
        self.seconds_spinbox.pack(side='left')
        self.seconds_spinbox.set("00")

        # 按钮框架
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)
        
        ttk.Button(button_frame, text="开始", command=self.start_countdown).pack(side='left', padx=5)
        ttk.Button(button_frame, text="停止", command=self.stop_countdown).pack(side='left')

        # 倒计时显示
        self.countdown_label = ttk.Label(self, text="未开始", font=('Arial', 20))
        self.countdown_label.pack(pady=20)

    def start_countdown(self):
        """开始倒计时"""
        try:
            hours = int(self.hours_spinbox.get())
            minutes = int(self.minutes_spinbox.get())
            seconds = int(self.seconds_spinbox.get())
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            if total_seconds > 0:
                self.countdown = total_seconds
                self.update_countdown()
            else:
                messagebox.showerror("错误", "请设置大于0的时间")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的时间")

    def update_countdown(self):
        """更新倒计时"""
        if self.countdown is not None and self.countdown > 0:
            hours = self.countdown // 3600
            minutes = (self.countdown % 3600) // 60
            seconds = self.countdown % 60
            self.countdown_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.countdown -= 1
            self.after(1000, self.update_countdown)
        elif self.countdown == 0:
            messagebox.showinfo("提示", "倒计时结束！")
            self.countdown = None
            self.countdown_label.config(text="未开始")

    def stop_countdown(self):
        """停止倒计时"""
        self.countdown = None
        self.countdown_label.config(text="未开始") 