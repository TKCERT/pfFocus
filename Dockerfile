FROM python:3-alpine

COPY ./ /app
WORKDIR /app

RUN pip install -r /app/requirements.txt
RUN pip install /app

ENTRYPOINT ["/usr/local/bin/pfFocus-format"]
CMD ["-q", "-f", "md", "-i", "-", "-o", "-"]
