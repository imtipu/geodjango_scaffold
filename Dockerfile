FROM python:3.8-slim as base

# libpq-dev and python3-dev help with psycopg2
RUN apt-get update \
  && apt-get install -y --no-install-recommends python3-dev libpq-dev gcc curl g++ \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
  # You can add additional steps to the build by appending commands down here using the
  # format `&& <command>`. Remember to add a `\` at the end of LOC 12.
  # WARNING: Changes to this file may cause unexpected behaviors when building the app.
  # Change it at your own risk.


RUN apt-get update \
    && apt-get install -y binutils gdal-bin libproj-dev libgdal-dev

#ARG CPLUS_INCLUDE_PATH=/usr/include/gdal
#ARG C_INCLUDE_PATH=/usr/include/gdal

RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal

#RUN export CFLAGS=$(gdal-config --cflags)

RUN gdal_version=$(gdal-config --version); echo $gdal_version
RUN export GDALHOME=/Library/Frameworks/GDAL.framework/Versions/Current/unix/

# RUN pip install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL
#RUN pip3 install GDAL --global-option=build_ext --global-option="-I/usr/include/gdal"

RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install gdal==`gdal-config --version`
#RUN apt-remove -y gcc g++ \
#  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/webapp
COPY Pipfile* /opt/webapp/

RUN pip3 install --no-cache-dir -q 'pipenv==2018.11.26'
RUN pipenv install --deploy --system

COPY . /opt/webapp

FROM base as release

COPY --from=base /root/.local /root/.local
COPY --from=base /opt/webapp/manage.py /opt/webapp/manage.py


WORKDIR /opt/webapp
ENV PATH=/root/.local/bin:$PATH
ARG SECRET_KEY
RUN python3 manage.py collectstatic --no-input

# Run the image as a non-root user
RUN adduser --disabled-password --gecos "" django
USER django
CMD waitress-serve --port=$PORT geodjango_scaffold.wsgi:application
