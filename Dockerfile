FROM python:latest
RUN apt install -y git
ENV TZ=Europe/Berlin

ADD https://raw.githubusercontent.com/gsnhf/zwiftrunalyze/RestService/requirements.txt requirements.txt
RUN git clone --branch RestService https://github.com/gsnhf/zwiftrunalyze.git
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /zwiftrunalyze
COPY . .
CMD ["python", "rest.py"]