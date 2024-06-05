# Buffering Read/Write Project

## Introdução
Este projeto implementa operações de leitura e escrita de arquivos usando buffers, tanto de forma síncrona quanto assíncrona. O objetivo é demonstrar as diferenças entre operações síncronas e assíncronas e como elas podem ser usadas para gerenciar a leitura e escrita de dados de forma eficiente.

### O que é Síncrono?
**Operações Síncronas**: Em uma operação síncrona, as tarefas são executadas uma após a outra. Cada operação deve ser concluída antes que a próxima comece. Em termos de leitura e escrita de arquivos, isso significa que o programa lê um bloco de dados do arquivo de entrada, escreve esse bloco no arquivo de saída e só então prossegue para o próximo bloco.

### O que é Assíncrono?
**Operações Assíncronas**: Em uma operação assíncrona, as tarefas podem ser executadas simultaneamente. Isso permite que o programa inicie uma nova operação antes que a anterior tenha sido concluída, usando a capacidade de multitarefa do sistema operacional. Para leitura e escrita de arquivos, isso significa que o programa pode ler dados de um arquivo enquanto ainda está escrevendo dados lidos anteriormente em outro.

### Diferenças entre Síncrono e Assíncrono

#### Execução:
- **Síncrono**: Bloqueia a execução até que a operação atual seja concluída.
- **Assíncrono**: Permite a execução de outras operações enquanto aguarda a conclusão da operação atual.

#### Desempenho:
- **Síncrono**: Pode ser mais lento, pois cada operação deve esperar a anterior terminar.
- **Assíncrono**: Pode ser mais rápido, pois utiliza melhor os recursos do sistema, permitindo que múltiplas operações ocorram simultaneamente.

#### Uso de Recursos:
- **Síncrono**: Utiliza recursos de forma linear.
- **Assíncrono**: Utiliza recursos de forma paralela, permitindo um uso mais eficiente da CPU e outros recursos.

## Estrutura do Projeto

### Diretório `src`
- `__init__.py`: Arquivo de inicialização do pacote.
- `buffer.py`: Define duas classes de buffer, uma para operações síncronas (Buffer) e outra para operações assíncronas (AsyncBuffer).
- `synchronous.py`: Define a função de leitura e escrita síncrona.
- `asynchronous.py`: Define as funções de leitura e escrita assíncronas.
- `sync_benchmark.py`: Define a função de benchmark para operações síncronas.
- `async_benchmark.py`: Define a função de benchmark para operações assíncronas.
- `main.py`: Arquivo principal para execução do projeto.

### Diretório `ui`
- `__init__.py`: Arquivo de inicialização do pacote.
- `app.py`: Define a interface gráfica usando Tkinter e as funções para iniciar operações síncronas e assíncronas, além do benchmark.

### Diretório `resources`
- `new_input.txt`: Arquivo de exemplo usado como entrada para as operações de leitura/escrita.

### Arquivo `requirements.txt`
Lista as dependências necessárias para executar o projeto.

## Executando o Projeto

### Passo 1: Configuração Inicial
Instale as dependências necessárias (se houver):

```sh
pip install -r requirements.txt
```
### Passo 2: Navegue até o diretório do projeto no terminal
```sh
cd Downloads/Buffer_Project
```
### Passo 3: Configure o PYTHONPATH (se necessário)
```sh
export PYTHONPATH=$PYTHONPATH:Downloads/Buffer_project
```
### Passo 4: Execute a aplicação
```sh
python3 src/main.py
```

## Interface Gráfica

### Campo de Tamanho do Buffer

No campo ao lado do rótulo "Tamanho do Buffer:", digite um número inteiro, por exemplo, 10.

### Operações Síncronas

1. Clique no botão "Leitura/Escrita Síncrona".
2. Selecione `new_input.txt` ou outro arquivo do estilo .txt como arquivo de entrada.
3. Dê um nome ao arquivo de saída, por exemplo, `output_sync_new.txt`.
4. Verifique a mensagem de sucesso: "Leitura/Escrita Síncrona Concluída".

### Operações Assíncronas

1. Clique no botão "Leitura/Escrita Assíncrona".
2. Selecione `new_input.txt` ou outro arquivo do estilo .txt como arquivo de entrada.
3. Dê um nome ao arquivo de saída, por exemplo, `output_async_new.txt`.
4. Verifique a mensagem de sucesso: "Leitura/Escrita Assíncrona Concluída".

## Benchmark

### Executando o Benchmark

1. Clique no botão "Benchmark".
2. Selecione `new_input.txt` como arquivo de entrada.
3. Dê um nome ao arquivo de saída síncrona, por exemplo, `output_sync_benchmark.txt`.
4. Dê um nome ao arquivo de saída assíncrona, por exemplo, `output_async_benchmark.txt`.
5. Verifique os resultados no terminal e no arquivo `benchmark.log`.

## Explicação do Fluxo

### Leitura e Escrita Síncrona

A função `synchronous_read_write` lê dados do arquivo de entrada em blocos do tamanho especificado e escreve no arquivo de saída. Utiliza um buffer para armazenar temporariamente os dados lidos antes de escrevê-los. Mensagens de depuração mostram o processo de leitura e escrita.

### Leitura e Escrita Assíncrona

A função `async_main` coordena as funções `async_read` e `async_write`. `async_read` lê dados do arquivo de entrada em blocos do tamanho especificado e os coloca no buffer de forma assíncrona. `async_write` escreve dados do buffer no arquivo de saída de forma assíncrona. Mensagens de depuração mostram o processo de leitura e escrita.

### Benchmark Síncrono e Assíncrono

Os arquivos `sync_benchmark.py` e `async_benchmark.py` implementam as funções de benchmark para as operações síncronas e assíncronas, respectivamente. Eles medem o tempo de execução e registram os resultados no arquivo `benchmark.log`.

## Verificação do Conteúdo

Verifique se o conteúdo dos arquivos de saída (`output_sync_new.txt` e `output_async_new.txt`) é idêntico ao do arquivo de entrada (`new_input.txt`). As mensagens de depuração no terminal devem diferenciar claramente entre operações síncronas e assíncronas, mostrando o fluxo de dados.

## Finalização

Este projeto demonstra claramente as diferenças entre operações de leitura e escrita síncronas e assíncronas, usando buffers para gerenciar a eficiência do processamento de dados. A interface gráfica intuitiva, construída com Tkinter, facilita a seleção de arquivos e a definição do tamanho do buffer, tornando o processo acessível e compreensível.

Agradecemos por utilizar este projeto como parte do seu aprendizado e desenvolvimento. Esperamos que ele tenha sido útil para entender melhor as operações síncronas e assíncronas e como elas podem ser aplicadas de maneira eficaz em diferentes contextos de programação.

Certifique-se de ajustar os caminhos de diretórios e os nomes de arquivos conforme necessário para corresponder à estrutura real do seu projeto.




