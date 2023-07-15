import re
import pandas as pd
import numpy as np
import speech_recognition as sr
import csv
dataset=pd.read_csv("C:\\Users\\Manikanta.Chanda\\Downloads\\finaldata1.csv")
dataset = dataset.replace(np.nan, 'NA', regex=True)
dataset=dataset.dropna()
rest_id=list(dataset['restaurant_id'])
review_text=list(dataset["review_text"]);review_clean=[];cr=[];review ="";reviews_text = list()

for i in review_text:
    for j in i:
        j=str(j)
        if(re.search(r'[a-z]',j) or re.search(r'[A-Z]',j) or re.search(r'[0-9]',j) or re.search(r'\s',j) or re.search(r'\'',j) or re.search(r'.',j) or re.search(r'\!',j)):
            review+=j
    review_clean.append(review)
    review=""

for i in review_clean:
    res=re.findall(r'n\'t',i)
    i = i.replace("n\'t",' not')
    cr.append(i)
review_clean=cr
restaurant_name=list(dataset["name"]);restaurant_name_clean=[];review="";
restaurant_names = list()
for i in restaurant_name:
    for j in i:
        j=str(j)
        if(re.search(r'[a-z]',j) or re.search(r'[A-Z]',j) or re.search(r'[0-9]',j) or re.search(r'\s',j) or re.search(r'\'',j) or re.search(r'.',j) or re.search(r'\!',j)):
            if(re.search(r'[a-z]',j) or re.search(r'[A-Z]',j)):
                j=j.lower()
            review+=j
    restaurant_name_clean.append(review)
    review=""
review_title=list(dataset["title"]);title_clean=[];title=""
for i in review_title:
    for j in i:
        j=str(j)
        if(re.search(r'[a-z]',j) or re.search(r'[A-Z]',j) or re.search(r'[0-9]',j) or re.search(r'\s',j) or re.search(r'\'',j) or re.search(r'.',j) or re.search(r'\!',j)):
            title+=j
    title_clean.append(title)
    title=""
rest_id_dict={}
for i in range(len(rest_id)):
    rest_id_dict[rest_id[i]]=restaurant_name_clean[i]
rest_index_dict={}
for i in range(len(restaurant_name_clean)):
    if restaurant_name_clean[i] in rest_index_dict:
        rest_index_dict[restaurant_name_clean[i]].append(i)
    else:
        rest_index_dict[restaurant_name_clean[i]]=[i]
positive_words =['perfect','great','good','tasty','friendly','spectacular','awesome','delicious','yummy','best','soothing','juicy']
negative_words = ['bad','tastless','sad','mild','foul']
positive_words_syns = []
negative_words_syns = []

from nltk.corpus import wordnet
for word in positive_words: 
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            positive_words_syns.append(l.name())
positive_words_syns = list(set(positive_words_syns))

for word in negative_words: 
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            negative_words_syns.append(l.name())
negative_words_syns = list(set(negative_words_syns))
food_in_restaurants={}
cuisines=["French", "Indian", "Italian", "Spanish", "Mexican", "English","Dutch", "European", "Chinese"]
cuisines_lower=["french", "indian", "italian", "spanish", "mexican","english", "dutch", "european", "chinese"]
restaurant_index=[];

for cuisine in cuisines_lower:
    for review in review_clean:
        temp=str(review).lower()
        if(re.search(cuisine.lower(),temp)):
            restaurant_index.append(review_clean.index(review))
    food_in_restaurants[cuisine]=restaurant_index
    restaurant_index=[]

def classifyReviewsOf(indexes):
    indexWiseScore = {}
    positive_reviews = []
    negative_reviews = []
    insufficient_data_to_classify = []
    for index in indexes:
        score = calcScore(review_clean[index])
        indexWiseScore[index] = score;
        if(score>0):
            positive_reviews.append(review_clean[index])
        elif(score<-0):
            negative_reviews.append(review_clean[index])
        else:
            insufficient_data_to_classify.append(review_clean[index]) 
    return positive_reviews,negative_reviews,insufficient_data_to_classify,indexWiseScore
def calcScore(review):
    score = 0
    for word in review.split():
        if(word in positive_words_syns):
            score+=1
        elif(word in negative_words_syns):
            score-=1
    return score

def recommendRestaurantForACuisine(indexWiseScore):
    popular_restaurants = sorted(indexWiseScore, key=lambda x: (-indexWiseScore[x], x))
    most_popular_rest = []
    for index in popular_restaurants:
        if restaurant_name_clean[index] not in most_popular_rest:
            most_popular_rest.append(restaurant_name_clean[index])
    return most_popular_rest
 
positive_reviews=[]
negative_reviews=[]
insufficient_data_to_classify=[]

from tkinter import Button, PhotoImage, Entry, Label, E, W, N, Toplevel,Canvas, Tk, NORMAL, END, messagebox, INSERT, DISABLED, IntVar, Radiobutton,Text
from tkinter import ttk
root = Tk()
root.title("Home Page")
root.geometry("600x549")
root.resizable(False, False)
C = Canvas(root, bg="blue", height=549, width=600)
filename = PhotoImage(file = "C:\\Users\\Manikanta.Chanda\\Desktop\\bg1.png")
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def rest_review():
    def main_action():
        flag=True
        res_id=ip.get().lower()
        if(res_id.isdigit()):
            res_id=int(res_id)
        if(param.get()==1):
            if(res_id not in list(rest_id_dict.keys())):    
                flag=False
            else:
                name=rest_id_dict[res_id]
        else:
            if(res_id not in rest_id_dict.values()):
                flag=False
            else:
                name=res_id
        if(flag):
            label6.config(state=NORMAL)
            label7.config(state=NORMAL)
            label8.config(state=NORMAL)
            label6.delete('1.0', END)
            label7.delete('1.0', END)
            label8.delete('1.0', END)
            positive_reviews, negative_reviews,insufficient_data_to_classify,indexWiseScore =classifyReviewsOf(rest_index_dict[name])
            positive=len(positive_reviews)
            negative=len(negative_reviews)
            neutral=len(insufficient_data_to_classify)
            total=positive+negative+neutral
            positive_percentage=(positive*100)//total
            negative_percentage=(negative*100)//total
            neutral_percentage=(neutral*100)//total
            label6.insert(INSERT,str(positive_percentage)+"%")
            label7.insert(INSERT,str(neutral_percentage)+"%")
            label8.insert(INSERT,str(negative_percentage)+"%")
            label6.config(state=DISABLED)
            label7.config(state=DISABLED)
            label8.config(state=DISABLED)
        else:
            messagebox.showinfo("Error", "Invalid Restaurant. No such restaurant found.")
    def radio():
        if(param.get()==1):
            label2.config(text="Enter ID:")
        else:
            label2.config(text="Enter Name:")
    newwin = Toplevel(root)
    newwin.resizable(False, False)
    newwin.title("Restaurant Review")
    newwin.geometry("600x549")
    newwin.grid_columnconfigure(0, weight=1, uniform="fred")
    newwin.grid_columnconfigure(1, weight=1, uniform="fred")
    C = Canvas(newwin, bg="blue", height=549, width=600)
    filename = PhotoImage(file = "C:\\Users\\Manikanta.Chanda\\Desktop\\bg1.png")
    background_label = Label(newwin, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    param=IntVar()
    label1=Label(newwin,text="Search by:",bg='#ffae93')
    label1.grid(column=0,row=0,pady=(120,0))
    rb1=Radiobutton(newwin,text="Restauant ID",bg='#ffae93',padx =10,variable=param,value=1,command=radio)
    rb1.grid(column=1,row=0,pady=(120,0),sticky=W)
    rb2=Radiobutton(newwin,text="Restauant Name",bg='#ffae93',padx =10,variable=param,value=2,command=radio)
    rb2.grid(column=1,row=1,sticky=W)
    rb1.select()
    rb2.deselect()  
    label2=Label(newwin,text="Enter ID:",bg='#ffae93')
    label2.grid(column=0,row=2,pady=(10,10))
    ip=Entry(newwin,width=20)
    ip.grid(column=1,row=2,pady=(10,10),sticky=W)
    button1 =Button(newwin, text ="View Ratings", command =main_action)
    button1.grid(columnspan=2,row=3,pady=(5,0))
    up=PhotoImage(file="C:\\Users\\Manikanta.Chanda\\Desktop\\thumpsup.png")
    down=PhotoImage(file="C:\\Users\\Manikanta.Chanda\\Desktop\\thumpsneutral.png")
    nuetral=PhotoImage(file="C:\\Users\\Manikanta.Chanda\\Desktop\\thumpsdo.png")
    label3=Label(newwin,image=up)
    label3.grid(column=0,row=4,pady=2,sticky=E,padx=30)
    label4=Label(newwin,image=nuetral)
    label4.grid(column=0,row=5,pady=2,sticky=E,padx=30)
    label5=Label(newwin,image=down)
    label5.grid(column=0,row=6,pady=2,padx=30,sticky=E)
    label6=Text(newwin,font=("Helvetica", 24),fg="green",width=5,height=1)
    label6.grid(column=1,row=4,pady=2,sticky=W)
    label7=Text(newwin,font=("Helvetica", 24),fg="red",width=5,height=1)
    label7.grid(column=1,row=5,pady=2,sticky=W)
    label8=Text(newwin,font=("Helvetica", 24),fg="yellow",width=5,height=1)
    label8.grid(column=1,row=6,pady=2,sticky=W)
    label6.config(state=DISABLED)
    label7.config(state=DISABLED)
    label8.config(state=DISABLED)
    C.grid()
    newwin.mainloop()
 
def rest_cuisine():
    def main_action():
        name=cb.get().lower()
        if(name.lower() not in cuisines_lower):
            messagebox.showinfo("Error", "The selected Cuisine is not available.")
        else:
            text.delete('1.0', END)
            positive_reviews, negative_reviews,insufficient_data_to_classify,indexWiseScore =classifyReviewsOf(food_in_restaurants[name])
            most_popular_restaurant =recommendRestaurantForACuisine(indexWiseScore)
            text.insert(INSERT,'The Top '+name+' restaurants are:\n\n')
            if(len(most_popular_restaurant)<10):
                for i in range(len(most_popular_restaurant)):
                    resname=most_popular_restaurant[i].upper()
                    text.insert(INSERT,str(i+1)+'. '+ resname+'\n')
            else:
                for i in range(10):
                    resname=most_popular_restaurant[i].upper()
                    text.insert(INSERT,str(i+1)+'. '+ resname+'\n')
    newwin = Toplevel(root)
    newwin.resizable(False, False)
    newwin.grid_columnconfigure(0, weight=1, uniform="fred")
    newwin.grid_columnconfigure(1, weight=1, uniform="fred")
    newwin.title("Restaurant Cusines")
    newwin.geometry("600x549")
    C = Canvas(newwin, bg="blue", height=389, width=310)
    filename = PhotoImage(file = "C:\\Users\\Manikanta.Chanda\\Desktop\\bg2.png")
    background_label = Label(newwin, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    l1=Label(newwin,text="Choose Your Cuisine:",bg='#ffae93')
    l1.grid(column=0, row=2,sticky=E,pady=50)
    cb=ttk.Combobox(newwin,values=cuisines,width=10)
    cb.grid(column=1, row=2,sticky=W,pady=50,padx=(20,0))
    cb.current(0)
    button1 =Button(newwin, text ="View Top Restaurants", command=main_action)
    button1.grid(columnspan=2,row=3,sticky=N)
    text = Text(newwin, width=40)
    text.grid(columnspan=2,row=4,pady=(10,10),padx=(10,10))
    C.grid()
    newwin.mainloop()
def rest_submit():
    def record_voice():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source,timeout=5,phrase_time_limit=10)
        try:
            text.insert(INSERT,r.recognize_google(audio))
        except sr.UnknownValueError:
            messagebox.showinfo("Error", "Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            messagebox.showinfo("Error", "Could not request results from Google Speech Recognition service; {0}".format(e))
 
    def main_action():
        restaurant_id=ip1.get().lower()        
        if(restaurant_id.isdigit()):
            restaurant_id=int(restaurant_id)
        if(restaurant_id not in rest_id_dict.keys()):
            messagebox.showinfo("Error", "Invalid Restaurant ID")
        else:
            restaurant_name=rest_id_dict[restaurant_id]
            get_title=ip2.get()
            get_review=text.get("1.0",END)
            with open(r"C:\\Users\\Manikanta.Chanda\\Downloads\\samplexl2.csv", 'a', newline='') as csvfile:
                fieldnames = ['restaurant_id','name','title','review_text']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'restaurant_id':restaurant_id,'name':restaurant_name,'title':get_title,'review_text':get_review})
    newwin = Toplevel(root)
    newwin.resizable(False, False)
    newwin.title("Submit a Review")
    newwin.geometry("600x549")
    newwin.grid_columnconfigure(0, weight=1, uniform="fred")
    newwin.grid_columnconfigure(1, weight=1, uniform="fred")
    C = Canvas(newwin, bg="blue", height=549, width=600)
    filename = PhotoImage(file = "C:\\Users\\Manikanta.Chanda\\Desktop\\bg1.png")
    background_label = Label(newwin, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    label1=Label(newwin,text="Enter Restaurant ID:",bg='#ffae93')
    label1.grid(column=0,row=0,pady=(120,10))
    ip1=Entry(newwin,width=20)
    ip1.grid(column=1,row=0,pady=(120,10),sticky=W)
    label2=Label(newwin,text="Enter Review Title:",bg='#ffae93')
    label2.grid(column=0,row=1,pady=(0,10))
    ip2=Entry(newwin,width=20)
    ip2.grid(column=1,row=1,pady=(0,10),sticky=W)
    text=Text(newwin,width=40,height=8)
    text.grid(columnspan=2,row=2,padx=(10,10),pady=(0,10))
    mic_on=PhotoImage(file="C:\\Users\\Manikanta.Chanda\\Desktop\\mic.png")
    record=Button(newwin,text="Record Voice",command=record_voice,image=mic_on)
    record.grid(column=0,row=3,pady=(0,10),padx=30,sticky=E)
    button=Button(newwin,text="Submit Review",command=main_action)
    button.grid(column=1,row=3,pady=(0,10),padx=5,sticky=W)
    C.grid()
    newwin.mainloop()
op1=PhotoImage(file="C:\\Users\\Manikanta.Chanda\\Desktop\\ratings.png")
root.grid_columnconfigure(0, weight=1,uniform="fred")
root.grid_columnconfigure(1, weight=1,uniform="fred")
button1 =Button(root, text ="View Reviews",image=op1, command =rest_review)
button1.grid(column=0,row=8,padx=(50,0),sticky=E,pady=(300,0))
op2=PhotoImage(file="C:\\Users\\Manikanta.Chanda\\Desktop\\review image.png")
button2 =Button(root, text ="Top Cuisine Restarants",image=op2, command=rest_cuisine)
button2.grid(column=1,row=8,padx=(50,0),sticky=W,pady=(300,0))
op3=PhotoImage(file="C:\\Users\\Manikanta.Chanda\\Desktop\\penbook.png")
button2 =Button(root, text ="Submit feedback",image=op3, command=rest_submit)
button2.grid(column=4,row=8,padx=(50,50),sticky=N,pady=(300,0))
C.grid()
root.mainloop()
