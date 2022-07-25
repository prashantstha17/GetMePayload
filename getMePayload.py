from tkinter import *
from tkinter import ttk, messagebox
from customtkinter import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import wget
import os
from tkinterhtml import HtmlFrame


app = CTk()
app.set_appearance_mode("system")
app.geometry("1100x880")
app.title("GetMePayload | Author: @PrashantShrestha")
app.resizable(False, False)

app.iconbitmap(r'@assets/baseIcon.xbm')



wrapper1 = LabelFrame(app)
wrapper1.grid(row=0, column=0, padx=10, pady=10)


mycanvas = CTkCanvas(wrapper1, width=220, height=860)
mycanvas.grid(row=0, column=0, padx=10, pady=10)

yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=mycanvas.yview)
yscrollbar.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

mycanvas.configure(yscrollcommand=yscrollbar.set)
mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion = mycanvas.bbox('all')))

myframe = CTkFrame(mycanvas, width=250, height=860)
mycanvas.create_window((0, 0), window=myframe, anchor="nw")



try:
    if os.path.exists("source/homepage.html"):
        with open("source/homepage.html", "r") as f:
            html = f.read()
            # print(html)
            soup = BeautifulSoup(html, "html.parser")
   
    else:
        url =  "https://github.com/swisskyrepo/PayloadsAllTheThings"
        r = requests.get(url)
        os.makedirs('source', exist_ok=True)
        soup = BeautifulSoup(r.content, 'html.parser')
        # print(soup)
        with open('source/homepage.html', 'w', encoding='utf-8') as f_out:
            f_out.write(str(soup))
except:
    print("[-] Error: Could not connect to github")
    print('[-] Error: Requires internet connection for the first time.')
    exit()



ancs = soup.find_all('a')

filters = []
for i in range(len(ancs)):

    if '/swisskyrepo/PayloadsAllTheThings/tree/master/' in ancs[i].get('href'):
            filters.append(ancs[i])

dic = {}
for i in range(len(filters)):
    dic[filters[i].text] = f"https://raw.githubusercontent.com{unquote(filters[i].get('href'))}"

dic.pop('.github')

# print(dic)

for key in dic:
    k = key
    key = key.replace(' ','_')
    globals () ['button_%s' % key] = CTkButton(myframe, 
                                                text=k, 
                                                command=lambda j=key:getPayload(j),
                                                width=190, 
                                                height=40,
                                                hover_color="orange",
                                                text_font=("Times", "10", "bold"))
    dynamic_button = eval(['button_%s' % key][0])
    dynamic_button.grid(pady=10)


wrapper2 = CTkFrame(app)
wrapper2.grid(row=0, column=1, padx=10, pady=10)



mycanvas2 = CTkCanvas(wrapper2, width=735, height=650)
mycanvas2.grid(row=0, column=0)

yscrollbar2 = ttk.Scrollbar(wrapper2, orient="vertical", command=mycanvas2.yview)
yscrollbar2.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

mycanvas2.configure(yscrollcommand=yscrollbar2.set)
mycanvas2.bind('<Configure>', lambda e: mycanvas2.configure(scrollregion = mycanvas2.bbox('all')))



myframe2 = CTkFrame(mycanvas2)
mycanvas2.create_window((0, 0), window=myframe2, anchor="nw")


def download():
    for i in dic:
        # download_progress.set(value)
        url = dic[i].replace('/tree','')
        title = dic[i].split('/')[-1]
        title = title.replace(' ', '_')
        filepath = f'source/{title}_README.md'
        try:
            # print(f"{url}/README.md")
            if not os.path.exists(filepath):
                wget.download(f"{url}/README.md", out=filepath)
        except:
            try:
                if not os.path.exists(filepath):
                    wget.download(f"{url}/readme.md", out=filepath)
            except:
                print(dynamic_button)
                dynamic_button.destroy()

    message = messagebox.showinfo("Download Status", "Download/Check Complete")   

download_button = CTkButton(myframe2, 
                            text='Download/Check Files', 
                            command=download,
                            width=300, 
                            height=150,
                            hover_color="lightgreen",
                            text_font=("Times", "12", "bold"))
download_button.grid(row=1, column=0, pady=100, padx=100, sticky="nesw")

info_label = CTkLabel(myframe2, 
                    text=f"Info: You only need to click this button once until the download completes.\n Next time you can get payload offline!",
                    text_font=("Times", "12", "bold"),
                    fg_color="lightgreen")
info_label.grid(row=5, column=0, pady=100, padx=100, sticky="nesw")



def getPayload(value):
    md2HtmlFile = value.replace(" ", "_")

    try:
        if not os.path.exists(f"source/{md2HtmlFile}_README.md"):
            message = messagebox.showerror("Error", "Download the file first!")

        elif not os.path.exists(f"source/{md2HtmlFile}.html"):
            download_button.destroy() # clears the download/check button
            info_label.destroy() # clears the info label
            os.system(f'md2html source/{md2HtmlFile}_README.md > source/{md2HtmlFile}.html')
            with open(f'source/{md2HtmlFile}.html') as f:
                frame = HtmlFrame(myframe2, horizontal_scrollbar="true", vertical_scrollbar="true",fontscale=1)
                x = f.read()
                frame.set_content(x)
                frame.grid(row=0, column=1, padx=10, pady=10)
        else:
            download_button.destroy() # clears the download/check button
            info_label.destroy() # clears the info label
            with open(f'source/{md2HtmlFile}.html') as f:
                frame = HtmlFrame(myframe2, horizontal_scrollbar="true", vertical_scrollbar="true", fontscale=1)
                x = f.read()
                frame.set_content(x)
                frame.grid(row=0, column=1, padx=10, pady=10)
    except:
        pass



app.mainloop()