class DragMixin:
    def __init__(self, widget):
        self.widget = widget
        self._is_dragging = False
        self._drag_data = None
        
        # 绑定拖拽事件
        self.widget.bind('<B1-Motion>', self.drag_window)
        self.widget.bind('<ButtonPress-1>', self.start_drag)
        self.widget.bind('<ButtonRelease-1>', self.stop_drag)

    def start_drag(self, event):
        """开始拖动"""
        self._drag_data = {'x': event.x, 'y': event.y}

    def drag_window(self, event):
        """处理拖动"""
        if not self._drag_data:
            return
            
        deltax = event.x - self._drag_data['x']
        deltay = event.y - self._drag_data['y']
        
        if abs(deltax) < 3 and abs(deltay) < 3:
            return
            
        x = self.widget.master.winfo_x() + deltax
        y = self.widget.master.winfo_y() + deltay
        self.widget.master.geometry(f'+{x}+{y}')
        self._is_dragging = True

    def stop_drag(self, event):
        """停止拖动"""
        self._is_dragging = False
        self._drag_data = None 