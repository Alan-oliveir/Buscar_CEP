import tkinter as tk
import customtkinter as ctk

from PIL import Image, ImageTk

import os

import requests

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

PATH = os.path.dirname(os.path.realpath(__file__))

class App(ctk.CTk):

    APP_NAME = "Buscar CEP"
    WIDTH = 500
    HEIGHT = 650

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(App.WIDTH, App.HEIGHT)
        self.maxsize(App.WIDTH, App.HEIGHT)
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # load image with PIL and convert to PhotoImage
        image = Image.open(PATH + "/test_images/bg_gradient.jpg").resize((self.WIDTH, self.HEIGHT))
        self.bg_image = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(master=self, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.frame = ctk.CTkFrame(master=self, width=300, height=App.HEIGHT, corner_radius=0)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label = ctk.CTkLabel(master=self.frame, width=200, height=30,corner_radius=6, fg_color=("gray70", "gray25"), text="BUSCA DE CEP")
        self.label.place(relx=0.5, rely=0.08, anchor=tk.CENTER)

        self.option_uf = ctk.CTkOptionMenu(master=self.frame, corner_radius=6, width=200, values=["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", 
                                                                                                            "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
                                                                                                            "SP", "SE", "TO"])
        self.option_uf.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.entry_cidade = ctk.CTkEntry(master=self.frame, corner_radius=6, width=200, placeholder_text="Cidade")
        self.entry_cidade.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        
        self.entry_endereco = ctk.CTkEntry(master=self.frame, corner_radius=6, width=200, placeholder_text="Rua")
        self.entry_endereco.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.button_submit = ctk.CTkButton(master=self.frame, text="Enviar", corner_radius=6, command=self.button_event_submit, width=200)
        self.button_submit.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.button_clean = ctk.CTkButton(master=self.frame, text="Clean", corner_radius=6, command=self.button_event_clean, width=200)
        self.button_clean.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        self.label_count_cep = ctk.CTkLabel(master=self.frame, width=250, corner_radius=6, fg_color=("gray70", "gray25"), text = "Número de CEPs encontrados: ")
        self.label_count_cep.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.textbox = ctk.CTkTextbox(master=self.frame, width=250, height=200, corner_radius=6)
        self.textbox.place(relx=0.5, rely=0.78, anchor=tk.CENTER)

    def button_event_submit(self):
                
        uf = self.option_uf.get()
        cidade = self.entry_cidade.get()        
        endereco = self.entry_endereco.get()              

        link = f'https://viacep.com.br/ws/{uf}/{cidade}/{endereco}/json/'

        requisicao = requests.get(link)

        # Verifica erro na requisição do CEP
        if requisicao.status_code != 200:
            self.message_window = ctk.CTkToplevel(self)
            self.message_window.title('Erro de Requisição')
            self.message_window.after(10000, self.message_window.destroy)

            # create label on CTkToplevel window
            label = ctk.CTkLabel(self.message_window, text="Ocorreu um erro na requisição do CEP.\nVerifique o endereço e tente novamente.")
            label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

        dic_requisicao = requisicao.json()        
               
        count =(len(dic_requisicao))
        
        self.label_count_cep.configure(text=f"Número de CEPs encontrados: {count}")

        # Exibe o endereço e primeiro CEP encontrado na caixa de texto
        self.textbox.insert("0.0", f" UF: {uf}\n Cidade: {cidade}\n Bairro: {dic_requisicao[0]['bairro']}\n Logradouro: {endereco}\n CEP: {dic_requisicao[0]['cep']}\n")

    def button_event_clean(self):
        
        self.entry_cidade.delete(0, 'end')
        self.entry_endereco.delete(0, 'end')
        self.textbox.delete("0.0", 'end')
        self.label_count_cep.configure(text="Número de CEPs encontrados: ")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()