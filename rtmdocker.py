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
        self._command = self.assume_options(command)
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
        help_message = (
            'openrtp             : start OpenRTP\n'
            'Controller          : start C++ ControllerComp\n'
            'Motor               : start C++ MotorComp\n'
            'ConsoleIn           : start C++ ConsoleInComp\n'
            'ConsoleOut          : start C++ ConsoleOutComp\n'
            'ConfigSample        : start C++ ConfigSampleComp\n'
            'SeqIn               : start C++ SeqInComp\n'
            'SeqOut              : start C++ SeqOutComp\n'
            'MyServiceConsumer   : start C++ MyServiceConsumerComp\n'
            'MyServiceProvider   : start C++ MyServiceProviderComp\n'
            'ConsoleInPy         : start Python ConsoleIn.py\n'
            'ConsoleOutPy        : start Python ConsoleOut.py\n'
            'ConfigSamplePy      : start Python ConfigSampleComp\n'
            'SeqInPy             : start Python SeqIn.py\n'
            'SeqOutPy            : start Python SeqOut.py\n'
            'MyServiceConsumerPy : start Python MyServiceConsumerComp\n'
            'MyServiceProviderPy : start Python MyServiceProviderComp\n'
            'TkJoyStick          : start Python TkJoyStickComp.py\n'
            'TkLRFViewer         : start Python TkLRFViewer.py\n'
            'Affine              : start OpenCV AffineComp\n'
            'BackGroundSubtractionSimple '
            ': start OpenCV BackGroundSubtractionSimpleComp\n'
            'Binarization        : start OpenCV BinarizationComp\n'
            'CameraViewer        : start OpenCV CameraViewerComp\n'
            'Chromakey           : start OpenCV ChromakeyComp\n'
            'DilationErosion     : start OpenCV DilationErotionComp\n'
            'Edge                : start OpenCV EdgeComp\n'
            'Findcontour         : start OpenCV FindcontourComp\n'
            'Flip                : start OpenCV FlipComp\n'
            'Histogram           : start OpenCV HistogramComp\n'
            'Hough               : start OpenCV HoughComp\n'
            'ImageCalibration    : start OpenCV ImageCalibrationComp\n'
            'ImageSubstraction   : start OpenCV ImageSubstractionComp\n'
            'ObjectTracking      : start OpenCV ObjectTrackingComp\n'
            'OpenCVCamera        : start OpenCV OpenCVCameraComp\n'
            'Perspective         : start OpenCV PerspectiveComp\n'
            'RockPaperScissors   : start OpenCV RockPaperScissorsComp\n'
            'Rotate              : start OpenCV RotateComp\n'
            'Scale               : start OpenCV ScaleComp\n'
            'Sepia               : start OpenCV SepiaComp\n'
            'SubstractCaptureImage : start OpenCV SubstractCaptureImageComp\n'
            'Template            : start OpenCV TemplateComp\n'
            'Translate           : start OpenCV TranslateComp\n'
            'bash                : start bash')

        argparser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter)
        argparser.add_argument(
            'command', type=str,
            default='bash', help=help_message)
        argparser.add_argument(
            '-v', '--version', action='version', version='%(prog)s 1.0.0')
        argparser.add_argument(
            '-n', '--nameserver', action='store_true',
            help='run command with starting nameserver')
        argparser.add_argument(
            '-t', '--tag', type=str, dest='tagname',
            default='latest', help='tag name of image')
        argparser.add_argument(
            '-r', '--rdp', action='store_true',
            help='run command with start RDP server')
        argparser.add_argument(
            '-d', '--device', type=str, dest='device',
            help='allow access to device from inside of container')
        argparser.add_argument(
            '-e', '--execute', type=str, dest='run_component',
            help='run your C++ component')
        argparser.add_argument(
            '-c', '--compile', type=str, dest='compile_component',
            help='compile your C++ component')
        argparser.add_argument(
            '-x', '--xforward', action='store_true',
            help='enable X forwarding')
        argparser.add_argument(
            '-U', '--upgrade', action='store_true',
            help='upgrade target image before startup')
        argparser.add_argument(
            '--dryrun', action='store_true',
            help='dry run for debug')
        return argparser.parse_args()

    def assume_command(self, command):
        # OpenRTM version check
        if "120" in self._args.tagname:
            cpp = "/usr/share/openrtm-1.2/components/c++/examples/"
            py = "python /usr/share/openrtm-1.2/components/c++/examples/"
            cv = "/usr/share/openrtm-1.1/components/c++/opencv-rtcs/"
        else:
            cpp = "/usr/share/openrtm-1.1/example/"
            py = "python " + cpp + "/python/"
            cv = "/usr/share/openrtm-1.1/components/c++/opencv-rtcs/"

        # command list
        c_dict = {
            "openrtp": "openrtp",
            "Controller": cpp + "ControllerComp",
            "Motor": cpp + "MotorComp",
            "ConsoleIn": cpp + "ConsoleInComp",
            "ConsoleOut": cpp + "ConsoleOutComp",
            "ConfigSample": cpp + "ConfigSampleComp",
            "SeqIn": cpp + "SeqInComp",
            "SeqOut": cpp + "SeqOutComp",
            "MyServiceConsumer": cpp + "MyServiceConsumerComp",
            "MyServiceProvider": cpp + "MyServiceProviderComp",
            "ConsoleInPy": py + "SimpleIO/ConsoleIn.py",
            "ConsoleOutPy": py + "SimpleIO/ConsoleOut.py",
            "ConfigSamplePy": py + "ConfigSample/ConfigSample.py",
            "SeqInPy": py + "SeqIO/SeqIn.py",
            "SeqOutPy": py + "SeqIO/SeqOut.py",
            "MyServiceConsumerPy": py + "SimpleService/MyServiceConsumer.py",
            "MyServiceProviderPy": py + "SimpleService/MyServiceProvider.py",
            "TkJoyStick": py + "TkJoyStick/TkJoyStickComp.py",
            "TkLRFViewer": py + "TkLRFViewer/TkLRFViewer.py",
            "Affine": cv + "AffineComp",
            "BackGroundSubtractionSimple": cv + "BackGroundSubtractionSimpleComp",
            "Binarization": cv + "BinarizationComp",
            "CameraViewer": cv + "CameraViewerComp",
            "Chromakey": cv + "ChromakeyComp",
            "DilationErosion": cv + "DilationErotionComp",
            "Edge": cv + "EdgeComp",
            "Findcontour": cv + "FindcontourComp",
            "Flip": cv + "FlipComp",
            "Histogram": cv + "HistogramComp",
            "Hough": cv + "HoughComp",
            "ImageCalibration": cv + "ImageCalibrationComp",
            "ImageSubstraction": cv + "ImageSubstractionComp",
            "ObjectTracking": cv + "ObjectTrackingComp",
            "OpenCVCamera": cv + "OpenCVCameraComp",
            "Perspective": cv + "PerspectiveComp",
            "RockPaperScissors": cv + "RockPaperScissorsComp",
            "Rotate": cv + "RotateComp",
            "Scale": cv + "ScaleComp",
            "Sepia": cv + "SepiaComp",
            "SubstractCaptureImage": cv + "SubstractCaptureImageComp",
            "Template": cv + "TemplateComp",
            "Translate": cv + "TranslateComp",
            "bash": "bash"}

        try:
            c = c_dict[command]
        except KeyError:
            logging.warning("undefined command: " +
                            command + ", iinstead use bash")
            c = "bash"

        return c

    def assume_options(self, command):
        # Docker Option
        option_list = []

        # Mount home directory
        option = self.get_mountpoint()
        logging.info("mount: " + str(option))
        option_list.append(option)

        # Device access
        logging.info("device: " + str(self._args.device))
        if self._args.device:
            option_device = "--device=" + self._args.device
            option_list.append(option_device)

        # Set X forwarding
        logging.info("x-forward: " + str(self._args.xforward))
        if self._args.xforward:
            display = os.environ.get('DISPLAY')
            option_display = "-e DISPLAY=" + display + \
                " -v /tmp/.X11-unix:/tmp/.X11-unix -v " + \
                self.get_home() + "/.Xauthority:/root/.Xauthority"
            option_list.append(option_display)

        # Add starting xrdp service
        logging.info("rdp: " + str(self._args.rdp))
        if self._args.rdp:
            command = "/etc/init.d/xrdp start;" + command

        # Add starting nameserver
        logging.info("nameserver: " + str(self._args.nameserver))
        if self._args.nameserver:
            command = "rtm-naming;" + command

        # Compile RTC
        logging.info("compile_component: " + str(self._args.compile_component))
        if self._args.compile_component:
            # Compile C++ component
            command = "apt-get update && apt-get -y install cmake && cd " + \
                os.getcwd() + " && mkdir -p build && cd build cmake .. && make"

        # Startup RTC
        logging.info("run_component: " + str(self._args.run_component))
        if self._args.run_component:
            if self._args.run_component in '.py':
                # Python component
                command = "cd " + os.getcwd() + \
                    " && python " + self._args.run_component
            else:
                # C++ component
                command = "cd " + os.getcwd() + \
                    " && ./" + self._args.run_component

        option_network = "--net=host"
        option_list.append(option_network)
        option_list.append("takahasi/docker-openrtm:" + self._args.tagname)
        option_list.append("\"" + command + "\"")

        # Naming randomly
        name = "docker-openrtm-" + str(random.randint(0, 99)) + " "

        # Upgrade image
        logging.info("upgrade: " + str(self._args.upgrade))
        if self._args.upgrade:
            return "docker pull takahasi/docker-openrtm:" + \
                self._args.tagname + "&& docker run -ti --rm --name " + \
                name + " ".join(option_list)
        else:
            return "docker run -ti --rm --name " + name + " ".join(option_list)

    def get_home(self):
        if self._platform == "win32":
            return os.environ.get('USERPROFILE')
        else:
            return os.environ.get('HOME')

    def get_mountpoint(self):
        # Mount home directory
        if self._platform == "win32":
            h = self.get_home()
            e = "/home/" + os.environ.get('USERNAME')
            option = "-v " + h + ":" + e + \
                ":rw --privileged=true --workdir=" + e
        else:
            h = self.get_home()
            option = "-v " + h + ":" + h + \
                ":rw --privileged=true --workdir=" + h
        return option

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
