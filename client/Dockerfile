FROM python:3
COPY . /client
WORKDIR /client
RUN pip install -r requirements.txt
EXPOSE 5678
CMD python ./client.py