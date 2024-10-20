FROM python:latest
RUN apt install -y git
ENV TZ=Europe/Berlin

ADD https://raw.githubusercontent.com/gsnhf/zwiftrunalyze/RestService/requirements.txt requirements.txt
RUN git clone --branch RestService https://github.com/gsnhf/zwiftrunalyze.git
RUN apt-get update && apt-get install -y cmake
RUN pip install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt
WORKDIR /zwiftrunalyze
COPY . .
CMD ["python", "rest.py"]