#!/bin/bash

git clone --depth 1 https://github.com/takahasi/ImageToObjectPrediction.git
docker build --network=host -t sample .
docker run --network=host -it sample

exit 0
