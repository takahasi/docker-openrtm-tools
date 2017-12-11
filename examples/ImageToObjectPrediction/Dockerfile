FROM takahasi/docker-openrtm

RUN pip install chainer && \
    pip install opencv-python && \
    git clone https://github.com/takahasi/ImageToObjectPrediction.git /tmp/test

CMD ["cd /tmp/test && python ImageToObjectPrediction.py", ""]
