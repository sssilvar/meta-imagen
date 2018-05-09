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


FROM freesurfer/freesurfer:6.0
MAINTAINER Santiago Smith <sssilvar@unal.edu.co>

# Set proxy (if necessary) --build-arg
ARG proxy
ENV http_proxy=$proxy

# Prevent dpkg errors
ENV TERM=xterm-256color

# Update container
RUN apt-get -y update && \
	apt-get -y install perl tcsh bash wget unzip

# Copy license to container
COPY license /opt/freesurfer/.license

# Create an input and an output folders
RUN mkdir /input && mkdir /output && mkdir /group

# Add enigma shape analysis
ADD enigma_shape /root/enigma_shape
RUN chmod -R 777 /root/enigma_shape

# Set Environment Variables
ENV FS=/opt/freesurfer
ENV runDirectory=/root/enigma_shape/

# ENTRYPOINT ["/root/enigma_shape/shape_group_run.sh"]
ENTRYPOINT ["/root/enigma_shape/run_analysis.sh"]
#RUN ./root/enigma_shape/shape_group_run.sh /group/groupfile.csv /input /output
