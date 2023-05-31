FROM python
WORKDIR /app
ADD . /app
COPY requirements.txt /app
RUN python3 -m pip install -r requirements.txt 
RUN python3 -m nltk.downloader all
EXPOSE 5000
CMD ["python3","app.py"]
