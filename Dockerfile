FROM python:latest
MAINTAINER Chris Gibson "cgibson@mrvoxel.com"

# Arguments for SSH public/private keys
ARG ssh_prv_key
ARG ssh_pub_key

# Copy the app source/data
COPY . /app
WORKDIR /app

# Install python requirements
RUN pip install -r requirements.txt

# Authorize bitbucket as an SSH host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan bitbucket.com > /root/.ssh/known_hosts

# Add the SSH public/private keys and set permissions
RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
    echo "$ssh_pub_key" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

ENTRYPOINT ["python"]
CMD ["app.py"]
