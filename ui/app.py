import os  # Biblioteca para manipulação de arquivos e diretórios
import asyncio  # Biblioteca para programação assíncrona
import logging  # Biblioteca para registro de logs
import tkinter as tk  # Biblioteca para criar interfaces gráficas
from tkinter import filedialog, messagebox, ttk  # Módulos específicos do tkinter
from PIL import Image, ImageTk  # Bibliotecas para manipulação de imagens
from ttkbootstrap import Style  # Biblioteca para temas do tkinter
from src.synchronous import synchronous_read_write  # Função de leitura/escrita síncrona
from src.asynchronous import async_main  # Função principal assíncrona
from src.benchmark_sync import benchmark_sync  # Função de benchmark síncrona
from src.benchmark_async import benchmark_async  # Função de benchmark assíncrona


class BufferApp:
    def __init__(self, root):
        # Inicialização da janela principal do Tkinter
        self.root = root
        self.root.title("Buffering Read/Write")  # Define o título da janela
        self.root.geometry("600x400")  # Define o tamanho da janela

        # Configuração do logger para registrar eventos e resultados de benchmark
        logging.basicConfig(
            filename="benchmarking.log",  # Nome do arquivo de log
            level=logging.INFO,  # Nível de registro do log
            format="%(asctime)s - %(levelname)s - %(message)s",  # Formato das mensagens de log
        )
        self.logger = logging.getLogger()  # Cria o logger

        # Configuração da imagem de fundo
        script_dir = os.path.dirname(__file__)  # Obtém o diretório do script atual
        rel_path = "image/background3.jpg"  # Caminho relativo da imagem de fundo
        abs_file_path = os.path.join(script_dir, rel_path)  # Caminho absoluto da imagem

        # Verifica se o arquivo de imagem existe antes de tentar abri-lo
        if not os.path.exists(abs_file_path):
            messagebox.showerror(
                "Erro", f"Arquivo de imagem não encontrado: {abs_file_path}"
            )
            return

        # Carrega a imagem de fundo
        self.background_image = Image.open(abs_file_path)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(root, image=self.background_photo)
        self.background_label.place(
            relwidth=1, relheight=1
        )  # Define a imagem como fundo

        # Criação de um frame transparente sobre a imagem de fundo
        style = Style(theme="flatly")
        self.frame = ttk.Frame(
            root, style="primary.TFrame", padding=10
        )  # Cria um frame com padding
        self.frame.place(
            relx=0.5, rely=0.5, anchor=tk.CENTER
        )  # Centraliza o frame na janela

        # Label e campo de entrada para o tamanho do buffer
        self.buffer_size_label = ttk.Label(
            self.frame,
            text="Tamanho do Buffer:",
            background="#000000",  # Fundo preto
            foreground="#FFFFFF",  # Texto branco
        )
        self.buffer_size_label.grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )  # Posiciona a label

        self.buffer_size_entry = ttk.Entry(
            self.frame, style="info.TEntry"
        )  # Campo de entrada para o buffer
        self.buffer_size_entry.grid(
            row=0, column=1, padx=5, pady=5, sticky=tk.E
        )  # Posiciona o campo de entrada

        # Configuração dos botões com estilo personalizado
        button_width = 22  # Largura dos botões
        style.configure(
            "Cyan.TButton",
            background="#00FFFF",  # Fundo ciano
            foreground="#000000",  # Texto preto
            font=("Helvetica", 10, "bold"),  # Fonte em negrito
        )

        # Botão para Leitura/Escrita Síncrona
        self.sync_button = ttk.Button(
            self.frame,
            text="Leitura/Escrita Síncrona",
            command=self.start_sync_read_write,  # Chama a função de leitura/escrita síncrona
            style="Cyan.TButton",
            width=button_width,
        )
        self.sync_button.grid(
            row=1, column=0, columnspan=2, pady=10
        )  # Posiciona o botão

        # Botão para Leitura/Escrita Assíncrona
        self.async_button = ttk.Button(
            self.frame,
            text="Leitura/Escrita Assíncrona",
            command=self.start_async_read_write,  # Chama a função de leitura/escrita assíncrona
            style="Cyan.TButton",
            width=button_width,
        )
        self.async_button.grid(
            row=2, column=0, columnspan=2, pady=10
        )  # Posiciona o botão

        # Botão para executar o benchmark
        self.benchmark_button = ttk.Button(
            self.frame,
            text="Benchmark",
            command=self.run_benchmark,  # Chama a função de benchmark
            style="Cyan.TButton",
            width=button_width,
        )
        self.benchmark_button.grid(
            row=3, column=0, columnspan=2, pady=10
        )  # Posiciona o botão

        # Barra de Progresso configurada com estilo personalizado
        style.configure(
            "Cyan.Horizontal.TProgressbar", troughcolor="white", background="#00FFFF"
        )
        self.progress = ttk.Progressbar(
            self.frame,
            orient="horizontal",
            length=300,  # Comprimento da barra de progresso
            mode="determinate",  # Modo de progresso determinado
            style="Cyan.Horizontal.TProgressbar",
        )
        self.progress.grid(
            row=4, column=0, columnspan=2, pady=(10, 0)
        )  # Posiciona a barra de progresso

        # Label de Status para exibir mensagens de status
        self.status_label = ttk.Label(
            self.frame, text="", background="#000000", foreground="#FFFFFF"
        )
        self.status_label.grid(
            row=5, column=0, columnspan=2, pady=(0, 5)
        )  # Posiciona a label de status

        # Vincula o redimensionamento da janela à função de redimensionar a imagem de fundo
        self.root.bind("<Configure>", self.resize_background)

    def resize_background(self, event):
        # Redimensiona a imagem de fundo ao redimensionar a janela
        new_width = event.width  # Nova largura da janela
        new_height = event.height  # Nova altura da janela
        if new_width > 0 and new_height > 0:
            self.background_image_resized = self.background_image.resize(
                (new_width, new_height), Image.LANCZOS  # Redimensiona a imagem
            )
            self.background_photo_resized = ImageTk.PhotoImage(
                self.background_image_resized
            )
            self.background_label.config(
                image=self.background_photo_resized
            )  # Atualiza a imagem de fundo
            self.background_label.image = (
                self.background_photo_resized
            )  # Mantém a referência à imagem

    def update_progress(self, current, total):
        # Atualiza a barra de progresso com o progresso atual
        self.progress["value"] = (
            current / total
        ) * 100  # Calcula a porcentagem do progresso
        self.root.update_idletasks()  # Atualiza a interface gráfica

    def start_sync_read_write(self):
        # Função para iniciar a leitura/escrita síncrona
        input_files = filedialog.askopenfilenames(
            title="Selecione o(s) Arquivo(s) de Entrada"
        )
        if not input_files:
            messagebox.showerror("Erro", "Arquivo(s) de entrada não selecionado(s).")
            return

        output_file = filedialog.asksaveasfilename(
            title="Escreva como deseja salvar o Arquivo de Saída"
        )
        if not output_file:
            messagebox.showerror("Erro", "Arquivo de saída não selecionado.")
            return

        buffer_size_str = self.buffer_size_entry.get()
        if not buffer_size_str.isdigit():
            messagebox.showerror(
                "Erro", "O tamanho do buffer deve ser um número inteiro."
            )
            return

        buffer_size = int(buffer_size_str)  # Converte o tamanho do buffer para inteiro
        total_size = sum(
            os.path.getsize(f) for f in input_files
        )  # Calcula o tamanho total dos arquivos de entrada
        self.progress["value"] = 0  # Reseta a barra de progresso
        self.update_progress(0, total_size)  # Atualiza a barra de progresso

        # Processa cada arquivo de entrada
        for input_file in input_files:
            try:
                # Chama a função de leitura/escrita síncrona
                synchronous_read_write(
                    input_file,
                    output_file,
                    buffer_size,
                    self.update_progress,  # Atualiza a barra de progresso
                    total_size,
                )
            except BufferError as e:
                # Mostra mensagem de erro se ocorrer um BufferError
                messagebox.showerror("Erro", str(e))
                return
        self.status_label.config(
            text="Leitura/Escrita Síncrona Concluída"
        )  # Atualiza a mensagem de status
        messagebox.showinfo(
            "Sucesso", "Leitura/Escrita Síncrona Concluída"
        )  # Mostra mensagem de sucesso

    def start_async_read_write(self):
        # Função para iniciar a leitura/escrita assíncrona
        input_file = filedialog.askopenfilename(
            title="Selecione o(s) Arquivo(s) de Entrada"
        )
        if not input_file:
            messagebox.showerror("Erro", "Arquivo de entrada não selecionado.")
            return

        output_file = filedialog.asksaveasfilename(
            title="Escreva como deseja salvar o Arquivo de Saída"
        )
        if not output_file:
            messagebox.showerror("Erro", "Arquivo de saída não selecionado.")
            return

        buffer_size_str = self.buffer_size_entry.get()
        if not buffer_size_str.isdigit():
            messagebox.showerror(
                "Erro", "O tamanho do buffer deve ser um número inteiro."
            )
            return

        buffer_size = int(buffer_size_str)  # Converte o tamanho do buffer para inteiro
        total_size = os.path.getsize(
            input_file
        )  # Calcula o tamanho do arquivo de entrada
        self.progress["value"] = 0  # Reseta a barra de progresso
        self.update_progress(0, total_size)  # Atualiza a barra de progresso

        # Executa a função assíncrona de leitura/escrita
        try:
            asyncio.run(
                async_main(
                    input_file,
                    output_file,
                    buffer_size,
                    self.update_progress,  # Atualiza a barra de progresso
                    total_size,
                )
            )
        except BufferError as e:
            # Mostra mensagem de erro se ocorrer um BufferError
            messagebox.showerror("Erro", str(e))
            return
        self.status_label.config(
            text="Leitura/Escrita Assíncrona Concluída"
        )  # Atualiza a mensagem de status
        messagebox.showinfo(
            "Sucesso", "Leitura/Escrita Assíncrona Concluída"
        )  # Mostra mensagem de sucesso

    def run_benchmark(self):
        # Função para executar o benchmark
        input_file = filedialog.askopenfilename(
            title="Selecione o Arquivo de Entrada para Benchmark"
        )
        if not input_file:
            messagebox.showerror("Erro", "Arquivo de entrada não selecionado.")
            return

        output_file_sync = filedialog.asksaveasfilename(
            title="Escreva como deseja salvar o Arquivo de Saída Síncrona"
        )
        if not output_file_sync:
            messagebox.showerror("Erro", "Arquivo de saída síncrona não selecionado.")
            return

        output_file_async = filedialog.asksaveasfilename(
            title="Escreva como deseja salvar o Arquivo de Saída Assíncrona"
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

        buffer_size = int(buffer_size_str)  # Converte o tamanho do buffer para inteiro

        # Executa os benchmarks síncronos e assíncronos
        sync_time = benchmark_sync(input_file, output_file_sync, buffer_size)
        async_time = benchmark_async(input_file, output_file_async, buffer_size)

        # Atualiza a barra de progresso ao final do benchmark
        self.progress["value"] = 100
        self.root.update_idletasks()

        # Registra os tempos de execução no log
        self.logger.info(f"Tempo de execução síncrona: {sync_time:.2f} segundos")
        self.logger.info(f"Tempo de execução assíncrona: {async_time:.2f} segundos")

        messagebox.showinfo(
            "Benchmark", "Benchmark concluído. Verifique os logs para mais detalhes."
        )
        self.status_label.config(
            text="Benchmark Concluído"
        )  # Atualiza a mensagem de status


def start_app():
    # Função para iniciar a aplicação Tkinter
    root = tk.Tk()  # Cria a janela principal
    style = Style(theme="flatly")  # Aplica o tema flatly
    app = BufferApp(root)  # Cria a aplicação
    root.mainloop()  # Inicia o loop principal da interface


if __name__ == "__main__":
    # Inicia a aplicação se o script for executado diretamente
    start_app()
