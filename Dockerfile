FROM python:3.4.3
MAINTAINER Chris Gibson "cgibson@mrvoxel.com"

# Copy the app source/data
COPY . /app
WORKDIR /app

# Install python requirements
RUN pip install -r requirements.txt

# Authorize bitbucket as an SSH host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh

# Tell ssh where to find the identify file.
RUN echo "    IdentityFile /root/.ssh/id_rsa" >> /etc/ssh/ssh_config

# Reassure ssh we know bitbucket.com
RUN ssh-keyscan -t rsa bitbucket.com > ~/.ssh/known_hosts

ENTRYPOINT ["python"]
CMD ["app.py"]
