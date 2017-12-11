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
            ps = ""
            try:
                ps = subprocess.check_output(["docker", "ps",  "-a", "-q"])
            except subprocess.CalledProcessError:
                logging.debug("No containers...")

            if ps:
                logging.info("containers: " + ps)
                subprocess.call(["docker", "stop", ps])
                subprocess.call(["docker", "rm", "-f", str(ps)])

        if self._args.images or self._args.all:
            images = ""
            try:
                images = subprocess.check_output(["docker", "images",  "-a", "-q"])
            except subprocess.CalledProcessError:
                logging.debug("No images...")

            if images:
                logging.info("images: " + images)
                subprocess.call(["docker", "rmi", "-f", str(images)])

        logging.info("Completed")
        return


def main():
    cleaner = RtmdockerCleaner()
    cleaner.start()
    return


if __name__ == "__main__":
    main()
