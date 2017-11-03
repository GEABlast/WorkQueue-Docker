FROM ubuntu:14.04

# Setup CCTools+WorkQueue
COPY cctools-6.2.2-source.tar.gz /usr/src

RUN cd /usr/src && tar xvfz cctools-6.2.2-source.tar.gz && rm cctools-6.2.2-source.tar.gz \
    && apt-get update \
    && apt-get install -y python python-dev python3 python3-dev python-pip python3-pip swig libperl-dev zlib1g-dev \
    && pip install psutil \
    && cd cctools-6.2.2-source && ./configure --prefix /usr/src/cctools && make install \
    && cd && rm -r /usr/src/cctools-6.2.2-source

# Setup test suite.
COPY test /usr/local/bin

# Set paths.
ENV PATH="${PATH}:/usr/src/cctools/bin"
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/cctools/lib/python2.7/site-packages"