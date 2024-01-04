FROM python
RUN useradd cjcon90
WORKDIR /var/www/hot-dogz

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY hot_dogz hot_dogz
COPY run.py config.py ./

ENV FLASK_APP run.py

RUN chown -R cjcon90:cjcon90 ./
USER root

EXPOSE 5001
CMD ["gunicorn", "-b", ":5001", "--access-logfile", "-", "--error-logfile", "-", "run:app"]
