FROM python:3.11.3

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV NLTK_DATA=/usr/local/share/nltk_data
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt

COPY . /code/seoninja

WORKDIR /code/seoninja

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]