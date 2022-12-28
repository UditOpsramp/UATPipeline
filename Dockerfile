FROM ubuntu:latest

RUN apt-get update 
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y golang 

WORKDIR /home/LogsAutomation

COPY . /home/LogsAutomation

RUN pip3 install -r requirements.txt

CMD ["python3","-u" , "LogsValidation.py"]
