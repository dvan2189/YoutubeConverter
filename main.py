from tkinter import *
from tkinter import ttk
from pytube import YouTube
import os
import threading



def Downloader(link,root,completion_callback):     
    url =YouTube(str(link.get()))
    video = url.streams.first()
    output_file = video.download()

    Label(root, text = 'The job done', font = 'arial 15').place(x= 180 , y = 210)  
    base, ext = os.path.splitext(output_file)
    export_file = base + '.mp3'
    os.rename(output_file,export_file)
    if completion_callback:
        completion_callback(base)

def download_completed(base,btn):
    print(f"Download completed for: {base}")
    btn.config(state="normal") 

def main():
	root = Tk()
	root.geometry('800x800')
	root.resizable(0,0)
	root.title("Try me out")

	frm = ttk.Frame(root, padding=10)
	frm.grid()
	link = StringVar()
	Label(root, text = 'Paste Link Here:', font = 'arial 15 bold').place(x= 160 , y = 60)
	link_enter = Entry(root, width = 80,  textvariable = link).place(x = 32, y = 90)

	def download():
		btn.config(state="disabled")
		thread = threading.Thread(target=lambda: Downloader(link, root, lambda base: download_completed(base, btn)))
		thread.start()

	btn = Button(root,text = 'DOWNLOAD', font = 'arial 15 bold' , command=download, bg = 'pale violet red', padx = 2)
	btn.place(x=180 ,y = 150)

	root.mainloop()


if __name__=="__main__":
	main()