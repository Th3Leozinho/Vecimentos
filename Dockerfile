# Dockerfile para o projeto aviso_vencimentos.py
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Instala dependências, se existir requirements.txt
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Comando para rodar o script principal
CMD ["python", "aviso_vencimentos.py"]
