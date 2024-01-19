FROM python:latest
RUN apt install -y git
ENV TZ=Europe/Berlin

ADD https://raw.githubusercontent.com/gsnhf/zwiftrunalyze/main/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install protobuf==3.20.*
RUN git clone --branch dev https://github.com/gsnhf/zwiftrunalyze.git
WORKDIR /zwiftrunalyze
CMD sleep infinity