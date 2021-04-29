FROM python:3.9.0

RUN pip3 install \
        --upgrade pip \
        numpy \
        pandas \
        matplotlib \
        jupyter \
        mysqlclient \
        tornado \
        && mkdir ~/.jupyter \
        && echo 'c.NotebookApp.token = ""' > ~/.jupyter/jupyter_notebook_config.py \
        && echo 'c.NotebookApp.password = ""' >> ~/.jupyter/jupyter_notebook_config.py

EXPOSE 3000
