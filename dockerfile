FROM ubuntu:latest

RUN set -ex \
  && echo "==> Upgrading apk and system ...." \
  && apt -y update\
  && echo "==> Installing Python3 and pip ...." \  
  && apt-get install python3 -y \
  && apt install python3-pip -y \
  && apt install openssh-client -y \
  \
  && echo "==> Adding pyATS ..." \
  && pip install pyats[full] \ 
  && pip uninstall --yes markupsafe \
  && pip install markupsafe==1.1.1 \
  \
  && echo "==> Adding Rich ..." \
  && pip install rich

COPY Camelot/Cisco/DevNet_Sandbox/ /Camelot/Cisco/DevNet_Sandbox/
COPY templates/cisco/nxos/* /templates/cisco/nxos/
COPY testbed/testbed_DevNet_Nexus9k_Sandbox.yaml /testbed/
COPY ascii_art.py ./
COPY DevNet_Sandbox_Nexus9k_merlin_docker_job.py ./
COPY DevNet_Sandbox_Nexus9k_merlin_docker.py ./
COPY general_functionalities.py ./

ENTRYPOINT [ "pyats", "run", "job", "DevNet_Sandbox_Nexus9k_merlin_docker_job.py", "--testbed-file" ]

CMD ["testbed/testbed_DevNet_Nexus9k_Sandbox.yaml"]