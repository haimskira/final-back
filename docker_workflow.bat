@echo off

REM Step 1: Build the Docker image
docker build -t django .

REM Step 2: Tag the Docker image
docker tag django haim1418/final-back

REM Step 3: Push the Docker image to the repository
docker push haim1418/final-back:latest
