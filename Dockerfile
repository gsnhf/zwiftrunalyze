FROM python:latest
RUN apt install -y git
ENV TZ=Europe/Berlin

ADD https://raw.githubusercontent.com/gsnhf/zwiftrunalyze/main/requirements.txt requirements.txt
RUN git clone --branch main https://github.com/gsnhf/zwiftrunalyze.git
RUN apt-get update && apt-get install -y cmake
RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /zwiftrunalyze
EXPOSE 5000
COPY . .
CMD ["python", "rest.py"]