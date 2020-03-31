FROM python:2.7-stretch

ENV CLOUDSDK_CORE_DISABLE_PROMPTS=1 \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH=.:/root/google-cloud-sdk/platform/google_appengine \
    PATH=${PATH}:/root/google-cloud-sdk/bin

RUN curl https://sdk.cloud.google.com | bash && \
    echo ". /root/google-cloud-sdk/path.bash.inc" >> /root/.bashrc && \
    echo ". /root/google-cloud-sdk/completion.bash.inc" >> /root/.bashrc && \
    /root/google-cloud-sdk/bin/gcloud components install app-engine-python app-engine-python-extras

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt
