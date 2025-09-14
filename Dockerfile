FROM python:3.13.5

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . . 
EXPOSE 8000
ENTRYPOINT [ "fastapi" ]
CMD [ "run", "app.py", "--port", "8000" ]