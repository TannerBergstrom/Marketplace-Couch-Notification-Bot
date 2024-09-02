import tkinter as tk
import threading
import time
from scraper import main as scraper_main  # Import the main function from scraper.py

# Global variables
running = False
interval_seconds = 300  # Default interval set to 5 minutes (300 seconds)
total_links_sent = 0  # Counter for total links sent

def start_scraper():
    global running, interval_seconds, total_links_sent, email, username, password
    if not running:
        try:
            interval_minutes = int(interval_entry.get())
        except ValueError:
            interval_minutes = 5  # Default to 5 minutes if invalid input
        try:
            email = email_entry.get()
        except ValueError:
            email = ''
        try:
            username = username_entry.get()
        except ValueError:
            username = ''
        try:
            password = password_entry.get()
        except ValueError:
            password = ''

        interval_seconds = interval_minutes * 60  # Convert minutes to seconds
        running = True
        stop_button.config(state="normal")  # Enable the Stop button
        start_button.config(state="disabled")  # Disable the Start button
        status_label.config(text="Running")
        threading.Thread(target=run_scraper_loop).start()
        threading.Thread(target=update_countdown).start()

def run_scraper_loop():
    global running, interval_seconds, total_links_sent
    while running:
        start_time = time.time()  # Record the start time
        sent_count = scraper_main(email, username, password)  # Call the main function and get the count of links sent
        if sent_count is None:
            sent_count = 0  # Ensure that we handle NoneType safely
        total_links_sent += sent_count  # Update the counter
        counter_label.config(text=f"Total Links Sent: {total_links_sent}")  # Update the label
        counter_label.update_idletasks()  # Ensure the counter updates immediately

        # Wait until the next interval, accounting for the time taken by the scraper
        elapsed_time = time.time() - start_time
        sleep_time = max(0, interval_seconds - elapsed_time)
        for _ in range(int(sleep_time)):
            if not running:
                break
            time.sleep(1)

def update_countdown():
    global interval_seconds, running
    while running:
        for remaining in range(interval_seconds, 0, -1):
            if not running:
                break
            minutes, seconds = divmod(remaining, 60)
            countdown_label.config(text=f"Next run in: {minutes:02}:{seconds:02}")
            countdown_label.update_idletasks()
            time.sleep(1)
        if running:
            countdown_label.config(text="Running...")

def stop_scraper():
    global running
    if running:
        running = False
        stop_button.config(state="disabled")  # Disable the Stop button
        start_button.config(state="normal")  # Enable the Start button
        status_label.config(text="Stopped")  # Update the status
        countdown_label.config(text="Next run in: 00:00")  # Reset the countdown

def animate_status():
    while running:
        for dots in ["Running", "Running.", "Running..", "Running..."]:
            if not running:
                break
            status_label.config(text=dots)
            status_label.update()
            time.sleep(0.5)  # Adjust the speed of the animation here

# Set up the GUI
root = tk.Tk()
root.title("Facebook Couch Web Scraper Control")

# Increase the window size
root.geometry("400x500")

# Interval input label and entry
interval_label = tk.Label(root, text="Interval (minutes):", font=('Helvetica', 12))
interval_label.pack(pady=5)

interval_entry = tk.Entry(root, width=10, font=('Helvetica', 12))
interval_entry.pack(pady=5)
interval_entry.insert(0, "5")  # Default value

email_label = tk.Label(root, text="Email:", font=('Helvetica', 12))
email_label.pack(pady=5)

email_entry = tk.Entry(root, width=30, font=('Helvetica', 12))
email_entry.pack(pady=5)
email_entry.insert(0, "tcbaby04@gmail.com")  # Default value

username_entry = tk.Entry(root, width=30, font=('Helvetica', 12))
username_entry.pack(pady=5)
username_entry.insert(0, "Kyleaburtt@gmail.com")  # Default value

password_entry = tk.Entry(root, width=30, font=('Helvetica', 12))
password_entry.pack(pady=5)
password_entry.insert(0, "KyleTanner2024ChatBot")  # Default value

# Countdown label to display the time until the next run
countdown_label = tk.Label(root, text="Next run in: 00:00", font=('Helvetica', 12))
countdown_label.pack(pady=5)

# Start button
start_button = tk.Button(root, text="Start Scraper", command=start_scraper, width=25, height=3, font=('Helvetica', 12))
start_button.pack(pady=10)

# Stop button (Initially disabled)
stop_button = tk.Button(root, text="Stop Scraper", command=stop_scraper, width=25, height=3, font=('Helvetica', 12))
stop_button.config(state="disabled")  # Disable the button initially
stop_button.pack(pady=10)

# Status label to display running status
status_label = tk.Label(root, text="Stopped", font=('Helvetica', 14))
status_label.pack(pady=20)

# Counter label to display the total number of links sent
counter_label = tk.Label(root, text="Total Links Sent: 0", font=('Helvetica', 14))
counter_label.pack(pady=20)

# Run the GUI loop
root.mainloop()
