#!/bin/zsh

cp ./openastro.package/dist/** ./package.deployment/
gcloud config set project [GCP-PROJECT]
gcloud builds submit --tag gcr.io/[GCP-PROJECT]/[GCP-SERVICE] .
gcloud run deploy [GCP-PROJECT] --image gcr.io/[GCP-PROJECT]/[GCP-SERVICE] --platform managed --region us-east4 --allow-unauthenticated
