#!/bin/bash

set -e

prog=$(basename $0)
version=1.0.0

# TAG NAME (default)
tag="latest"

# Docker Hub Image
DH_USER=takahasi
DH_REPO=docker-openrtm

image=$DH_USER/$DH_REPO:$tag

# Docker Option
entry=$PWD
option="-v $HOME:$HOME:rw --privileged=true -e ENTRY=$entry"
option_network="--net=host"
option_display=""

# initialize flag
compile_flag=0
nameserver_flag=0
xforward_flag=0

function usage()
{
  cat << EOS
Usage: $prog [OPTIONS] COMMAND
  This is utility script for OpenRTM on Docker.

Command:
  rtm-naming        : Run name server
  openrtp           : Run OpenRTP
  bash              : Run bash
  Composit          : Run C++ example component "Composite"
  ConsigSample      : Run C++ example component "ConsigSampleComp"
  ConsoleIn         : Run C++ example component "ConsoleInComp"
  ConsoleOut        : Run C++ example component "ConsoleOutComp"
  Controller        : Run C++ example component "ControllerComp"
  Motor             : Run C++ example component "MotorComp"
  SeqIn             : Run C++ example component "SeqInComp"
  SeqOut            : Run C++ example component "SeqOutComp"
  MyServiceConsumer : Run C++ example component "SeqOutComp"
  MyServiceProvider : Run C++ example component "SeqOutComp"
  Sensor            : Run C++ example component "SensorComp"

Options:
  -h, --help          : Print this message
  -v, --version       : Print version of this script
  -n, --nameserver    : Run command with nameserver
  -t, --tag TAGNAME   : Tag
  -r, --run COMPONENT : Run your component
  -c, --compile [ARG] : Compile your C++ component
  -x, --xforward      : Enable X-forwarding
EOS
  exit 1
}


for OPT in "$@"
  do
    case "$OPT" in
      '-h'|'--help' )
        usage
        exit 1
        ;;
      '-v'|'--version' )
        echo $version
        exit 1
        ;;
      '-t'|'--tag' )
        if [[ -z "$2" ]] || [[ "$2" =~ ^-+ ]]; then
          echo "$prog: option requires an argument -- $1" 1>&2
          exit 1
        fi
        tag="$2"
        shift 2
        ;;
      '-c'|'--compile' )
        if [[ -z "$2" ]] || [[ "$2" =~ ^-+ ]]; then
          compile_flag=1
          compile_target="$PWD"
          shift
        else
          compile_flag=1
          compile_target="$PWD/$2"
          shift 2
        fi
        ;;
      '-n'|'--nameserver' )
        nameserver_flag=1
        shift 1
        ;;
      '-x'|'--xforward' )
        xforward_flag=1
        shift 1
        ;;
      '--'|'-' )
        shift 1
        param+=( "$@" )
        break
        ;;
      -*)
        echo "$prog: illegal option -- '$(echo $1 | sed 's/^-*//')'" 1>&2
        exit 1
        ;;
      *)
        if [[ ! -z "$1" ]] && [[ ! "$1" =~ ^-+ ]]; then
          param+=( "$1" )
          shift 1
        fi
        ;;
    esac
done

case "$param" in
  'openrtp')
    command="openrtp"
    ;;
  'Controller')
    command="/usr/share/openrtm-1.1/example/ControllerComp"
    ;;
  'ConsoleIn')
    command="/usr/share/openrtm-1.1/example/ConsoleInComp"
    ;;
  'ConsoleOut')
    command="/usr/share/openrtm-1.1/example/ConsoleInComp"
    ;;
  'Motor')
    command="/usr/share/openrtm-1.1/example/MotorComp"
    ;;
  'SeqOut')
    command="/usr/share/openrtm-1.1/example/SeqOutComp"
    ;;
  'SeqIn')
    command="/usr/share/openrtm-1.1/example/SeqInComp"
    ;;
  'Sensor')
    command="/usr/share/openrtm-1.1/example/SensorComp"
    ;;
  'bash'|*)
    command="bash"
    ;;
esac

if [[ "$compile_flag" == "1" ]]; then
    command="apt-get update && apt-get -y install cmake && cd $compile_target && mkdir -p build && cd build cmake .. && make"
fi

if [[ "$nameserver_flag" == "1" ]]; then
    command="rtm-naming;"$command
fi

if [[ "$xforward_flag" == "1" ]]; then
  # Enable X11-forwarding
  xhost local: > /dev/null
  option_display="-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/root/.Xauthority"
fi

# Start docker
echo "IMAGE: $image/COMMAND: $command"
docker run -ti --rm $option $option_display $option_network $image "$command"

if [[ "$xforward_flag" == "1" ]]; then
  # Disable X11-forwarding
  xhost - > /dev/null
fi

exit 0
