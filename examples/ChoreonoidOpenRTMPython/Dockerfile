FROM takahasi/docker-openrtm:ubuntu1604_openrtm112-desktop
LABEL maintainer="takahasi <3263ta@gmail.com>" \
      description="OpenRTM Choreonoid on Docker: Choreonoid on Docker images." \
      build_type="ubuntu"

ENV DEBIAN_FRONTEND noninteractive

RUN git clone --depth=1 https://github.com/Nobu19800/choreonoid.git && \
    cd choreonoid && \
    ./misc/script/install-requisites-ubuntu-16.04.sh && \
    mkdir build && cd build && \
    cmake .. -DENABLE_PYTHON=ON -DBUILD_PYTHON_PLUGIN=ON -DBUILD_OPENRTM_PYTHON_PLUGIN=ON -DENABLE_CORBA=ON -DBUILD_CORBA_PLUGIN=ON -DBUILD_OPENRTM_PLUGIN=ON && \
    make && make install && \
    cd .. && \
    apt-get install -y libsdl2-2.0-0 libsdl2-image-2.0-0 wget && \
    wget https://bitbucket.org/marcusva/py-sdl2/downloads/PySDL2-0.9.5.tar.gz && \
    tar xf PySDL2-0.9.5.tar.gz && \
    cd PySDL2-0.9.5 && python setup.py install

ENTRYPOINT ["choreonoid", ""]
