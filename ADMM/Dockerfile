# Docker container that calculates the SVD decomposition over the data.
# Gets the main componets, the average and the iterative standard deviation
FROM python:3
MAINTAINER Santiago Smith <sssilvar@unal.edu.co>

# Set proxy (if necessary) --build-arg
ARG proxy
ENV http_proxy=$proxy

# Set ID
ARG id
ENV CLIENT_ID=$id

# Prevent dpkg errors
ENV TERM=xterm-256color

# Set Server URL
ARG server
ENV API_HOST=$server

# Create data folder and set an ENV var
RUN mkdir /root/data
ENV DATA_FOLDER=/root/data

# Add the scripts to the Docker container
ADD scripts /root/scripts
RUN chmod -R 777 /root/scripts

# Install dependencies
RUN pip install --no-cache-dir -r /root/scripts/requirements.txt

# Define an entrypoint
ENTRYPOINT ["/root/scripts/entrypoint.sh"]