# Create a base docker container that will execute the FreeSurfer recon-all pipeline and
# put the results in the /output foder
#
# Example usage:
#   docker run --rm -ti \
#       -v </groupfile/directory>:/group \
#       -v </input/directory>:/input \
#       -v </output/directory>:/output \
#       sssilvar/recon_all /group/groupfile.csv /input /output
#


FROM freesurfer/freesurfer:6.0
MAINTAINER Santiago Smith <sssilvar@unal.edu.co>

# Set proxy (if necessary) --build-arg
ARG proxy
ENV http_proxy=$proxy

# Prevent dpkg errors
ENV TERM=xterm-256color

# Update container
RUN apt-get -y update && \
	apt-get -y install perl tcsh bash wget unzip python3

# Copy license to container
COPY ../license /opt/freesurfer/.license

# Create an input and an output folders
RUN mkdir /input && mkdir /output && mkdir /group && mkdir /root/scripts

# Add scripts to container
ADD scripts /root/scripts

# Run entrypoint
ENTRYPOINT ["/root/scripts/entrypoint.sh"]
