from tkinter import ttk, messagebox
from datetime import datetime
import time
from .base_tab import BaseTab

class AlarmTab(BaseTab):
    def __init__(self, notebook):
        self.alarms = []
        super().__init__(notebook)
        # 开始检查闹钟
        self.check_alarms()

    def create_widgets(self):
        """创建闹钟标签页的控件"""
        # 时间设置框架
        time_frame = ttk.Frame(self)
        time_frame.pack(padx=5, pady=5)

        # 小时选择
        ttk.Label(time_frame, text="时:").pack(side='left')
        self.alarm_hour = ttk.Spinbox(
            time_frame, 
            from_=0, 
            to=23, 
            width=3,
            format="%02.0f"
        )
        self.alarm_hour.pack(side='left', padx=(0,10))
        self.alarm_hour.set("00")

        # 分钟选择
        ttk.Label(time_frame, text="分:").pack(side='left')
        self.alarm_minute = ttk.Spinbox(
            time_frame, 
            from_=0, 
            to=59, 
            width=3,
            format="%02.0f"
        )
        self.alarm_minute.pack(side='left')
        self.alarm_minute.set("00")

        ttk.Button(time_frame, text="添加", command=self.add_alarm).pack(side='left', padx=10)

        # 闹钟列表
        self.alarm_listbox = ttk.Treeview(
            self,
            columns=('time',),
            show='headings'
        )
        self.alarm_listbox.heading('time', text='闹钟时间')
        self.alarm_listbox.pack(fill='both', expand=True, padx=5, pady=5)

    def add_alarm(self):
        """添加闹钟"""
        try:
            hour = int(self.alarm_hour.get())
            minute = int(self.alarm_minute.get())
            alarm_time = f"{hour:02d}:{minute:02d}"
            
            # 验证时间格式
            datetime.strptime(alarm_time, '%H:%M')
            
            self.alarms.append(alarm_time)
            self.alarm_listbox.insert('', 'end', values=(alarm_time,))
            self.alarm_hour.set("00")
            self.alarm_minute.set("00")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的时间")

    def check_alarms(self):
        """检查闹钟"""
        current_time = time.strftime('%H:%M')
        for alarm in self.alarms:
            if alarm == current_time:
                messagebox.showinfo("闹钟", f"时间到了！现在是 {alarm}")
        self.after(1000, self.check_alarms) 