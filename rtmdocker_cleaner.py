#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

import sys
import argparse
import subprocess
import logging
import distutils.spawn


class RtmdockerCleaner:
    ''' Utility class to operate OpenRTM on Docker

    This is utility class to operate OpenRTM on Docker.

    '''

    def __init__(self):
        # Set parser
        self._args = self.parser()
        # Set logger
        logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s',
                            level=logging.INFO)
        # Check docker command exsting
        if not distutils.spawn.find_executable('docker'):
            logging.error(
                "Docker is not installed. Please install Docker first.")
            sys.exit(1)

    def parser(self):
        argparser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter)
        argparser.add_argument(
            '-v', '--version', action='version', version='%(prog)s 1.0.0')
        argparser.add_argument('-i', '--images', action='store_true',
                               help='remove all docker images')
        argparser.add_argument('-c', '--containers', action='store_true',
                               help='stop & remove all docker containers')
        argparser.add_argument('-a', '--all', action='store_true',
                               help='remove all docker containers & images')
        argparser.add_argument('--dryrun', action='store_true', help='dry run for debug')
        return argparser.parse_args()

    def start(self):
        # stop & remove all docker images
        logging.info("Start cleanup all images...")
        if self._args.containers or self._args.all:
            self.remove_containers()
        if self._args.images or self._args.all:
            self.remove_images()
        logging.info("Completed")

    def remove_containers(self):
        # check all docker containers
        ps = ""
        try:
            cmd = "docker ps -a -q"
            ps = subprocess.check_output(cmd, shell=True).replace("\n", "")
        except subprocess.CalledProcessError:
            logging.info("No containers...")

        # stop & remove all docker containers if exist
        if ps:
            logging.info("containers: " + ps)
            cmd = "docker stop " + str(ps)
            logging.info("command: " + cmd)
            subprocess.call(cmd.split(" "))
            cmd = "docker rm -f " + str(ps)
            logging.info("command: " + cmd)
            if not self._args.dryrun:
                subprocess.call(cmd.split(" "))
        return

    def remove_images(self):
        # check all docker images
        images = ""
        try:
            cmd = "docker images -a -q"
            images = subprocess.check_output(cmd, shell=True).replace("\n", "")
        except subprocess.CalledProcessError:
            logging.info("No images...")

        # remove all docker images if exist
        if images:
            cmd = "docker rmi -f " + str(images)
            logging.info("command: " + cmd)
            if not self._args.dryrun:
                subprocess.call(cmd.split(" "))
        return


def main():
    cleaner = RtmdockerCleaner()
    cleaner.start()
    return


if __name__ == "__main__":
    main()
