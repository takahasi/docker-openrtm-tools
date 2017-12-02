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
  openrtp             : Run OpenRTP
  bash                : Run bash
  Composit            : Run C++ example component "Composite"
  ConsigSample        : Run C++ example component "ConsigSampleComp"
  ConsoleIn           : Run C++ example component "ConsoleInComp"
  ConsoleInPy         : Run Python example component "ConsoleInComp"
  ConsoleOut          : Run C++ example component "ConsoleOutComp"
  ConsoleOutPy        : Run Python example component "ConsoleOutComp"
  Controller          : Run C++ example component "ControllerComp"
  Motor               : Run C++ example component "MotorComp"
  SeqIn               : Run C++ example component "SeqInComp"
  SeqInPy             : Run Python example component "SeqInComp"
  SeqOut              : Run C++ example component "SeqOutComp"
  SeqOutPy            : Run Python example component "SeqOutComp"
  TkJoyStick          : Run Python example component "TkJoyStick"
  TkLRFViewer         : Run Python example component "TkLRFViewer"
  MyServiceConsumer   : Run C++ example component "SeqOutComp"
  MyServiceConsumerPy : Run Python example component "SeqOutComp"
  MyServiceProvider   : Run C++ example component "SeqOutComp"
  MyServiceProviderPy : Run Python example component "SeqOutComp"
  Sensor              : Run C++ example component "SensorComp"

Options:
  -h, --help          : Print this message
  -v, --version       : Print version of this script
  -n, --nameserver    : Run command with starting nameserver
  -t, --tag TAGNAME   : Tag of image
  -r, --run COMPONENT : Run your component
  -c, --compile [ARG] : Compile your C++ component
  -x, --xforward      : Enable X-forwarding
EOS
  exit 1
}

function set_command()
{
  local example="/usr/share/openrtm-1.1/example"
  local example_py="$example/python"

  case "$1" in
    'openrtp')
      command="openrtp"
    ;;
    'Controller')
      command="$example/ControllerComp"
      ;;
    'Motor')
      command="$example/MotorComp"
      ;;
    'ConsoleIn')
      command="$example/ConsoleInComp"
      ;;
    'ConsoleOut')
      command="$example/ConsoleOutComp"
      ;;
    'SeqOut')
      command="$example/SeqOutComp"
      ;;
    'SeqIn')
      command="$example/SeqInComp"
      ;;
    'ConsoleInPy')
      command="python $example_py/SimpleIO/ConsoleIn.py"
      ;;
    'ConsoleOutPy')
      command="python $example_py/SimpleIO/ConsoleOut.py"
      ;;
    'SeqOutPy')
      command="python $example_py/SeqIO/SeqOut.py"
      ;;
    'SeqInPy')
      command="python $example_py/SeqIO/SeqIn.py"
      ;;
    'TkJoyStick')
      command="python $example_py/TkJoyStick/TkJoyStickComp.py"
      ;;
    'TkLRFViewer')
      command="python $example_py/TkLRFViewer/TkLRFViewer.py"
      ;;
    'MyServiceConsumer')
      command="$example/MyServiceConsumerComp"
      ;;
    'MyServiceProvider')
      command="$example/MyServiceProviderComp"
      ;;
    'MyServiceConsumerPy')
      command="python $example_py/SimpleService/MyServiceConsumer.py"
      ;;
    'MyServiceProviderPy')
      command="python $example_py/SimpleService/MyServiceProvider.py"
      ;;
    'Sensor')
      command="$example/SensorComp"
      ;;
    'bash'|*)
      command="bash"
      ;;
  esac

  return
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

set_command "$param"

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
