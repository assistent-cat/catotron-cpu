FROM python:3.7.9-slim-buster

RUN set -x \
    && apt-get update \
    && apt-get -y install --no-install-recommends wget \
    && apt-get -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./requirements-server.txt /srv/requirements.txt

RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r /srv/requirements.txt

COPY ./demo_server.py /srv/demo_server.py
COPY ./server.py /srv/server.py
COPY ./synthesizer.py /srv/synthesizer.py
COPY ./hparam.py /srv/hparam.py
COPY ./hparams_synth.py /srv/hparams_synth.py
COPY ./model.py /srv/model.py
COPY ./utils_tts.py /srv/utils_tts.py
COPY ./layers.py /srv/layers.py
COPY ./audio_processing.py /srv/audio_processing.py
COPY ./stft.py /srv/stft.py
COPY ./text /srv/text
COPY ./templates /srv/templates


RUN mkdir /srv/models
WORKDIR /srv/models
RUN wget -q https://www.softcatala.org/pub/softcatala/catotron-models/upc_ona_tacotron2.pt
RUN wget -q https://www.softcatala.org/pub/softcatala/catotron-models/upc_pau_tacotron2.pt
RUN wget -q https://www.softcatala.org/pub/softcatala/catotron-models/melgan_onapau_catotron.pt

WORKDIR /srv

ENTRYPOINT [ "python" ]
CMD [ "demo_server.py" ]