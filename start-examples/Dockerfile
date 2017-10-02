FROM takahasi/docker-openrtm
LABEL maintainer="takahasi <3263ta@gmail.com>" \
      description="Example of OpenRTM on Docker."

ENV DEBIAN_FRONTEND noninteractive

CMD ["rtm-naming", ""]
CMD ["/usr/share/openrtm-1.1/example/SeqInComp", ""]
CMD ["/usr/share/openrtm-1.1/example/SeqOutComp", ""]
CMD ["/usr/share/openrtm-1.1/example/MotorComp", ""]
CMD ["/usr/share/openrtm-1.1/example/SensorComp", ""]
CMD ["openrtp", ""]

ENTRYPOINT ["/bin/bash", "-c"]
EXPOSE 80
