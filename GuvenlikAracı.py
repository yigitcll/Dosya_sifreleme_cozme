import tkinter as tk
from tkinter import filedialog, messagebox
import os
import hashlib
import json

def islem_tetikle(mod):
    dosya = dosya_yolu.get()
    sifre = sifre_alani.get()

    if not dosya or not sifre:
        messagebox.showwarning("Uyari", "Alanlari bos birakmayin!")
        return

    try:
        anahtar = hashlib.sha256(sifre.encode()).digest()
        
        with open(dosya, 'rb') as f:
            veri = f.read()

        cikti = bytearray()
        for i in range(len(veri)):
            cikti.append(veri[i] ^ anahtar[i % len(anahtar)])

        dosya_adi = os.path.basename(dosya)
        ek = "sifreli_" if mod == "sifrele" else "cozulmus_"
        yeni_dosya_adi = ek + dosya_adi
        hedef_yol = os.path.join(os.path.dirname(dosya), yeni_dosya_adi)
        
        with open(hedef_yol, 'wb') as f:
            f.write(cikti)

        log = {
            "islem": mod,
            "dosya": dosya_adi,
            "sonuc": yeni_dosya_adi,
            "boyut": len(veri)
        }

        with open("islem_kaydi.json", "w") as j:
            json.dump(log, j, indent=4)

        messagebox.showinfo("Basarili", f"Islem Tamam: {yeni_dosya_adi}")

    except Exception:
        messagebox.showerror("Hata", "Bir sorun olustu!")

def secici():
    yol = filedialog.askopenfilename()
    if yol:
        dosya_yolu.set(yol)

pencere = tk.Tk()
pencere.title("Ostim Siber Araci")
pencere.geometry("400x350")
pencere.configure(bg='#121212')

dosya_yolu = tk.StringVar()

tk.Label(pencere, text="DOSYA SECIMI", bg='#121212', fg='#00ff00', font=('Consolas', 10)).pack(pady=(20,0))
tk.Entry(pencere, textvariable=dosya_yolu, width=40, bg='#1e1e1e', fg='white', relief='flat').pack(pady=10)
tk.Button(pencere, text="GOZAT", command=secici, bg='#333333', fg='white', relief='flat').pack()

tk.Label(pencere, text="SIFRE (ANAHTAR)", bg='#121212', fg='#00ff00', font=('Consolas', 10)).pack(pady=(20,0))
sifre_alani = tk.Entry(pencere, show="*", width=40, bg='#1e1e1e', fg='white', relief='flat')
sifre_alani.pack(pady=10)

tk.Button(pencere, text="SIFRELE", command=lambda: islem_tetikle("sifrele"), bg='#721c24', fg='white', width=20).pack(pady=10)
tk.Button(pencere, text="COZ", command=lambda: islem_tetikle("coz"), bg='#004085', fg='white', width=20).pack()

pencere.mainloop()