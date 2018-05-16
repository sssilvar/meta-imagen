# Docker container that calculates the SVD decomposition over the data.
# Gets the main componets, the average and the iterative standard deviation
FROM ubuntu:16.04
MAINTAINER Santiago Smith <sssilvar@unal.edu.co>

# Set proxy (if necessary) --build-arg
ARG proxy
ENV http_proxy=$proxy

# Prevent dpkg errors
ENV TERM=xterm-256color
ENV DATA_FOLDER=/data

# Update container
RUN apt-get -y update && \
	apt-get -y install python3
RUN mkdir ${DATA_FOLDER}

# Add the scripts to the Docker container
ADD scripts /root/scripts
RUN chmod -R 777 /root/scripts

# Define an entrypoint
ENTRYPOINT ["/root/scripts/entrypoint.sh"]