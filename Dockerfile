FROM python
# RUN useradd cjcon90
WORKDIR /var/www/hot-dogz
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY hot_dogz hot_dogz
COPY run.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py

# RUN chown -R cjcon90:cjcon90 ./
USER root

EXPOSE 5001
ENTRYPOINT ["./boot.sh"]
