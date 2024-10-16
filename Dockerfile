FROM python:latest
RUN apt install -y git
ENV TZ=Europe/Berlin

ADD https://raw.githubusercontent.com/gsnhf/zwiftrunalyze/main/requirements.txt requirements.txt
RUN git clone --branch main https://github.com/gsnhf/zwiftrunalyze.git
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install protobuf==3.20.*
WORKDIR /zwiftrunalyze
CMD sleep infinity
