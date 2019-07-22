FROM python:3

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

ADD ./ ./
RUN pip install ./

ENTRYPOINT ["/usr/local/bin/pfFocus-format"]
CMD ["-q", "-f", "md", "-i", "-", "-o", "-"]
