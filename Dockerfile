FROM python:3.5

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY *.py ./
CMD ./format.py -q -f md -i - -o -
