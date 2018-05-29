# Docker container that calculates the SVD decomposition over the data.
# Gets the main componets, the average and the iterative standard deviation
FROM python:3
MAINTAINER Santiago Smith <sssilvar@unal.edu.co>

# Set proxy (if necessary) --build-arg
ARG proxy
ENV http_proxy=$proxy

# Prevent dpkg errors
ENV TERM=xterm-256color

# # Update container
# RUN apt-get -y update && \
# 	apt-get -y install python3 python3-numpy python3-pandas python3-requests

# Set Server URL
ENV API_HOST="http://ec2-34-217-80-61.us-west-2.compute.amazonaws.com:3300/"
ENV CLIENT_ID="5b0c370074a6fd000f8a4c32"


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