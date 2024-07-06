from tkinter import *
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube, Playlist
import os
import threading
import time

#download each single URL
def Downloader(link, root, output_dir, quality,progress_var, completion_callback):     
    url =YouTube(str(link.get()))
    
    video = url.streams.filter(res= quality).first()
    print(f"Video format: {video}")

    if not video:
    	messagebox.showerror("Error",f"No video avaialable for this selected {quality}")
    	root.update_idletasks()
    	return 
    #audio = url.streams.filter(only_audio=True).first()
    #print(f"Audio only : {audio}")
    output_file = video.download(output_path = output_dir)

    Label(root, text = 'The single file download completed', font = 'arial 18', bg = 'black', fg = 'white').place(x= 180 , y = 300)  
    #print(f"output_file format: {output_file}")
    base, ext = os.path.splitext(output_file)

    export_file = base + '.mp3'
    os.rename(output_file,export_file)
    if completion_callback:
        completion_callback(base)

#Download a whole playlist 
def PlaylistDownloader(link, root, output_dir, quality,progress_var, completion_callback):
	playlist = Playlist(str(link.get()))
	total_videos = len(playlist.video_urls)
	if total_videos ==0:
		messagebox.showerror("Error", "The playlist is empty or the link is invalid")
		root.update_idletasks()
		return

	progress_step = 100/total_videos
	current_progress = 0 

	for index, video_url in enumerate(playlist.video_urls, start =1):#playlist.video_urls:
		url =YouTube(video_url)
		video = url.streams.filter(res= quality).first()
		if not video:
			messagebox.showerror("Error",f"No video avaialable for this selected {quality}")
			root.update_idletasks()
			return
		output_file = video.download(output_path = output_dir)
		base, ext = os.path.splitext(output_file)
		export_file = base + '.mp3'
		os.rename(output_file,export_file)
		current_progress =index *progress_step
		progress_var.set(current_progress)
		root.update_idletasks()
	if completion_callback:
		completion_callback("Playlist download completed")

#update the download progressing bar 
def update_progress_bar(progress_var, root, time):
	while progress_var.get() < 100:
		progress_var.set(progress_var.get() + 1)
		root.update_idletasks()
		time.sleep(0.05)

def disable_button(btn, btn_playlist):
	btn.config(state="disabled")
	btn_playlist.config(state="disabled")

def enable_download_button(btn, btn_playlist):
	btn.config(state = "normal")
	btn_playlist.config(state = "normal")

#check it download complete and throw it back to normal
def download_completed(base, btn , btn_playlist,progress_var):
    progress_var.set(100)
    if base =="Playlist download completed":
    	Label(root, text = 'The Playlist download completed', font = 'arial 18', bg = 'black', fg = 'white').place(x= 180 , y = 300)  
    enable_download_button(btn, btn_playlist)

#asking the directory and toss the file in that directory 
def select_location(entry_location):
	select_dir = filedialog.askdirectory()
	if select_dir:
		entry_location.delete(0, END)
		entry_location.insert(0, select_dir)

def main():
	root = Tk()
	root.geometry('800x800')
	root.resizable(0,0)
	root.title("YouTube Dowloader Demo")
	root.configure(bg='black')

	frm = ttk.Frame(root, padding=10)
	frm.grid()
	#ttk.Style().configure("TMenubutton", background = 'black')

	link = StringVar()
	Label(root, text = 'Paste Link Here:', font = 'arial 15 bold', bg = 'black', fg = 'white').place(x= 160 , y = 60)
	link_enter = Entry(root, width = 80,  textvariable = link, bg = 'black', fg = 'white', insertbackground='white').place(x = 32, y = 90)

	location = StringVar()
	Label(root, text = 'Save Your File at:', font = 'arial 15 bold', bg = 'black', fg = 'white').place(x = 160, y = 120)
	entry_location = Entry(root, width = 60, textvariable = location, bg = 'black', fg = 'white', insertbackground='white')
	entry_location.place(x = 32, y = 150)
	btn_location = Button(root, text = 'Browser', command = lambda: select_location(entry_location), bg = 'gray', fg = 'black')
	btn_location.place(x = 500, y = 145)

	quality = StringVar(value = '720p')
	Label(root, text = "Select quality: ", font = 'arial 15 bold', bg = 'black', fg = 'white').place(x = 32, y = 210)
	quality_menu = OptionMenu(root, quality, "360p", "480p", "720p", "1080p")
	quality_menu.config(bg = 'white', fg = 'black')
	menu = root.nametowidget(quality_menu.menuname)
	menu.config(bg = 'black', fg = 'white')
	quality_menu.place(x = 150, y = 210)
	#quality_menu["menu"].configure(bg ='white', fg = 'black')

	progress_var = IntVar()
	progress_bar = ttk.Progressbar(root, variable = progress_var, maximum = 100)
	progress_bar.place(x = 32, y = 250, width = 700)

	def download():
		disable_button(btn, btn_playlist)
		progress_var.set(0)
		#threading.Thread(target = update_progress_bar, args = (progress_var,root,time)).start()
		thread = threading.Thread(target=lambda: Downloader(link, root, location.get(),quality.get(),progress_var, lambda base: download_completed(base, btn, btn_playlist, progress_var))).start()
		#thread.start()

	def download_playlist():
		disable_button(btn, btn_playlist)
		progress_var.set(0)
		#threading.Thread(target = update_progress_bar, args = (progress_var,root,time)).start()
		thread = threading.Thread(target=lambda: PlaylistDownloader(link, root, location.get(),quality.get(),progress_var, lambda base: download_completed(base, btn, btn_playlist, progress_var))).start()
		

	btn = Button(root,text = 'DOWNLOAD', font = 'arial 15 bold' , command=download, bg = 'gray', fg = 'black')
	btn.place(x=180 ,y = 180)

	btn_playlist = Button(root,text = 'DOWNLOAD PLAYLIST', font = 'arial 15 bold' , command=download_playlist, bg = 'gray', fg = 'black')
	btn_playlist.place(x=400 ,y = 180)

	root.mainloop()


if __name__=="__main__":
	main()
