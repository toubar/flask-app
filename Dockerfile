# Alpine images are recommended as they're tightly controlled and small in size while still being a full Linux distribution.
FROM python:3.7-alpine

LABEL author="Ahmed Toubar"
LABEL maintainer="aatoubar@gmail.com"
LABEL version="0.0.1"
LABEL description="This dockerfile builds an image for a flask API"

RUN adduser -D backend

WORKDIR /home/backend

# copy python project list of dependencies file (think package.json in a NodeJs app)
COPY requirements.txt requirements.txt

# create python virtual environement
RUN python -m venv venv

# install dependencies from requirements.txt
RUN venv/bin/pip install -r requirements.txt

# upgrade pip
RUN pip install --upgrade pip

# create environment variables
ENV FLASK_APP "main.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

# copy source code files
COPY services services
COPY static static
COPY main.py ./

# give backend use permission to backend directory
RUN chown -R backend:backend ./

USER backend

# expose the port on which a container listens for connections. Typically, the traditional port for the app at hand.
EXPOSE 5000

RUN source venv/bin/activate
CMD venv/bin/python -m flask run --host=0.0.0.0