# Create a base docker container that will execute the ENIGMA Shape analysis and
# put the results in the /output foder
#
# Example usage:
#   docker run --rm -ti \
#       -v </groupfile/directory>:/group \
#       -v </input/directory>:/input \
#       -v </output/directory>:/output \
#       sssilvar/eshape_fs /group/groupfile.csv /input /output
#


FROM ubuntu:16.04
MAINTAINER Santiago Smith <sssilvar@unal.edu.co>

# Set proxy (if necessary) --build-arg
ARG proxy
ENV http_proxy=$proxy

# Prevent dpkg errors
ENV TERM=xterm-256color

# Update container
RUN apt-get -y update && \
	apt-get -y install perl tcsh bash wget

# Download and Install Freesurfer
ADD freesurfer /usr/local/freesurfer
ENV FREESURFER_HOME=/usr/local/freesurfer
ENV FS=/usr/local/freesurfer

# Copy license to container
COPY license /usr/local/freesurfer/license.txt

# Create an input and an output folders
RUN mkdir /input && mkdir /output && mkdir /group

# Add enigma shape analysis
ADD enigma_shape /usr/local/enigma_shape
RUN chmod +x -R /usr/local/enigma_shape
ENV ENIGMA_SHAPE_DIR=/usr/local/enigma_shape/
ENTRYPOINT ["/usr/local/enigma_shape/shape_group_run.sh"]