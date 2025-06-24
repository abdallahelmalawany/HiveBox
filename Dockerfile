FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . . 
EXPOSE 80
ENTRYPOINT [ "fastapi" ]
CMD [ "run", "app.py", "--port", "80" ]