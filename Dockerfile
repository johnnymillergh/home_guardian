FROM --platform=$BUILDPLATFORM python:3.7.3-slim AS base

ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM"

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN apt-get install -y libhdf5-dev libhdf5-serial-dev libhdf5-103
RUN apt-get install -y libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
RUN apt-get install -y libatlas-base-dev
RUN apt-get install -y libjasper-dev

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Has to use "root" user to run this application
WORKDIR /app

# Install application into container
COPY . .
RUN chmod +x /app/docker-entrypoint.sh

# Run the executable
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python", "-m", "home_guardian", "detect"]
