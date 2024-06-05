import os
import asyncio
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from ttkbootstrap import Style
from src.synchronous import synchronous_read_write
from src.asynchronous import async_main
from src.benchmark_sync import benchmark_sync
from src.benchmark_async import benchmark_async


class BufferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Buffering Read/Write")
        self.root.geometry("600x400")

        # Background Image
        script_dir = os.path.dirname(__file__)  # Localização do script atual
        rel_path = "image/background3.jpg"
        abs_file_path = os.path.join(script_dir, rel_path)

        # Verifica se o arquivo existe antes de tentar abrir
        if not os.path.exists(abs_file_path):
            messagebox.showerror(
                "Erro", f"Arquivo de imagem não encontrado: {abs_file_path}"
            )
            return

        self.background_image = Image.open(abs_file_path)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Frame transparente
        style = Style(theme="flatly")
        self.frame = ttk.Frame(root, style="primary.TFrame", padding=10)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Tamanho do Buffer
        self.buffer_size_label = ttk.Label(
            self.frame,
            text="Tamanho do Buffer:",
            background="#000000",
            foreground="#FFFFFF",
        )
        self.buffer_size_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.buffer_size_entry = ttk.Entry(self.frame, style="info.TEntry")
        self.buffer_size_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

        # Botões
        style.configure(
            "Cyan.TButton",
            background="#00FFFF",
            foreground="#000000",
            font=("Helvetica", 10, "bold"),
        )
        self.sync_button = ttk.Button(
            self.frame,
            text="Leitura/Escrita Síncrona",
            command=self.start_sync_read_write,
            style="Cyan.TButton",
        )
        self.sync_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.async_button = ttk.Button(
            self.frame,
            text="Leitura/Escrita Assíncrona",
            command=self.start_async_read_write,
            style="Cyan.TButton",
        )
        self.async_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.benchmark_button = ttk.Button(
            self.frame,
            text="Benchmark",
            command=self.run_benchmark,
            style="Cyan.TButton",
        )
        self.benchmark_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Barra de Progresso
        style.configure(
            "Cyan.Horizontal.TProgressbar", troughcolor="white", background="#00FFFF"
        )
        self.progress = ttk.Progressbar(
            self.frame,
            orient="horizontal",
            length=300,
            mode="determinate",
            style="Cyan.Horizontal.TProgressbar",
        )
        self.progress.grid(row=4, column=0, columnspan=2, pady=(10, 0))

        # Label de Status
        self.status_label = ttk.Label(
            self.frame, text="", background="#000000", foreground="#FFFFFF"
        )
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(0, 5))

        # Bind redimensionamento da janela
        self.root.bind("<Configure>", self.resize_background)

    def resize_background(self, event):
        new_width = event.width
        new_height = event.height
        if new_width > 0 and new_height > 0:
            self.background_image_resized = self.background_image.resize(
                (new_width, new_height), Image.LANCZOS
            )
            self.background_photo_resized = ImageTk.PhotoImage(
                self.background_image_resized
            )
            self.background_label.config(image=self.background_photo_resized)
            self.background_label.image = self.background_photo_resized

    def update_progress(self, current, total):
        self.progress["value"] = (current / total) * 100
        self.root.update_idletasks()

    def start_sync_read_write(self):
        input_files = filedialog.askopenfilenames(
            title="Selecione os Arquivos de Entrada"
        )
        if not input_files:
            messagebox.showerror("Erro", "Arquivos de entrada não selecionados.")
            return

        output_file = filedialog.asksaveasfilename(title="Selecione o Arquivo de Saída")
        if not output_file:
            messagebox.showerror("Erro", "Arquivo de saída não selecionado.")
            return

        buffer_size_str = self.buffer_size_entry.get()
        if not buffer_size_str.isdigit():
            messagebox.showerror(
                "Erro", "O tamanho do buffer deve ser um número inteiro."
            )
            return

        buffer_size = int(buffer_size_str)
        total_size = sum(os.path.getsize(f) for f in input_files)
        self.progress["value"] = 0
        self.update_progress(0, total_size)

        for input_file in input_files:
            try:
                synchronous_read_write(
                    input_file,
                    output_file,
                    buffer_size,
                    self.update_progress,
                    total_size,
                )
            except BufferError as e:
                messagebox.showerror("Erro", str(e))
                return
        self.status_label.config(text="Leitura/Escrita Síncrona Concluída")
        messagebox.showinfo("Sucesso", "Leitura/Escrita Síncrona Concluída")

    def start_async_read_write(self):
        input_file = filedialog.askopenfilename(title="Selecione o Arquivo de Entrada")
        if not input_file:
            messagebox.showerror("Erro", "Arquivo de entrada não selecionado.")
            return

        output_file = filedialog.asksaveasfilename(title="Selecione o Arquivo de Saída")
        if not output_file:
            messagebox.showerror("Erro", "Arquivo de saída não selecionado.")
            return

        buffer_size_str = self.buffer_size_entry.get()
        if not buffer_size_str.isdigit():
            messagebox.showerror(
                "Erro", "O tamanho do buffer deve ser um número inteiro."
            )
            return

        buffer_size = int(buffer_size_str)
        total_size = os.path.getsize(input_file)
        self.progress["value"] = 0
        self.update_progress(0, total_size)

        try:
            asyncio.run(
                async_main(
                    input_file,
                    output_file,
                    buffer_size,
                    self.update_progress,
                    total_size,
                )
            )
        except BufferError as e:
            messagebox.showerror("Erro", str(e))
            return
        self.status_label.config(text="Leitura/Escrita Assíncrona Concluída")
        messagebox.showinfo("Sucesso", "Leitura/Escrita Assíncrona Concluída")

    def run_benchmark(self):
        input_file = filedialog.askopenfilename(
            title="Selecione o Arquivo de Entrada para Benchmark"
        )
        if not input_file:
            messagebox.showerror("Erro", "Arquivo de entrada não selecionado.")
            return

        output_file_sync = filedialog.asksaveasfilename(
            title="Selecione o Arquivo de Saída Síncrona"
        )
        if not output_file_sync:
            messagebox.showerror("Erro", "Arquivo de saída síncrona não selecionado.")
            return

        output_file_async = filedialog.asksaveasfilename(
            title="Selecione o Arquivo de Saída Assíncrona"
        )
        if not output_file_async:
            messagebox.showerror("Erro", "Arquivo de saída assíncrona não selecionado.")
            return

        buffer_size_str = self.buffer_size_entry.get()
        if not buffer_size_str.isdigit():
            messagebox.showerror(
                "Erro", "O tamanho do buffer deve ser um número inteiro."
            )
            return

        buffer_size = int(buffer_size_str)
        sync_time = benchmark_sync(input_file, output_file_sync, buffer_size)
        async_time = benchmark_async(input_file, output_file_async, buffer_size)

        # Registrar os tempos de execução no log
        logger.info(f"Tempo de execução síncrona: {sync_time:.2f} segundos")
        logger.info(f"Tempo de execução assíncrona: {async_time:.2f} segundos")

        messagebox.showinfo(
            "Benchmark", "Benchmark concluído. Verifique os logs para mais detalhes."
        )


def start_app():
    root = tk.Tk()
    style = Style(theme="flatly")
    app = BufferApp(root)
    root.mainloop()


if __name__ == "__main__":
    # Configuração do logger
    logging.basicConfig(
        filename="benchmarking.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger()

    start_app()
