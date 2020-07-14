FROM python:latest
MAINTAINER Christopher Gibson "cgibson@mrvoxel.com"

# Copy the app source/data
COPY . /app
WORKDIR /app

# Install python requirements
RUN pip install -r requirements.txt
EXPOSE 5000

# Authorize bitbucket as an SSH host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh

ENV FLASK_APP /app/app.py
CMD ["flask", "run", "--host=0.0.0.0"]
