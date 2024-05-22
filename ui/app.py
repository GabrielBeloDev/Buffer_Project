import tkinter as tk
from tkinter import filedialog, messagebox
from src.synchronous import synchronous_read_write
from src.asynchronous import async_main
import asyncio


def start_sync_read_write():
    input_file = filedialog.askopenfilename(title="Selecione o Arquivo de Entrada")
    if not input_file:
        messagebox.showerror("Erro", "Arquivo de entrada não selecionado.")
        return

    output_file = filedialog.asksaveasfilename(title="Selecione o Arquivo de Saída")
    if not output_file:
        messagebox.showerror("Erro", "Arquivo de saída não selecionado.")
        return

    buffer_size_str = buffer_size_entry.get()
    if not buffer_size_str.isdigit():
        messagebox.showerror("Erro", "O tamanho do buffer deve ser um número inteiro.")
        return

    buffer_size = int(buffer_size_str)
    synchronous_read_write(input_file, output_file, buffer_size)
    messagebox.showinfo("Sucesso", "Leitura/Escrita Síncrona Concluída")


def start_async_read_write():
    input_file = filedialog.askopenfilename(title="Selecione o Arquivo de Entrada")
    if not input_file:
        messagebox.showerror("Erro", "Arquivo de entrada não selecionado.")
        return

    output_file = filedialog.asksaveasfilename(title="Selecione o Arquivo de Saída")
    if not output_file:
        messagebox.showerror("Erro", "Arquivo de saída não selecionado.")
        return

    buffer_size_str = buffer_size_entry.get()
    if not buffer_size_str.isdigit():
        messagebox.showerror("Erro", "O tamanho do buffer deve ser um número inteiro.")
        return

    buffer_size = int(buffer_size_str)
    asyncio.run(async_main(input_file, output_file, buffer_size))
    messagebox.showinfo("Sucesso", "Leitura/Escrita Assíncrona Concluída")


def start_app():
    # Configuração da GUI
    root = tk.Tk()
    root.title("Buffering Read/Write")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    buffer_size_label = tk.Label(frame, text="Tamanho do Buffer:")
    buffer_size_label.grid(row=0, column=0, padx=5, pady=5)
    global buffer_size_entry
    buffer_size_entry = tk.Entry(frame)
    buffer_size_entry.grid(row=0, column=1, padx=5, pady=5)

    sync_button = tk.Button(
        frame, text="Leitura/Escrita Síncrona", command=start_sync_read_write
    )
    sync_button.grid(row=1, column=0, columnspan=2, pady=10)

    async_button = tk.Button(
        frame, text="Leitura/Escrita Assíncrona", command=start_async_read_write
    )
    async_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()
