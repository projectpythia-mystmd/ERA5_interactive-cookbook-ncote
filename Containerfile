# Use an official Python runtime as a base image
FROM docker.io/mambaorg/micromamba:latest

USER root

RUN apt-get update && apt-get install -y git-all

# Set the working directory in the container to /app
WORKDIR /home/mambauser/app

# Copy the current directory contents into the container at /usr/src/app
RUN git clone https://github.com/NicholasCote/ERA5_interactive-cookbook-ncote.git

# Install any needed packages specified in requirements.yml
RUN micromamba env create -f ERA5_interactive-cookbook-ncote/environment.yml

RUN mv ERA5_interactive-cookbook-ncote/notebooks/04_dashboard.ipynb .

RUN rm -r ERA5_interactive-cookbook-ncote/

# Activate the environment by providing ENV_NAME as an environment variable at runtime 
# Make port bokeh application port to the world outside this container
EXPOSE 5006

USER mambauser

CMD ["panel", "serve", "04_dashboard.ipynb", "--allow-websocket-origin=*", "--autoreload"]