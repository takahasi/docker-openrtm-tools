#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

import os


def main():
    os.system("docker build --network=host -t sample .")
    os.system("docker run --network=host -it sample")
    return

if __name__ == "__main__":
    main()
