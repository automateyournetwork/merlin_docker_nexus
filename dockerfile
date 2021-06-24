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

COPY Camelot/Show_IP_Interface_Brief/* /Camelot/Show_IP_Interface_Brief/
COPY templates/cisco/nxos/* /templates/cisco/nxos/
COPY testbed/testbed_DevNet_Nexus9k_Sandbox.yaml /testbed/
COPY ascii_art.py ./
COPY Nexus9k_ip_int_brief_job.py ./
COPY Nexus9k_ip_int_brief.py ./
COPY general_functionalities.py ./

ENTRYPOINT [ "pyats", "run", "job", "Nexus9k_ip_int_brief_job.py", "--testbed-file" ]

CMD ["testbed/testbed_DevNet_Nexus9k_Sandbox.yaml"]