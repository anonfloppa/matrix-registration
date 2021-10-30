ARG PYTHON_VERSION=3.8

FROM docker.io/python:${PYTHON_VERSION} as builder

COPY README.md setup.py config.sample.yaml /tmp/matrix-registration/
COPY matrix_registration /tmp/matrix-registration/matrix_registration/

RUN pip install --prefix="/install" --no-warn-script-location \
		/tmp/matrix-registration[postgres]

# Runtime
FROM docker.io/python:${PYTHON_VERSION}

COPY --from=builder /install /usr/local

VOLUME ["/data"]

EXPOSE 5000/tcp

ENTRYPOINT ["matrix-registration", "--config-path=/data/config.yaml"]