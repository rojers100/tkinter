from tkinter import ttk, messagebox
from datetime import datetime
from .base_tab import BaseTab

class ScheduleTab(BaseTab):
    def __init__(self, notebook):
        self.schedules = []
        super().__init__(notebook)

    def create_widgets(self):
        """创建日程安排标签页的控件"""
        # 时间选择框架
        time_frame = ttk.Frame(self)
        time_frame.pack(fill='x', padx=5, pady=5)

        # 开始时间
        ttk.Label(time_frame, text="开始时间:").pack(side='left')
        
        # 开始时间 - 小时
        self.start_hour = ttk.Spinbox(
            time_frame,
            from_=0,
            to=23,
            width=3,
            format="%02.0f"
        )
        self.start_hour.pack(side='left')
        self.start_hour.set("00")
        
        ttk.Label(time_frame, text=":").pack(side='left')
        
        # 开始时间 - 分钟
        self.start_minute = ttk.Spinbox(
            time_frame,
            from_=0,
            to=59,
            width=3,
            format="%02.0f"
        )
        self.start_minute.pack(side='left')
        self.start_minute.set("00")
        
        # 结束时间
        ttk.Label(time_frame, text="  结束时间:").pack(side='left')
        
        # 结束时间 - 小时
        self.end_hour = ttk.Spinbox(
            time_frame,
            from_=0,
            to=23,
            width=3,
            format="%02.0f"
        )
        self.end_hour.pack(side='left')
        self.end_hour.set("00")
        
        ttk.Label(time_frame, text=":").pack(side='left')
        
        # 结束时间 - 分钟
        self.end_minute = ttk.Spinbox(
            time_frame,
            from_=0,
            to=59,
            width=3,
            format="%02.0f"
        )
        self.end_minute.pack(side='left')
        self.end_minute.set("00")

        # 事项输入框架
        event_frame = ttk.Frame(self)
        event_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(event_frame, text="事项:").pack(side='left')
        self.schedule_entry = ttk.Entry(event_frame)
        self.schedule_entry.pack(side='left', expand=True, fill='x')

        add_btn = ttk.Button(event_frame, text="添加", command=self.add_schedule)
        add_btn.pack(side='right')

        # 日程列表
        self.schedule_listbox = ttk.Treeview(
            self,
            columns=('time', 'event'),
            show='headings'
        )
        self.schedule_listbox.heading('time', text='时间')
        self.schedule_listbox.heading('event', text='事项')
        self.schedule_listbox.pack(fill='both', expand=True, padx=5, pady=5)

    def add_schedule(self):
        """添加日程"""
        event = self.schedule_entry.get()
        if event:
            try:
                # 获取并格式化时间
                start_time = f"{int(self.start_hour.get()):02d}:{int(self.start_minute.get()):02d}"
                end_time = f"{int(self.end_hour.get()):02d}:{int(self.end_minute.get()):02d}"
                
                # 验证时间格式
                datetime.strptime(start_time, '%H:%M')
                datetime.strptime(end_time, '%H:%M')
                
                # 验证结束时间是否晚于开始时间
                start_minutes = int(self.start_hour.get()) * 60 + int(self.start_minute.get())
                end_minutes = int(self.end_hour.get()) * 60 + int(self.end_minute.get())
                
                if end_minutes <= start_minutes:
                    messagebox.showerror("错误", "结束时间必须晚于开始时间")
                    return
                
                # 格式化日程显示
                time_str = f"{start_time} - {end_time}"
                
                # 添加到列表
                self.schedules.append((time_str, event))
                self.schedule_listbox.insert('', 'end', values=(time_str, event))
                
                # 清空输入
                self.schedule_entry.delete(0, 'end')
                self.start_hour.set("00")
                self.start_minute.set("00")
                self.end_hour.set("00")
                self.end_minute.set("00")
                
            except ValueError:
                messagebox.showerror("错误", "请输入有效的时间格式") 