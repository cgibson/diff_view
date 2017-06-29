FROM python:latest
MAINTAINER Christopher Gibson "cgibson@mrvoxel.com"

# Copy the app source/data
COPY . /app
WORKDIR /app

# Install python requirements
RUN pip install -r requirements.txt

# Authorize bitbucket as an SSH host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh

ENTRYPOINT ["python"]
CMD ["app.py"]
