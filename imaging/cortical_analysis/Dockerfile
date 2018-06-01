# Docker container that performs the thickness and jacobian feature extraction
# Gets the main componets, the average and the iterative standard deviation
FROM freesurfer/freesurfer:6.0
MAINTAINER Santiago Smith <sssilvar@unal.edu.co>

# Set proxy (if necessary) --build-arg
ARG proxy
ENV http_proxy=$proxy

# Prevent dpkg errors
ENV TERM=xterm-256color

# Create data folder and set an ENV var
RUN mkdir /root/data
ENV DATA_FOLDER=/root/data

# Add the scripts to the Docker container
ADD scripts /root/scripts
RUN chmod -R 777 /root/scripts

# Install dependencies
RUN apt-get -y update && apt-get -y install python3 python3-pip python3-pandas openjdk-7-jdk
#RUN pip3 install -r /root/scripts/requirements.txt

# Copy license to container
COPY license /opt/freesurfer/.license

# Define an entrypoint
ENTRYPOINT ["/root/scripts/entrypoint.sh"]