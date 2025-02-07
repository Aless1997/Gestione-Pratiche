import tkinter as tk
from tkinter import StringVar, ttk, messagebox
from ttkbootstrap import Style
import csv
import os
from datetime import datetime

CSV_FILE = "pratiche.csv"

class Applicazione:
    def __init__(self, parent):
        parent.title("Schedulatore Ordini di Vendita")
        parent.geometry("900x900")
        parent.resizable(False, False)

        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 500) // 2
        parent.geometry(f"+{x}+{y}")

        style = Style(theme="superhero")

        # Frame principale con bordo
        main_frame = ttk.Frame(parent, padding=15, borderwidth=2, relief="ridge")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Titolo con bordo
        title_frame = ttk.LabelFrame(main_frame, text="Schedulatore per ordini", padding=10)
        title_frame.pack(fill="x", pady=10)

        ttk.Label(title_frame, text="Schedulatore per ordini di vendita", font=("Arial", 14, "bold")).pack()

        # Frame per i campi di input con bordo
        input_frame = ttk.LabelFrame(main_frame, text="Dati Pratica", padding=10)
        input_frame.pack(fill="x", pady=10)

        ttk.Label(input_frame, text="Numero Pratica:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.input1 = StringVar()
        self.nPratica = ttk.Entry(input_frame, textvariable=self.input1, width=30)
        self.nPratica.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Settore:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.settore = ttk.Combobox(input_frame, values=['Aerospace', 'Automotive'], state="readonly", width=27)
        self.settore.set("")
        self.settore.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Tipologia:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.tipologia = ttk.Combobox(input_frame, values=['Laminato', 'Monolitico'], state="readonly", width=27)
        self.tipologia.set("")
        self.tipologia.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Note:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.note = tk.Text(input_frame, width=30, height=3, borderwidth=2, relief="groove")
        self.note.grid(row=3, column=1, padx=5, pady=5)

        # Frame per il Lead Time con bordo
        leadtime_frame = ttk.LabelFrame(main_frame, text="Lead Time", padding=10)
        leadtime_frame.pack(fill="x", pady=10)

        self.btn1 = ttk.Button(leadtime_frame, text='Calcola LeadTime', style="primary.TButton", command=self.leadTime)
        self.btn1.pack(pady=5)

        self.lt = ttk.Label(leadtime_frame, text="", font=("Arial", 10, "bold"), foreground="blue")
        self.lt.pack(pady=5)

        # Frame per i bottoni con bordo
        button_frame = ttk.Frame(main_frame, borderwidth=2, relief="ridge", padding=10)
        button_frame.pack(fill="x", pady=10)

        self.btn_save = ttk.Button(button_frame, text='Salva Pratica', style="success.TButton", command=self.salva_pratica)
        self.btn_save.pack(side="left", padx=5)

        self.btn_read = ttk.Button(button_frame, text='Leggi Pratiche Salvate', style="info.TButton", command=self.leggi_pratiche)
        self.btn_read.pack(side="right", padx=5)

    def leadTime(self):
        tipo_selezionato = self.tipologia.get()
        if tipo_selezionato == "Monolitico":
            self.lt.config(text="Lead Time: 8 Wk da evasione schede tecniche", foreground="green")
        elif tipo_selezionato == 'Laminato':
            self.lt.config(text="Lead Time: 10 Wk da evasione schede tecniche", foreground="green")
        else:
            self.lt.config(text="⚠️ Seleziona una tipologia valida!", foreground="red")

    def salva_pratica(self):
        numero_pratica = self.input1.get()
        settore = self.settore.get()
        tipologia = self.tipologia.get()
        note = self.note.get("1.0", tk.END).strip()
        lead_time = self.lt.cget("text").replace("Lead Time: ", "")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not numero_pratica or not settore or not tipologia or not lead_time:
            messagebox.showerror("Errore", "Compila tutti i campi e calcola il Lead Time!")
            return

        nuova_pratica = [numero_pratica, settore, tipologia, note, lead_time, timestamp]

        file_esiste = os.path.exists(CSV_FILE)
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_esiste:
                writer.writerow(["Numero Pratica", "Settore", "Tipologia", "Note", "Lead Time", "Data/Ora"])
            writer.writerow(nuova_pratica)

        messagebox.showinfo("Successo", f"Pratica {numero_pratica} salvata con successo!")

    def leggi_pratiche(self):
        if not os.path.exists(CSV_FILE):
            messagebox.showinfo("Info", "Nessuna pratica salvata.")
            return

        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            dati = list(reader)

        if len(dati) <= 1:
            messagebox.showinfo("Info", "Nessuna pratica registrata nel file.")
            return

        finestra_dati = tk.Toplevel()
        finestra_dati.title("Pratiche Salvate")
        finestra_dati.geometry("700x350")

        text_area = tk.Text(finestra_dati, wrap="word", height=15, width=90, borderwidth=2, relief="ridge")
        text_area.pack(pady=10, padx=10)

        for row in dati:
            text_area.insert(tk.END, "\t".join(row) + "\n")

        text_area.config(state="disabled")

root = tk.Tk()
app = Applicazione(root)
root.mainloop()
