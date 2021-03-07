FROM pytorch/pytorch
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt

