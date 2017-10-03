FROM takahasi/docker-openrtm
LABEL maintainer="takahasi <3263ta@gmail.com>" \
      description="Examples of OpenRTM on Docker."

ADD rtc-run.sh /etc/rtc-run.sh
CMD ["/etc/rtc-run.sh"]

ENTRYPOINT ["/bin/bash", "-c"]
EXPOSE 80
