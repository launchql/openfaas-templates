FROM openfaas/of-watchdog:0.7.7 as watchdog

FROM python:3.8.5-alpine3.11

# Allows you to add additional packages via build-arg
ARG ADDITIONAL_PACKAGE

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

RUN apk --no-cache add ca-certificates ${ADDITIONAL_PACKAGE}

# Add non root user
RUN addgroup -S app && adduser app -S -G app

WORKDIR /home/app/

COPY index.py .
COPY requirements.txt .

RUN chown -R app /home/app && \
  mkdir -p /home/app/python && chown -R app /home/app

USER app
ENV PATH=$PATH:/home/app/.local/bin:/home/app/python/bin/
ENV PYTHONPATH=$PYTHONPATH:/home/app/python
RUN pip install -r requirements.txt --target=/home/app/python

RUN mkdir -p function
RUN touch ./function/__init__.py

WORKDIR /home/app/function/
COPY function/requirements.txt	.

RUN pip install -r requirements.txt --target=/home/app/python

WORKDIR /home/app/

COPY function function

USER root
RUN chown -R app:app ./ && \
  chown -R app:app /home/app && \
  chmod -R 777 /home/app

USER app

ENV cgi_headers="true"
ENV fprocess="python index.py"
ENV mode="http"
ENV PORT 10101
ENV upstream_url="http://127.0.0.1:10101"

ENV exec_timeout="20s" 
ENV write_timeout="25s" 
ENV read_timeout="25s" 

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1
CMD ["fwatchdog"]