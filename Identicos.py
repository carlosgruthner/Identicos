import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import sys

# Determina o diretório base
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

icone_path = os.path.join(base_path, "file.ico")

# Configuração da interface gráfica
window = ctk.CTk()
window.title("Identicos")
window.geometry("400x300")
window.iconbitmap(icone_path)

# Função para selecionar uma pasta
def select_folder(prompt, label):
    folder = filedialog.askdirectory(title=prompt)
    if folder:
        label.set(folder)

# Função para sincronizar as pastas
def synchronize_folders(source, destination, progress, status):
    total_files = sum(len(files) for _, _, files in os.walk(source))  # Conta total de arquivos
    copied_files = 0
    
    for root, dirs, files in os.walk(source):
        rel_path = os.path.relpath(root, source)
        dest_path = os.path.join(destination, rel_path)
        
        # Cria a pasta de destino se não existir
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            status.set(f"Criada pasta: {dest_path}")
        
        # Copia os arquivos
        for file in files:
            source_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            shutil.copy2(source_file, dest_file)  # Copia o arquivo
            copied_files += 1
            progress.set(copied_files / total_files)  # Atualiza a barra de progresso
            status.set(f"Copiado: {file}")
            window.update_idletasks()  # Atualiza a interface
    
    status.set("Cópia concluída!")
    messagebox.showinfo("Sucesso", "Cópia concluída com sucesso.")

# Função para iniciar a sincronização em um thread separado
def start_sync(source, destination, progress, status):
    if not source or not destination:
        messagebox.showerror("Erro", "Selecione ambas as pastas de origem e destino.")
        return
    progress.set(0)  # Reseta a barra de progresso
    status.set("Iniciando cópia...")
    thread = threading.Thread(target=synchronize_folders, args=(source, destination, progress, status))
    thread.start()




# Variáveis para armazenar os caminhos das pastas
source_folder = ctk.StringVar()
destination_folder = ctk.StringVar()

programa_label = ctk.CTkLabel(window, text="Sincronizador de Pastas", font=("Arial", 16, "bold")).pack(pady=10)

# Botão e rótulo para pasta de origem
ctk.CTkButton(window, text="Selecionar Origem", command=lambda: select_folder("Selecione a pasta de origem", source_folder)).pack(pady=10)
ctk.CTkLabel(window, textvariable=source_folder).pack()

# Botão e rótulo para pasta de destino
ctk.CTkButton(window, text="Selecionar Destino", command=lambda: select_folder("Selecione a pasta de destino", destination_folder)).pack(pady=10)
ctk.CTkLabel(window, textvariable=destination_folder).pack()

# Botão para iniciar a cópia
ctk.CTkButton(window, text="Sincronizar", command=lambda: start_sync(source_folder.get(), destination_folder.get(), progress_var, status_var)).pack(pady=10)

# Barra de progresso
progress_var = ctk.DoubleVar()
progress_bar = ctk.CTkProgressBar(window, variable=progress_var)
progress_bar.pack(pady=10)

# Mensagem de status
status_var = ctk.StringVar()
status_label = ctk.CTkLabel(window, textvariable=status_var)
status_label.pack(pady=10)

# Inicia o loop principal da interface
window.mainloop()