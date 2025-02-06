import tkinter as tk
from tkinter import StringVar, ttk, messagebox
from ttkbootstrap import Style
import csv
import os
from datetime import datetime

# Nome del file CSV
CSV_FILE = "pratiche.csv"


class Applicazione:
    def __init__(self, parent):
        parent.title("Schedulatore Ordini di Vendita")
        parent.geometry("600x450")
        parent.resizable(False, False)

        # Centrare la finestra
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 450) // 2
        parent.geometry(f"+{x}+{y}")

        # Applicare un tema moderno
        style = Style(theme="superhero")

        # Frame principale
        main_frame = ttk.Frame(parent, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Titolo principale
        ttk.Label(main_frame, text='Schedulatore per ordini di vendita:', font=("Arial", 14, "bold")).grid(row=0,
                                                                                                           column=0,
                                                                                                           columnspan=3,
                                                                                                           pady=10)

        # Etichette e campi di input
        ttk.Label(main_frame, text="Numero Pratica:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5,
                                                                               sticky="w")
        self.input1 = StringVar()
        self.nPratica = ttk.Entry(main_frame, textvariable=self.input1, width=30)
        self.nPratica.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(main_frame, text="Settore:", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.settore = ttk.Combobox(main_frame, values=['Aerospace', 'Automotive'], state="readonly", width=27)
        self.settore.set("")
        self.settore.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(main_frame, text="Tipologia:", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.tipologia = ttk.Combobox(main_frame, values=['Laminato', 'Monolitico'], state="readonly", width=27)
        self.tipologia.set("")
        self.tipologia.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(main_frame, text="Note:", font=("Arial", 10)).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.note = tk.Text(main_frame, width=30, height=3)
        self.note.grid(row=4, column=1, padx=5, pady=5)

        # Bottone per calcolare il Lead Time
        self.btn1 = ttk.Button(main_frame, text='Calcola LeadTime', style="primary.TButton", command=self.leadTime)
        self.btn1.grid(row=5, column=1, pady=10, padx=5)

        # Etichetta per mostrare il risultato
        self.lt = ttk.Label(main_frame, text="", font=("Arial", 10, "bold"), foreground="blue")
        self.lt.grid(row=6, column=1, pady=10, padx=5)

        # Bottone per salvare la pratica
        self.btn_save = ttk.Button(main_frame, text='Salva Pratica', style="success.TButton",
                                   command=self.salva_pratica)
        self.btn_save.grid(row=7, column=1, pady=5)

        # Bottone per leggere le pratiche salvate
        self.btn_read = ttk.Button(main_frame, text='Leggi Pratiche Salvate', style="info.TButton",
                                   command=self.leggi_pratiche)
        self.btn_read.grid(row=8, column=1, pady=5)

    def leadTime(self):
        """ Calcola il Lead Time basato sulla tipologia selezionata """
        tipo_selezionato = self.tipologia.get()
        if tipo_selezionato == "Monolitico":
            self.lt.config(text="Lead Time: 8 Wk da evasione schede tecniche", foreground="green")
        elif tipo_selezionato == 'Laminato':
            self.lt.config(text="Lead Time: 10 Wk da evasione schede tecniche", foreground="green")
        else:
            self.lt.config(text="⚠️ Seleziona una tipologia valida!", foreground="red")

    def salva_pratica(self):
        """ Salva la pratica su un file CSV """
        numero_pratica = self.input1.get()
        settore = self.settore.get()
        tipologia = self.tipologia.get()
        note = self.note.get("1.0", tk.END).strip()
        lead_time = self.lt.cget("text").replace("Lead Time: ", "")  # Estrarre solo il lead time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not numero_pratica or not settore or not tipologia or not lead_time:
            messagebox.showerror("Errore", "Compila tutti i campi e calcola il Lead Time!")
            return

        nuova_pratica = [numero_pratica, settore, tipologia, note, lead_time, timestamp]

        # Verifica se il file esiste, altrimenti crea l'intestazione
        file_esiste = os.path.exists(CSV_FILE)
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_esiste:
                writer.writerow(["Numero Pratica", "Settore", "Tipologia", "Note", "Lead Time", "Data/Ora"])
            writer.writerow(nuova_pratica)

        messagebox.showinfo("Successo", f"Pratica {numero_pratica} salvata con successo!")

    def leggi_pratiche(self):
        """ Legge e mostra le pratiche salvate """
        if not os.path.exists(CSV_FILE):
            messagebox.showinfo("Info", "Nessuna pratica salvata.")
            return

        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            dati = list(reader)

        if len(dati) <= 1:
            messagebox.showinfo("Info", "Nessuna pratica registrata nel file.")
            return

        # Creazione di una nuova finestra per visualizzare i dati
        finestra_dati = tk.Toplevel()
        finestra_dati.title("Pratiche Salvate")
        finestra_dati.geometry("700x350")

        text_area = tk.Text(finestra_dati, wrap="word", height=15, width=90)
        text_area.pack(pady=10, padx=10)

        # Inserisce i dati nel Text Widget
        for row in dati:
            text_area.insert(tk.END, "\t".join(row) + "\n")

        text_area.config(state="disabled")  # Rende il testo non modificabile


# Avviare la GUI
root = tk.Tk()
app = Applicazione(root)
root.mainloop()
