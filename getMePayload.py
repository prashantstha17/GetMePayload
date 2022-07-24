from tkinter import *
from tkinter import ttk, messagebox
from customtkinter import *
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import unquote
import wget
from markdown2 import Markdown
from tkinterhtml import HtmlFrame


app = CTk()
app.title("GET Me A Payload")
app.set_appearance_mode("dark")
app.geometry("1000x880")


wrapper1 = LabelFrame(app)
wrapper1.grid(row=0, column=0, padx=10, pady=10)
# wrapper1.pack(side="left", fill="both", padx=10, pady=10)


mycanvas = CTkCanvas(wrapper1, width=200, height=860)
mycanvas.grid(row=0, column=0, padx=10, pady=10)
# mycanvas.pack(side="left", fill="both", expand=True)

yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=mycanvas.yview)
yscrollbar.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
# yscrollbar.pack(side=RIGHT, fill=Y)

mycanvas.configure(yscrollcommand=yscrollbar.set)
mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion = mycanvas.bbox('all')))

myframe = CTkFrame(mycanvas, width=250, height=860)
mycanvas.create_window((0, 0), window=myframe, anchor="nw")



url =  "https://github.com/swisskyrepo/PayloadsAllTheThings"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# create a directory name source with OS
os.makedirs('source', exist_ok=True)

with open('source/homepage.html', 'w', encoding='utf-8') as f_out:
    f_out.write(soup.prettify())

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

for i in dic:
    k = i
    i = i.replace(' ','_')
    globals () ['button_%s' % i] = CTkButton(myframe, text=k, command=lambda j=i:getPayload(j))
    dynamic_button = eval(['button_%s' % i][0])
    dynamic_button.grid(pady=10)
    # button = CTkButton(myframe, text=i, command=lambda j=i:getPayload(j))
    # button.grid(pady=10)

wrapper2 = CTkFrame(app)
wrapper2.grid(row=0, column=1, padx=10, pady=10)
# wrapper2.pack(fill="both", side=RIGHT, padx=10, pady=10)


mycanvas2 = CTkCanvas(wrapper2, width=640, height=850)
mycanvas2.grid(row=0, column=0, padx=10, pady=10)
# mycanvas2.pack(side=LEFT, fill=BOTH, expand=True)

yscrollbar2 = ttk.Scrollbar(wrapper2, orient="vertical", command=mycanvas2.yview)
yscrollbar2.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
# yscrollbar2.pack(side=RIGHT, fill=Y)

mycanvas2.configure(yscrollcommand=yscrollbar2.set)
mycanvas2.bind('<Configure>', lambda e: mycanvas2.configure(scrollregion = mycanvas2.bbox('all')))



myframe2 = CTkFrame(mycanvas2, height=850)
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
                pass
                print(dynamic_button)
                dynamic_button.destroy()
                
    message = messagebox.showinfo("Download Status", "Download/Check Complete")   
download_button = CTkButton(myframe2, text='Download/Check Files', command=download)
download_button.grid(row=1, column=0, pady=100, padx=100, sticky="nesw")



def getPayload(value):
    download_button.destroy()
    md2HtmlFile = value.replace(" ", "_")
    print(md2HtmlFile)
    try:
        if not os.path.exists(f"source/{md2HtmlFile}.html"):
            os.system(f'md2html source/{md2HtmlFile}_README.md > source/{md2HtmlFile}.html')
            with open(f'source/{md2HtmlFile}.html') as f:
                frame = HtmlFrame(myframe2, horizontal_scrollbar="true", vertical_scrollbar="true")
                x = f.read()
                frame.set_content(x)
                frame.grid(row=0, column=1, padx=10, pady=10)
        else:
            with open(f'source/{md2HtmlFile}.html') as f:
                frame = HtmlFrame(myframe2, horizontal_scrollbar="true", vertical_scrollbar="true")
                x = f.read()
                frame.set_content(x)
                frame.grid(row=0, column=1, padx=10, pady=10)
    except:
        pass



app.mainloop()