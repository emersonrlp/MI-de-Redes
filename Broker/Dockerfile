# Use a imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos necessários para o contêiner
COPY broker.py .
COPY requirements.txt .
COPY api.py .

# Instale as dependências (se aplicável)
RUN pip install --no-cache-dir -r requirements.txt

# Defina o comando de inicialização
CMD ["python", "broker.py"]