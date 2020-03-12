FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN mkdir app/staticfiles
RUN mkdir app/mediafiles
WORKDIR /app
ADD requirements.txt /app/
ADD .env /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /app/