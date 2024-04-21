import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pytube import YouTube
import moviepy.editor as mp
import os
import threading

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    completion = int((bytes_downloaded / total_size) * 100)
    progress_bar['value'] = completion
    progress_label.config(text=f"{completion}%")
    root.update_idletasks()

def download_video(youtube_link, output_path, progress_bar, progress_label):
    try:
        yt = YouTube(youtube_link, on_progress_callback=progress_function)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=output_path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        messagebox.showinfo("Success", "Downloaded and converted video to MP3 successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def start_download_thread(youtube_link, output_path, progress_bar, progress_label):
    download_thread = threading.Thread(target=download_video, args=(youtube_link, output_path, progress_bar, progress_label))
    download_thread.start()

def update_output_directory():
    output_entry.delete(0, tk.END)
    output_entry.insert(0, filedialog.askdirectory())


root = tk.Tk()
root.title("YouTube to MP3 Converter")

button_fg = "white"     # Text color
button_font = ("Helvetica", 12, "bold")
button_borderwidth = 1
button_relief = "flat"

style = ttk.Style(root)
style.theme_use('default')
style.configure("TProgressbar", thickness=20, troughcolor='grey', background='green')


url_label = tk.Label(root, text="Enter YouTube URL:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10, padx=10)


output_label = tk.Label(root, text="Select Output Directory:")
output_label.pack()
output_entry = tk.Entry(root, width=50)
output_entry.pack()


output_button = tk.Button(root, text="Browse", bg="#64FF33", fg="black",
                          font=("Helvetica", 10), borderwidth=2, relief="groove",
                          command=update_output_directory)
output_button.pack(pady=10, padx=10)


progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.pack()


progress_label = tk.Label(root, text="0%", font=('Helvetica', 10))
progress_label.pack()


button_bg = "#007bff"  
button_fg = "white"    
button_font = ("Helvetica", 12, "bold")
button_borderwidth = 1
button_relief = "flat"  

download_button = tk.Button(root, text="Download", bg=button_bg, fg=button_fg, font=button_font,
                            borderwidth=button_borderwidth, relief=button_relief,
                            command=lambda: start_download_thread(url_entry.get(), output_entry.get(), progress_bar, progress_label))
download_button.pack(pady=10, padx=10 ,)


root.mainloop()
