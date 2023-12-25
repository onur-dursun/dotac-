import tkinter as tk
from datetime import datetime
import pygame

class AlwaysOnTopText(tk.Tk):
    def __init__(self, text):
        super().__init__()
        self.overrideredirect(True)  # Remove window decorations
        self.attributes('-topmost', True)  # Set window to always on top

        # Make the window transparent
        self.wm_attributes('-transparentcolor', self['bg'])

        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Create a small icon for dragging
        self.drag_icon = tk.Label(top_frame, text="🚀", font=('Arial', 10), cursor="fleur", fg="black", bg="white")
        self.drag_icon.pack(side=tk.RIGHT, pady=5, padx=(10, 5))
        
        # Bind mouse events for dragging
        self.drag_icon.bind("<ButtonPress-1>", self.start_drag)
        self.drag_icon.bind("<B1-Motion>", self.on_drag)

        self.label = tk.Label(self, text=text, font=('Arial', 12), fg="white")
        self.label.pack(padx=10, pady=10)

        self.start_time = datetime.now()

        self.timer_label = tk.Label(self, text="Time: 00:00:00", font=('Arial', 10), fg="white")
        self.timer_label.pack(pady=5)

        close_button = tk.Button(
            self,
            text="Close",
            command=self.destroy,
            bg="red",  # Set background color to red
            fg="white",  # Set text color to white
            activebackground="darkred"  # Set background color when button is clicked
        )
        close_button.pack(pady=10)

        pygame.mixer.init()

        self.update_window_position()
        #self.bind('<Configure>', lambda e: self.update_window_position())
        self.update_timer()
        
        self.alert("aslkdfjşlaskdjf")

    def update_window_position(self):
        width, height = self.winfo_reqwidth(), self.winfo_reqheight()
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f'+{x}+{y}')

    def update_timer(self):
        current_time = datetime.now()
        elapsed_time = current_time - self.start_time
        elapsed_str = str(elapsed_time).split(".")[0]  # Format as HH:MM:SS

        self.timer_label.config(text=f"Time: {elapsed_str}")

         # Update label text every 45th second
        if elapsed_str.split(":")[2] == "02":
            self.alert("Stack zamanı geldi.", "lib/sound/stack_alarm.mp3")

        self.after(1000, self.update_timer) 

    def alert(self, message, alert_sound = ""):
        self.label.config(text=message)

        if not alert_sound:
            return
        pygame.mixer.music.load(alert_sound)
        pygame.mixer.music.play()
    
    def start_drag(self, event):
        self._drag_data = {'x': event.x, 'y': event.y}

    def on_drag(self, event):
            self.drag_icon.config(cursor="fleur")
            x = self.winfo_x() + (event.x - self._drag_data['x'])
            y = self.winfo_y() + (event.y - self._drag_data['y'])
            self.geometry(f'+{x}+{y}')       

def main():
    text_to_display = "Dota akımı başlasın."
    
    app = AlwaysOnTopText(text_to_display)
    app.mainloop()

if __name__ == "__main__":
    main()
