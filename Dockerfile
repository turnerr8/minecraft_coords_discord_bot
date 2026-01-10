#small stable python
FROM python:3.11-slim

#prevent .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

#set wd
WORKDIR /app

#install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy app source
COPY . .

#create data dir for sqlite
RUN mkdir -p data

# run bot
CMD ["python", "index.py"]