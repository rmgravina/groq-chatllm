FROM python:3.9-slim


RUN apt-get update && apt-get install -y bash nano


WORKDIR /app


COPY . .


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


EXPOSE 8501

CMD ["streamlit", "run", "--server.port", "8501", "app.py"]
