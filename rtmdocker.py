import sys
import os
from argparse import ArgumentParser

prog = __file__
version = "1.0.0"

# TAG NAME (default)
tag = "latest"

# Docker Hub Image
image = "takahasi/docker-openrtm:" + tag

# Docker Option
entry = os.getcwd()
option = "-v $HOME:$HOME:rw --privileged=true -e ENTRY=" + entry
option_network = "--net=host"
option_display = "-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/root/.Xauthority"

pf = sys.platform


def parser():
    usage = 'Usage: python {} [-v] [-n] [-t <tag>] [-x] [-c <comp>] [-r <comp>] [--help] command'.format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('command', type=str, help='command')
    argparser.add_argument('-v', '--version', action='store_true', help='print version')
    argparser.add_argument('-n', '--nameserver', action='store_true', help='run command with starting nameserver')
    argparser.add_argument('-c', '--compile', type=str, dest='c_component', help='compile your C++ component')
    argparser.add_argument('-t', '--tag', type=str, dest='tagname', help='tag name of image')
    argparser.add_argument('-r', '--run', type=str, dest='r_component', help='run your component')
    argparser.add_argument('-x', '--xforward', action='store_true', help='enable X forwarding')
    return argparser.parse_args()


def set_command(s):
    example = "/usr/share/openrtm-1.1/example"
    example_py = "$example/python"

    c_dict = {"openrtp": "openrtp",
              "Controller": example + "/ControllerComp",
              "Motor": example + "/MotorComp",
              "ConsoleIn": example + "/ConsoleInComp",
              "ConsoleOut": example + "/ConsoleOutComp",
              "SeqIn": example + "/SeqInComp",
              "SeqOut": example + "/SeqOutComp",
              "MyServiceConsumer": example + "/MyServiceConsumerComp",
              "MyServiceProvider": example + "/MyServiceProviderComp",
              "ConsoleInPy": "python" + example_py + "/ConsoleIn.py",
              "ConsoleOutPy": "python" + example_py + "/ConsoleOut.py",
              "SeqInPy": "python " + example_py + "/SeqIn.py",
              "SeqOutPy": "python " + example_py + "/SeqOut.py",
              "MyServiceConsumerPy": "python " + example_py + "/MyServiceConsumerComp",
              "MyServiceProviderPy": "python " + example_py + "/MyServiceProviderComp",
              "TkJoyStick": "python " + example_py + "/TkJoyStickComp.py",
              "TkLRFViewer": "python " + example_py + "/TkLRFViewer.py",
              "bash": "bash",
              }

    c = c_dict[s]
    if c is None:
        return "bash"
    else:
        return c


def enable_x():
    os.system("xhost local: > /dev/null")
    return


def disable_x():
    os.system("xhost - > /dev/null")
    return


def main():
    args = parser()
    if pf == "win32":
        print("not yet")
    else:
        # darwin, linux
        command = set_command(args.command)

        option_list = []
        option_list.append(option)

        if args.xforward:
            enable_x()
            option_list.append(option_display)

        if args.nameserver:
            command = "rtm-naming;" + command

        if args.compile:
            command = "apt-get update && apt-get -y install cmake && cd " + entry + " && mkdir -p build && cd build cmake .. && make"

        if args.run:
            command = args.r_component

        option_list.append(option_network)
        option_list.append(image)
        option_list.append("\"" + command + "\"")
        print("docker run -ti --rm " + " ".join(option_list))
        os.system("docker run -ti --rm " + " ".join(option_list))

        if args.xforward:
            disable_x()

    return

if __name__ == "__main__":
    main()
