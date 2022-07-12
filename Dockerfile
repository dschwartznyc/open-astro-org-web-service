# local build: 
# docker build . -t danschwartz/open-astro-org-web-service
# gcloud - build:
# gcloud builds submit --tag gcr.io/cc-web-service-279214/open-astro-org-web-service .
# gcloud - deploy:
# gcloud run deploy cc-web-framework-service --image gcr.io/cc-web-service-279214/cc-web-service --platform managed --region us-east4 --allow-unauthenticated
# nb - copy the python deployments (tar.gz) to pip-deployment

FROM python:3.10.5

LABEL Dan Schwartz "daniel.schwartz@ftadvisory.co"

RUN apt-get update -y && \
    apt-get install gcc

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /open-astro-web-service/requirements.txt

WORKDIR /open-astro-web-service

RUN pip install -r requirements.txt

COPY ./package.deployment/openastro-1.1.57.tar.gz tmp/
RUN pip install ./tmp/openastro-1.1.57.tar.gz

COPY ./app/*.py /open-astro-web-service/app/
WORKDIR /open-astro-web-service/app

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
EXPOSE 5000