#
# Necrospider Dockerfile
#
# http://www.necrospider.net
#
# Written by: Michael Pellon <m@pellon.io>
# Updated by: Chandrapal <bnchandrapal@protonmail.com>
# Updated by: Steve Micallef <steve@binarypool.com>
# Updated by: Steve Bate <svc-necrospider@stevebate.net>
#    -> Inspired by https://github.com/combro2k/dockerfiles/tree/master/alpine-necrospider
#
# Usage:
#
#   sudo docker build -t necrospider .
#   sudo docker run -p 5001:5001 --security-opt no-new-privileges necrospider
#
# Using Docker volume for necrospider data
#
#   sudo docker run -p 5001:5001 -v /mydir/necrospider:/var/lib/necrospider necrospider
#
# Using NecroSpider remote command line with web server
#
#   docker run --rm -it necrospider sfcli.py -s http://my.necrospider.host:5001/
#
# Running necrospider commands without web server (can optionally specify volume)
#
#   sudo docker run --rm necrospider sf.py -h
#
# Running a shell in the container for maintenance
#   sudo docker run -it --entrypoint /bin/sh necrospider
#
# Running necrospider unit tests in container
#
#   sudo docker build -t necrospider-test --build-arg REQUIREMENTS=test/requirements.txt .
#   sudo docker run --rm necrospider-test -m pytest --flake8 .

FROM alpine:3.12.4 AS build
ARG REQUIREMENTS=requirements.txt
RUN apk add --no-cache gcc git curl python3 python3-dev py3-pip swig tinyxml-dev \
 python3-dev musl-dev openssl-dev libffi-dev libxslt-dev libxml2-dev jpeg-dev \
 openjpeg-dev zlib-dev cargo rust
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin":$PATH
COPY $REQUIREMENTS requirements.txt ./
RUN ls
RUN echo "$REQUIREMENTS"
RUN pip3 install -U pip
RUN pip3 install -r "$REQUIREMENTS"



FROM alpine:3.13.0
WORKDIR /home/necrospider

# Place database and logs outside installation directory
ENV NECROSPIDER_DATA /var/lib/necrospider
ENV NECROSPIDER_LOGS /var/lib/necrospider/log
ENV NECROSPIDER_CACHE /var/lib/necrospider/cache

# Run everything as one command so that only one layer is created
RUN apk --update --no-cache add python3 musl openssl libxslt tinyxml libxml2 jpeg zlib openjpeg \
    && addgroup necrospider \
    && adduser -G necrospider -h /home/necrospider -s /sbin/nologin \
               -g "NecroSpider User" -D necrospider \
    && rm -rf /var/cache/apk/* \
    && rm -rf /lib/apk/db \
    && rm -rf /root/.cache \
    && mkdir -p $NECROSPIDER_DATA || true \
    && mkdir -p $NECROSPIDER_LOGS || true \
    && mkdir -p $NECROSPIDER_CACHE || true \
    && chown necrospider:necrospider $NECROSPIDER_DATA \
    && chown necrospider:necrospider $NECROSPIDER_LOGS \
    && chown necrospider:necrospider $NECROSPIDER_CACHE

COPY . .
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

USER necrospider

EXPOSE 5001

# Run the application.
ENTRYPOINT ["/opt/venv/bin/python"]
CMD ["sf.py", "-l", "0.0.0.0:5001"]
