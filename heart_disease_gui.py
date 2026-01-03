import tkinter as tk
from tkinter import messagebox
import re, pickle

model = pickle.load(open("heart_model.pkl","rb"))

def extract_nlp():
    text = symptom.get().lower()

    age.delete(0,'end')
    chol.delete(0,'end')
    sugar.delete(0,'end')
    sex.delete(0,'end')

    a = re.search(r'(\d+)\s*year', text)
    c = re.search(r'cholesterol\s*(\d+)', text)

    if a: age.insert(0, a.group(1))
    if c: chol.insert(0, c.group(1))
    sex.insert(0, 1 if "male" in text else 0)
    sugar.insert(0, 1 if "high sugar" in text else 0)

def predict():
    data = [[
        int(age.get()), int(sex.get()), int(cp.get()),
        int(bp.get()), int(chol.get()), int(sugar.get()),
        int(ecg.get()), int(hr.get()), int(angina.get()),
        float(oldpeak.get()), int(slope.get()),
        int(vessels.get()), int(thal.get())
    ]]

    prob = model.predict_proba(data)[0][1]*100
    result = model.predict(data)[0]

    if result == 1:
        messagebox.showwarning("Prediction Result",
                               f"HIGH RISK OF HEART DISEASE\nConfidence: {prob:.2f}%")
    else:
        messagebox.showinfo("Prediction Result",
                            f"LOW RISK\nConfidence: {100-prob:.2f}%")

root = tk.Tk()
root.title("Heart Disease Prediction System")
root.geometry("900x520")

tk.Label(root,text="Heart Disease Prediction System",
         bg="brown",fg="white",
         font=("Arial",16,"bold")).pack(fill="x")

frame1=tk.Frame(root); frame1.pack(pady=8)
tk.Label(frame1,text="NLP Symptom Input").pack(anchor="w")
symptom=tk.Entry(frame1,width=90)
symptom.pack()
tk.Button(frame1,text="Extract Features (NLP)",command=extract_nlp).pack(anchor="e")

frame2=tk.Frame(root); frame2.pack()

def field(text,r,c):
    tk.Label(frame2,text=text).grid(row=r,column=c)
    e=tk.Entry(frame2,width=10)
    e.grid(row=r,column=c+1)
    return e

age=field("Age",0,0); sex=field("Sex",0,2)
cp=field("Chest Pain",1,0); bp=field("BP",1,2)
chol=field("Cholesterol",2,0); sugar=field("Sugar",2,2)
ecg=field("ECG",3,0); hr=field("Max HR",3,2)
angina=field("Angina",4,0); oldpeak=field("Oldpeak",4,2)
slope=field("Slope",5,0); vessels=field("Vessels",5,2)
thal=field("Thal",6,0)

tk.Button(root,text="PREDICT RISK",
          bg="green",fg="white",
          font=("Arial",14,"bold"),
          command=predict).pack(fill="x",pady=15)

root.mainloop()
