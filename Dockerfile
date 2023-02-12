FROM python:3.10-slim-buster

ENV TZ=Asia/Yerevan

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .

ENV DALLE_BOT_TOKEN=$DALLE_BOT_TOKEN
ENV DALLE_KEY=$DALLE_KEY
ENV PYTHONPATH=/code/

CMD ["python", "/code/main.py"]
