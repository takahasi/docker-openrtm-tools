#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

import sys
import os
import argparse


class Rtmdocker:
    ''' Utility class to operate OpenRTM on Docker

    This is utility class to operate OpenRTM on Docker.

    '''
    def __init__(self):
        self._platform = sys.platform
        self._args = self.parser()

    def start(self):
        command = self.assume_command(self._args.command)
        self._command = self.assume_options(self._args, command)
        if self._args.xforward:
            self.enable_x()

        # Start Docker
        print(self._command)
        os.system(self._command)

        if self._args.xforward:
            self.disable_x()

        return

    def parser(self):
        usage = 'Usage: python {} [-v] [-n] [-t <tag>] [-x] [-c <comp>] [-r <comp>] [--help] command'.format(__file__)
        help_message = 'openrtp             : start OpenRTP\n' + \
                       'Controller          : start C++ ControllerComp\n' + \
                       'Motor               : start C++ MotorComp\n' + \
                       'ConsoleIn           : start C++ ConsoleInComp\n' + \
                       'ConsoleOut          : start C++ ConsoleOutComp\n' + \
                       'SeqIn               : start C++ SeqInComp\n' + \
                       'SeqOut              : start C++ SeqOutComp\n' + \
                       'MyServiceConsumer   : start C++ MyServiceConsumerComp\n' + \
                       'MyServiceProvider   : start C++ MyServiceProviderComp\n' + \
                       'ConsoleInPy         : start Python ConsoleIn.py\n' + \
                       'ConsoleOutPy        : start Python ConsoleOut.py\n' + \
                       'SeqInPy             : start Python SeqIn.py\n' + \
                       'SeqOutPy            : start Python SeqOut.py\n' + \
                       'MyServiceConsumerPy : start Python MyServiceConsumerComp\n' + \
                       'MyServiceProviderPy : start Python MyServiceProviderComp\n' + \
                       'TkJoyStick          : start Python TkJoyStickComp.py\n' + \
                       'TkLRFViewer         : start Python TkLRFViewer.py\n' + \
                       'bash                : start bash'
        argparser = argparse.ArgumentParser(usage=usage, formatter_class=argparse.RawTextHelpFormatter)
        argparser.add_argument('command', type=str, default='bash', help=help_message)
        argparser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')
        argparser.add_argument('-n', '--nameserver', action='store_true', help='run command with starting nameserver')
        argparser.add_argument('-t', '--tag', type=str, dest='tagname', default='latest', help='tag name of image')
        argparser.add_argument('-r', '--rdp', action='store_true', help='run command with start RDP server')
        argparser.add_argument('-e', '--execute', type=str, dest='run_component', help='run your C++ component')
        argparser.add_argument('-c', '--compile', type=str, dest='compile_component', help='compile your C++ component')
        argparser.add_argument('-x', '--xforward', action='store_true', help='enable X forwarding')
        return argparser.parse_args()

    def assume_command(self, command):
        example = "/usr/share/openrtm-1.1/example"
        example_py = "python " + example + "/python"

        # command list
        c_dict = {"openrtp": "openrtp",
                  "Controller": example + "/ControllerComp",
                  "Motor": example + "/MotorComp",
                  "ConsoleIn": example + "/ConsoleInComp",
                  "ConsoleOut": example + "/ConsoleOutComp",
                  "SeqIn": example + "/SeqInComp",
                  "SeqOut": example + "/SeqOutComp",
                  "MyServiceConsumer": example + "/MyServiceConsumerComp",
                  "MyServiceProvider": example + "/MyServiceProviderComp",
                  "ConsoleInPy": example_py + "/SimpleIO/ConsoleIn.py",
                  "ConsoleOutPy": example_py + "/SimpleIO/ConsoleOut.py",
                  "SeqInPy": example_py + "/SeqIO/SeqIn.py",
                  "SeqOutPy": example_py + "/SeqIO/SeqOut.py",
                  "MyServiceConsumerPy": example_py + "/SimpleService/MyServiceConsumerComp",
                  "MyServiceProviderPy": example_py + "/SimpleService/MyServiceProviderComp",
                  "TkJoyStick": example_py + "/TkJoyStick/TkJoyStickComp.py",
                  "TkLRFViewer": example_py + "/TkLRFViewer/TkLRFViewer.py",
                  "bash": "bash",
                  }

        c = c_dict[command]
        if c is None:
            return "bash"
        else:
            return c

    def assume_options(self, args, command):
        # Docker Option
        option_list = []

        # Mount home directory
        if self._platform == "win32":
            user = os.environ.get('USERNAME')
            home = os.environ.get('USERPROFILE')
            print(home)
            option = "-v " + home + ":/home/" + user + ":rw --privileged=true"
        else:
            home = os.environ.get('HOME')
            option = "-v " + home + ":" + home + ":rw --privileged=true"
        option_list.append(option)

        # Set X forwarding
        if args.xforward:
            user = os.environ.get('DISPLAY')
            option_display = "-e DISPLAY=" + display + "-v /tmp/.X11-unix:/tmp/.X11-unix -v " + home + "/.Xauthority:/root/.Xauthority"
            option_list.append(option_display)

        if args.rdp:
            # Add starting xrdp service
            command = "/etc/init.d/xrdp start;" + command

        if args.nameserver:
            # Add starting nameserver
            command = "rtm-naming;" + command

        entry = os.getcwd()
        if args.compile_component:
            # Compile C++ component
            command = "apt-get update && apt-get -y install cmake && cd " + entry + " && mkdir -p build && cd build cmake .. && make"

        if args.run_component:
            if args.run_component in '.py':
                # Python compnent
                command = "cd " + entry + " && python " + args.run_component
            else:
                # C++ compnent
                command = "cd " + entry + " && ./" + args.run_component

        option_network = "--net=host"
        option_list.append(option_network)
        option_list.append("takahasi/docker-openrtm:" + args.tagname)
        option_list.append("\"" + command + "\"")
        return "docker run -ti --rm " + " ".join(option_list)

    def enable_x(self):
        if self._platform != "win32":
            os.system("xhost local: > /dev/null")
        return

    def disable_x(self):
        if self._platform != "win32":
            os.system("xhost - > /dev/null")
        return


def main():
    rtmdocker = Rtmdocker()
    rtmdocker.start()
    return

if __name__ == "__main__":
    main()
