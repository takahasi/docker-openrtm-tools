FROM takahasi/docker-openrtm

RUN pip install chainer && \
    pip install opencv-python

COPY ImageToObjectPrediction /tmp/

CMD ["cd /tmp && python ImageToObjectPrediction.py", ""]
