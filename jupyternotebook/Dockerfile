#######################################
# DESCRIPTION: Dockerfile for healthcan
# Container: JupyterNotebook
# Owner: RenGoto
#######################################
FROM python:3.7.4
MAINTAINER "Ren Goto" <r0719en@pluslab.org>

RUN pip3 install \
        numpy \
        pandas \
        matplotlib \
        jupyter \
        mysqlclient \
        tornado \
        && mkdir ~/.jupyter \
        && echo 'c.NotebookApp.token = ""' > ~/.jupyter/jupyter_notebook_config.py \
        && echo 'c.NotebookApp.password = ""' >> ~/.jupyter/jupyter_notebook_config.py

EXPOSE 8888
EXPOSE 3000
CMD ["/usr/local/bin/jupyter", "notebook", "--port", "8888", "--ip=0.0.0.0", "--allow-root"]
