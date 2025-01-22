from tkinter import ttk

class BaseTab(ttk.Frame):
    def __init__(self, notebook):
        super().__init__(notebook)
        self.create_widgets()
    
    def create_widgets(self):
        """创建控件"""
        raise NotImplementedError 