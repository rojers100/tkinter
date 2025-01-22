from tkinter import ttk, messagebox
from datetime import datetime
from .base_tab import BaseTab

class TodoTab(BaseTab):
    def __init__(self, notebook):
        self.todos = []
        super().__init__(notebook)

    def create_widgets(self):
        """创建待办事项标签页的控件"""
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

        # 待办事项输入框架
        entry_frame = ttk.Frame(self)
        entry_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(entry_frame, text="待办事项:").pack(side='left')
        self.todo_entry = ttk.Entry(entry_frame)
        self.todo_entry.pack(side='left', expand=True, fill='x')

        add_btn = ttk.Button(entry_frame, text="添加", command=self.add_todo)
        add_btn.pack(side='right')

        # 待办列表
        self.todo_listbox = ttk.Treeview(
            self,
            columns=('time', 'task'),
            show='headings'
        )
        self.todo_listbox.heading('time', text='时间')
        self.todo_listbox.heading('task', text='待办事项')
        self.todo_listbox.pack(fill='both', expand=True, padx=5, pady=5)

    def add_todo(self):
        """添加待办事项"""
        todo_text = self.todo_entry.get()
        if todo_text:
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
                
                # 格式化待办事项显示
                time_str = f"{start_time} - {end_time}"
                
                # 添加到列表
                self.todos.append((time_str, todo_text))
                self.todo_listbox.insert('', 'end', values=(time_str, todo_text))
                
                # 清空输入
                self.todo_entry.delete(0, 'end')
                self.start_hour.set("00")
                self.start_minute.set("00")
                self.end_hour.set("00")
                self.end_minute.set("00")
                
            except ValueError:
                messagebox.showerror("错误", "请输入有效的时间格式") 