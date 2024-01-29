import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import winsound
import threading
import time

class Alarm:
    def __init__(self, time, tone):
        self.time = time
        self.tone = tone
        self.active = True

class AlarmClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock App")

        self.current_time_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.current_time_label.pack(pady=20)

        self.set_alarm_button = tk.Button(root, text="Set New Alarm", command=self.show_alarm_setting)
        self.set_alarm_button.pack(pady=10)

        self.alarm_listbox = tk.Listbox(root, selectmode=tk.SINGLE, font=("Helvetica", 12))
        self.alarm_listbox.pack(pady=10)

        self.toggle_alarm_button = tk.Button(root, text="Toggle Alarm", command=self.toggle_alarm)
        self.toggle_alarm_button.pack(pady=5)

        self.snooze_button = tk.Button(root, text="Snooze", command=self.snooze_alarm)
        self.snooze_button.pack(pady=5)

        self.dismiss_button = tk.Button(root, text="Dismiss", command=self.dismiss_alarm)
        self.dismiss_button.pack(pady=5)

        # Alarm variables
        self.alarms = []
        self.selected_alarm_index = None

        # Update the current time label
        self.update_time()

        # Start a thread to update the time every second
        self.update_time_thread = threading.Thread(target=self.update_time_thread_function, daemon=True)
        self.update_time_thread.start()

    def update_time_thread_function(self):
        while True:
            time.sleep(1)
            self.update_time()

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.current_time_label.config(text=current_time)

    def show_alarm_setting(self):
        alarm_setting_window = tk.Toplevel(self.root)
        alarm_setting_window.title("Set New Alarm")

        time_label = tk.Label(alarm_setting_window, text="Select Alarm Time:")
        time_label.pack()

        time_picker = ttk.Combobox(alarm_setting_window, values=list(range(24)), state="readonly")
        time_picker.set("00")
        time_picker.pack()

        tone_label = tk.Label(alarm_setting_window, text="Select Alarm Tone:")
        tone_label.pack()

        tone_picker = ttk.Combobox(alarm_setting_window, values=["Tone 1", "Tone 2", "Tone 3"], state="readonly")
        tone_picker.set("Tone 1")
        tone_picker.pack()

        save_button = tk.Button(alarm_setting_window, text="Save Alarm", command=lambda: self.save_alarm(alarm_setting_window, time_picker.get(), tone_picker.get()))
        save_button.pack()

    def save_alarm(self, window, selected_time, selected_tone):
        new_alarm = Alarm(time=int(selected_time), tone=selected_tone)
        self.alarms.append(new_alarm)
        self.update_alarm_listbox()
        window.destroy()

    def update_alarm_listbox(self):
        self.alarm_listbox.delete(0, tk.END)
        for i, alarm in enumerate(self.alarms):
            status = "Active" if alarm.active else "Inactive"
            self.alarm_listbox.insert(tk.END, f"Alarm {i + 1}: {alarm.time:02d}:00 - Tone: {alarm.tone} ({status})")

    def toggle_alarm(self):
        if self.selected_alarm_index is not None:
            alarm = self.alarms[self.selected_alarm_index]
            alarm.active = not alarm.active
            self.update_alarm_listbox()

    def snooze_alarm(self):
        if self.selected_alarm_index is not None:
            alarm = self.alarms[self.selected_alarm_index]
            if alarm.active:
                # Simulate snooze action
                messagebox.showinfo("Snooze", "Alarm snoozed for 5 minutes.")
                winsound.PlaySound(None, winsound.SND_PURGE)

    def dismiss_alarm(self):
        if self.selected_alarm_index is not None:
            alarm = self.alarms[self.selected_alarm_index]
            if alarm.active:
                # Simulate dismiss action
                winsound.PlaySound(None, winsound.SND_PURGE)
                messagebox.showinfo("Dismiss", "Alarm dismissed.")
                self.alarms.pop(self.selected_alarm_index)
                self.update_alarm_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClockApp(root)
    root.mainloop()

