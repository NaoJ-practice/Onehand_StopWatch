import tkinter as tk
import time
from pynput import mouse

class StopWatch(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # フォーマットの設定
        self.title("ワンハンド ストップウォッチ")
        self.geometry("400x400")
        self.configure(bg="#2C3E50")
        
        self.time_label = tk.Label(self, text="00:00:00", font=("Arial", 40), fg="white", bg="#2C3E50")
        self.time_label.pack(pady=10)

        self.lap_listbox = tk.Listbox(self, font=("Arial", 12), bg="#34495E", fg="white", width=40, height=10)
        self.lap_listbox.pack(pady=10)

        # 初期値
        self.lap_times = []
        self.is_running = False
        self.start_time = None
        self.last_lap_time = None
        self.reset_flag = False
        self.lap_num = 0
        self.update_time()

        # マウスリスナーの設定
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll)
        self.mouse_listener.start()
    
    # 時間表示部分(hoursは使うことないが一応追加)
    def update_time(self):
        if self.is_running:
            current_time = time.time() - self.start_time
            hours, remainder = divmod(current_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_label.config(text=f"{hours:02.0f}:{minutes:02.0f}:{seconds:03.3f}")
        self.after(100, self.update_time)  # 0.001秒後にupdate_timeメソッドが呼び出される

    # スタート・ストップ機能
    def start_stop_toggle(self):
        if not self.is_running:
            self.start_time = time.time() - (self.last_lap_time or 0)  # self.last_lap_timeがFALSEなら0
            self.is_running = True
            self.reset_flag = False
        else:
            self.is_running = False
            self.last_lap_time = time.time() - self.start_time
    
    # ラップ取得部分
    def record_lap(self, event=None):
        if self.is_running:
            self.lap_num += 1
            lap_time = time.time() - self.start_time
            hours, remainder = divmod(lap_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            lap_text = f"Lap{self.lap_num} {hours:02.0f}:{minutes:02.0f}:{seconds:03.3f}"
            self.lap_times.append(lap_text)
            self.lap_listbox.insert(tk.END, lap_text)
    
    # リセット機能
    def reset_stopwatch(self):
        self.is_running = False
        self.start_time = None
        self.last_lap_time = None
        self.time_label.config(text="00:00:00")
        self.lap_listbox.delete(0, tk.END)
        self.lap_times.clear()
        self.lap_num = 0
        self.reset_flag = True

    # マウスの画面外の反応を検知する機能
    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == mouse.Button.left:
                self.start_stop_toggle()
            elif button == mouse.Button.right:
                self.record_lap()

    def on_scroll(self, x, y, dx, dy):
        if not self.is_running and dy < 0:  # マウスホイールを下にスクロールしたらリセット
            self.reset_stopwatch()

if __name__ == "__main__":
    app = StopWatch()
    app.mainloop()
