#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

import sys
import os
import subprocess
import argparse
import logging
import distutils.spawn
import random


class Rtmdocker:
    ''' Utility class to operate OpenRTM on Docker

    This is utility class to operate OpenRTM on Docker.

    '''

    def __init__(self):
        # Set parser
        self._args = self.parser()
        # Set logger
        logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s',
                            level=logging.INFO)
        # Set platform
        self._platform = sys.platform
        logging.info("platform: : " + self._platform)
        # Check docker command existing
        if not distutils.spawn.find_executable('docker'):
            logging.error(
                "Docker is not installed. Please install Docker first.")
            sys.exit(1)

    def start(self):
        command = self.assume_command(self._args.command)
        self._command = self.assume_options(self._args, command)
        # Open x-forwarding
        if self._args.xforward:
            self.enable_x()

        # Start Docker
        logging.info("command: " + self._command)
        if not self._args.dryrun:
            logging.info("start docker ...")
            try:
                subprocess.call(self._command, shell=True)
            except subprocess.CalledProcessError:
                logging.error("Docker was exited by exception")

        # Close x-forwarding
        if self._args.xforward:
            self.disable_x()

        return

    def parser(self):
        help_message = 'openrtp             : start OpenRTP\n' + \
                       'Controller          : start C++ ControllerComp\n' + \
                       'Motor               : start C++ MotorComp\n' + \
                       'ConsoleIn           : start C++ ConsoleInComp\n' + \
                       'ConsoleOut          : start C++ ConsoleOutComp\n' + \
                       'ConfigSample        : start C++ ConfigSampleComp\n' + \
                       'SeqIn               : start C++ SeqInComp\n' + \
                       'SeqOut              : start C++ SeqOutComp\n' + \
                       'MyServiceConsumer   : start C++ MyServiceConsumerComp\n' + \
                       'MyServiceProvider   : start C++ MyServiceProviderComp\n' + \
                       'ConsoleInPy         : start Python ConsoleIn.py\n' + \
                       'ConsoleOutPy        : start Python ConsoleOut.py\n' + \
                       'ConfigSamplePy      : start Python ConfigSampleComp\n' + \
                       'SeqInPy             : start Python SeqIn.py\n' + \
                       'SeqOutPy            : start Python SeqOut.py\n' + \
                       'MyServiceConsumerPy : start Python MyServiceConsumerComp\n' + \
                       'MyServiceProviderPy : start Python MyServiceProviderComp\n' + \
                       'TkJoyStick          : start Python TkJoyStickComp.py\n' + \
                       'TkLRFViewer         : start Python TkLRFViewer.py\n' + \
                       'bash                : start bash'
        argparser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter)
        argparser.add_argument('command', type=str,
                               default='bash', help=help_message)
        argparser.add_argument(
            '-v', '--version', action='version', version='%(prog)s 1.0.0')
        argparser.add_argument('-n', '--nameserver', action='store_true',
                               help='run command with starting nameserver')
        argparser.add_argument('-t', '--tag', type=str, dest='tagname',
                               default='latest', help='tag name of image')
        argparser.add_argument(
            '-r', '--rdp', action='store_true', help='run command with start RDP server')
        argparser.add_argument('-d', '--device', type=str, dest='device',
                               help='allow access to device from inside of container')
        argparser.add_argument('-e', '--execute', type=str,
                               dest='run_component', help='run your C++ component')
        argparser.add_argument('-c', '--compile', type=str,
                               dest='compile_component', help='compile your C++ component')
        argparser.add_argument(
            '-x', '--xforward', action='store_true', help='enable X forwarding')
        argparser.add_argument('-U', '--upgrade', action='store_true',
                               help='upgrade target image before startup')
        argparser.add_argument('--dryrun', action='store_true', help='dry run for debug')
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
                  "ConfigSample": example + "/ConfigSampleComp",
                  "SeqIn": example + "/SeqInComp",
                  "SeqOut": example + "/SeqOutComp",
                  "MyServiceConsumer": example + "/MyServiceConsumerComp",
                  "MyServiceProvider": example + "/MyServiceProviderComp",
                  "ConsoleInPy": example_py + "/SimpleIO/ConsoleIn.py",
                  "ConsoleOutPy": example_py + "/SimpleIO/ConsoleOut.py",
                  "ConfigSamplePy": example_py + "/ConfigSample/ConfigSample.py",
                  "SeqInPy": example_py + "/SeqIO/SeqIn.py",
                  "SeqOutPy": example_py + "/SeqIO/SeqOut.py",
                  "MyServiceConsumerPy": example_py + "/SimpleService/MyServiceConsumer.py",
                  "MyServiceProviderPy": example_py + "/SimpleService/MyServiceProvider.py",
                  "TkJoyStick": example_py + "/TkJoyStick/TkJoyStickComp.py",
                  "TkLRFViewer": example_py + "/TkLRFViewer/TkLRFViewer.py",
                  "bash": "bash",
                  }

        try:
            c = c_dict[command]
        except KeyError:
            logging.warning("undefined command: " +
                            command + ", iinstead use bash")
            c = "bash"

        return c

    def assume_options(self, args, command):
        # Docker Option
        option_list = []

        # Mount home directory
        if self._platform == "win32":
            user = os.environ.get('USERNAME')
            home = os.environ.get('USERPROFILE')
            entry = "/home/" + user
            option = "-v " + home + ":" + entry + ":rw --privileged=true --workdir=" + entry
        else:
            home = os.environ.get('HOME')
            entry = home
            option = "-v " + home + ":" + entry + ":rw --privileged=true --workdir=" + entry
        logging.info("mount: " + str(option))
        option_list.append(option)

        # Device access
        logging.info("device: " + str(args.device))
        if args.device:
            option_device = "--device=" + args.device
            option_list.append(option_device)

        # Set X forwarding
        logging.info("x-forward: " + str(args.xforward))
        if args.xforward:
            display = os.environ.get('DISPLAY')
            option_display = "-e DISPLAY=" + display + \
                " -v /tmp/.X11-unix:/tmp/.X11-unix -v " + \
                home + "/.Xauthority:/root/.Xauthority"
            option_list.append(option_display)

        # Add starting xrdp service
        logging.info("rdp: " + str(args.rdp))
        if args.rdp:
            command = "/etc/init.d/xrdp start;" + command

        # Add starting nameserver
        logging.info("nameserver: " + str(args.nameserver))
        if args.nameserver:
            command = "rtm-naming;" + command

        # Compile RTC
        logging.info("compile_component: " + str(args.compile_component))
        if args.compile_component:
            # Compile C++ component
            command = "apt-get update && apt-get -y install cmake && cd " + \
                os.getcwd() + " && mkdir -p build && cd build cmake .. && make"

        # Startup RTC
        logging.info("run_component: " + str(args.run_component))
        if args.run_component:
            if args.run_component in '.py':
                # Python component
                command = "cd " + os.getcwd() + " && python " + args.run_component
            else:
                # C++ component
                command = "cd " + os.getcwd() + " && ./" + args.run_component

        option_network = "--net=host"
        option_list.append(option_network)
        option_list.append("takahasi/docker-openrtm:" + args.tagname)
        option_list.append("\"" + command + "\"")

        # Naming randomly
        name = "docker-openrtm-" + str(random.randint(0, 99)) + " "

        # Upgrade image
        logging.info("upgrade: " + str(args.upgrade))
        if args.upgrade:
            return "docker pull takahasi/docker-openrtm:" + args.tagname + "&& docker run -ti --rm --name " + name + " ".join(option_list)
        else:
            return "docker run -ti --rm --name " + name + " ".join(option_list)

    def enable_x(self):
        if self._platform != "win32":
            try:
                subprocess.call("xhost local: > /dev/null", shell=True)
            except subprocess.CalledProcessError:
                logging.error("xhost was exited by exception")
        return

    def disable_x(self):
        if self._platform != "win32":
            try:
                subprocess.call("xhost - > /dev/null", shell=True)
            except subprocess.CalledProcessError:
                logging.error("xhost was exited by exception")
        return


def main():
    rtmdocker = Rtmdocker()
    rtmdocker.start()
    return


if __name__ == "__main__":
    main()
