FROM python:3.9.0

RUN pip3 install \
        --upgrade pip \
        python-dotenv \
        pytz \
        jupyter \
        mysqlclient \
        tornado \
        && mkdir ~/.jupyter \
        && echo 'c.NotebookApp.token = ""' > ~/.jupyter/jupyter_notebook_config.py \
        && echo 'c.NotebookApp.password = ""' >> ~/.jupyter/jupyter_notebook_config.py

CMD ["/usr/local/bin/jupyter", "notebook", "--port", "8888", "--ip=0.0.0.0", "--allow-root"]
